#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional, List, Any, Tuple

import pandas as pd

APPLE_EPOCH_UTC = datetime(2001, 1, 1, tzinfo=timezone.utc)
SMS_DB_FILE_ID = "3d0d7e5fb2ce288813306e4d4636395e047a3d28"


@dataclass(frozen=True)
class FoundDB:
    db_path: str
    backup_dir: str
    mtime: float


def normalize_handle_id(s: Optional[str]) -> str:
    if s is None:
        return ""
    s = str(s).strip().lower()
    s = re.sub(r"[\s\-\(\)\.]", "", s)
    return s


def normalize_digit_pattern(s: Optional[str]) -> str:
    if s is None:
        return ""
    return re.sub(r"\D", "", str(s))


def safe_filename_fragment(s: str, max_len: int = 50) -> str:
    s = normalize_handle_id(s)
    s = re.sub(r"[^a-z0-9\+@]", "_", s).strip("_")
    return (s[:max_len] or "filtered")


def apple_coredata_to_datetime(value) -> Optional[datetime]:
    if value is None:
        return None
    try:
        v = int(value)
    except (TypeError, ValueError):
        return None

    # heuristic: ns since 2001 is huge, seconds is not
    if v > 10**12:
        dt = APPLE_EPOCH_UTC + timedelta(seconds=v / 1_000_000_000)
    else:
        dt = APPLE_EPOCH_UTC + timedelta(seconds=v)

    return dt.astimezone()


def iter_candidate_backup_roots() -> Iterable[str]:
    appdata = os.environ.get("APPDATA")
    userprofile = os.environ.get("USERPROFILE")

    if appdata:
        yield os.path.join(appdata, "Apple Computer", "MobileSync", "Backup")
    if userprofile:
        yield os.path.join(userprofile, "Apple", "MobileSync", "Backup")

    # macOS (harmless on Windows)
    yield os.path.expanduser("~/Library/Application Support/MobileSync/Backup")


def find_messages_db_in_backups() -> str:
    found: List[FoundDB] = []
    for root in iter_candidate_backup_roots():
        if not root or not os.path.isdir(root):
            continue

        try:
            backup_dirs = [
                os.path.join(root, d)
                for d in os.listdir(root)
                if os.path.isdir(os.path.join(root, d))
            ]
        except OSError:
            continue

        for bdir in backup_dirs:
            c1 = os.path.join(bdir, SMS_DB_FILE_ID)
            c2 = os.path.join(bdir, SMS_DB_FILE_ID[:2], SMS_DB_FILE_ID)
            for candidate in (c1, c2):
                if os.path.isfile(candidate):
                    try:
                        mtime = os.path.getmtime(candidate)
                    except OSError:
                        mtime = 0.0
                    found.append(FoundDB(candidate, bdir, mtime))
                    break

    if not found:
        roots = "\n  - " + "\n  - ".join(iter_candidate_backup_roots())
        raise FileNotFoundError(
            "Could not auto-locate the Messages database in your iPhone backups.\n"
            f"Searched for hashed file name: {SMS_DB_FILE_ID}\n"
            f"Searched under these roots (if they exist):{roots}\n"
            "You can also pass --db explicitly."
        )

    best = max(found, key=lambda x: x.mtime)
    return best.db_path


def _coerce_bytes(b: Any) -> Optional[bytes]:
    if b is None:
        return None
    if isinstance(b, (bytes, bytearray)):
        return bytes(b)
    if isinstance(b, memoryview):
        return b.tobytes()
    return None


def _walk_find_strings(obj: Any, max_depth: int = 6) -> List[str]:
    """Best-effort recursive string extraction from decoded typedstream objects."""
    out: List[str] = []

    def rec(x: Any, d: int):
        if x is None or d > max_depth:
            return
        if isinstance(x, str):
            out.append(x)
            return
        # common typedstream objects: NSString('...') with attribute `.value`
        if hasattr(x, "value") and isinstance(getattr(x, "value"), str):
            out.append(getattr(x, "value"))
            return
        # sometimes attributed strings may expose `.string`
        if hasattr(x, "string") and isinstance(getattr(x, "string"), str):
            out.append(getattr(x, "string"))
            return

        # containers
        if isinstance(x, dict):
            for v in x.values():
                rec(v, d + 1)
            return
        if isinstance(x, (list, tuple, set)):
            for v in x:
                rec(v, d + 1)
            return

        # generic typedstream objects may be indexable
        try:
            if hasattr(x, "__len__") and hasattr(x, "__getitem__"):
                n = len(x)
                for i in range(min(n, 50)):
                    rec(x[i], d + 1)
                return
        except Exception:
            pass

        # last resort: inspect attributes
        try:
            for v in vars(x).values():
                rec(v, d + 1)
        except Exception:
            return

    rec(obj, 0)
    return out


def decode_attributed_body(blob: Any) -> Optional[str]:
    b = _coerce_bytes(blob)
    if not b:
        return None

    # 1) Robust path: pytypedstream (if installed)
    try:
        import typedstream  # pip install pytypedstream

        obj = typedstream.unarchive_from_data(b)
        strings = _walk_find_strings(obj)
        # choose the longest "reasonable" string
        strings = [s.strip() for s in strings if s and s.strip()]
        if strings:
            return max(strings, key=len)
    except Exception:
        pass

    # 2) Fallback heuristic (brittle but often works)
    try:
        s = b.decode("utf-8", errors="replace")
    except Exception:
        return None

    # Heuristic based on common patterns seen in attributedBody dumps
    if "NSNumber" in s and "NSString" in s:
        s = s.split("NSNumber", 1)[0]
        s = s.split("NSString", 1)[-1]
        if "NSDictionary" in s:
            s = s.split("NSDictionary", 1)[0]

    # remove control chars that frequently appear in the blob
    s = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()

    return s or None


def export_csv(df_final: pd.DataFrame, out_path: str) -> None:
    df_final.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(df_final):,} rows to {out_path}")


def show_top_ids(df_final: pd.DataFrame, top_n: int = 20) -> None:
    counts = df_final["id"].dropna().astype(str).value_counts().head(top_n)
    if counts.empty:
        print("No handle IDs found to list.")
        return
    print("\nMost common handle IDs (top {}):".format(top_n))
    for handle_id, cnt in counts.items():
        print(f"  {handle_id}  ({cnt:,} messages)")


def export_all_conversations(
    df_final: pd.DataFrame, out_dir: str
) -> List[dict]:
    os.makedirs(out_dir, exist_ok=True)

    work = df_final.copy()
    work["id"] = work["id"].fillna("").astype(str)
    work["id_norm"] = work["id"].apply(normalize_handle_id)

    conversation_meta: List[dict] = []
    grouped = work[work["id_norm"] != ""].groupby("id_norm", sort=False)

    for _, group in grouped:
        conversation = group.copy()
        conversation.sort_values(
            by="date_dt", ascending=False, inplace=True, kind="mergesort")

        raw_ids = [x for x in conversation["id"].tolist() if str(x).strip()]
        canonical_id = raw_ids[0] if raw_ids else "unknown"
        filename = f"my_messages_{safe_filename_fragment(canonical_id)}.csv"
        export_path = os.path.join(out_dir, filename)
        export_csv(conversation.drop(columns=["id_norm", "date_dt"]), export_path)

        oldest_first = conversation.sort_values(
            by="date_dt", ascending=True, kind="mergesort")
        preview_messages = oldest_first["text"].head(100).astype(str).tolist()
        latest_date = conversation["date_dt"].max()

        conversation_meta.append(
            {
                "id_norm": normalize_handle_id(canonical_id),
                "id": canonical_id,
                "digits": normalize_digit_pattern(canonical_id),
                "export_path": export_path,
                "latest_date": latest_date,
                "preview_blob": "\n".join(preview_messages).casefold(),
            }
        )

    return conversation_meta


def select_conversation(
    query: str, conversation_meta: List[dict]
) -> Tuple[Optional[dict], str]:
    query = (query or "").strip()
    if not query:
        return None, "No filter value provided."

    digit_pattern = normalize_digit_pattern(query)
    if digit_pattern:
        matches = [
            convo for convo in conversation_meta
            if digit_pattern in convo["digits"]
        ]
        if not matches:
            return None, (
                f"No conversation matched the number pattern '{query}'."
            )

        chosen = max(
            matches,
            key=lambda convo: convo["latest_date"] or datetime.min.replace(
                tzinfo=timezone.utc),
        )
        if len(matches) > 1:
            return chosen, (
                f"Matched {len(matches)} conversations for number pattern '{query}'. "
                f"Using the most recent one: {chosen['id']}"
            )
        return chosen, f"Matched conversation: {chosen['id']}"

    name_query = query.casefold()
    matches = [
        convo for convo in conversation_meta
        if name_query in convo["preview_blob"]
    ]
    if not matches:
        return None, (
            f"No conversation had '{query}' in its first 100 messages."
        )

    chosen = max(
        matches,
        key=lambda convo: convo["latest_date"] or datetime.min.replace(
            tzinfo=timezone.utc),
    )
    if len(matches) > 1:
        return chosen, (
            f"Found {len(matches)} conversations with '{query}' in the first 100 messages. "
            f"Using the one with the most recent activity: {chosen['id']}"
        )
    return chosen, (
        f"Matched by name in the first 100 messages: {chosen['id']}"
    )


def copy_selected_export(export_path: str, cwd: Optional[str] = None) -> str:
    target_dir = cwd or os.getcwd()
    os.makedirs(target_dir, exist_ok=True)
    destination = os.path.join(target_dir, os.path.basename(export_path))

    if os.path.abspath(export_path) != os.path.abspath(destination):
        shutil.copy2(export_path, destination)

    print(f"Copied selected conversation to {destination}")
    return destination


def main():
    parser = argparse.ArgumentParser(
        description="Extract iPhone Messages to CSV (with attributedBody decoding)")
    parser.add_argument(
        "--db", default=None, help="Path to messages DB. If omitted, auto-searches backups.")
    parser.add_argument("--out", default="my_messages.csv",
                        help="Output CSV filename for full export")
    parser.add_argument(
        "--conversations-dir",
        default="my_messages_by_contact",
        help="Directory where every conversation CSV will be exported",
    )
    parser.add_argument(
        "--filter", "--filter-id",
        dest="filter_value",
        default=None,
        help=(
            "Optional conversation selector. Digits are treated as a phone-number "
            "pattern; any other text is treated as a name to search for in the first "
            "100 messages of each conversation."
        ),
    )
    args = parser.parse_args()

    db_path = args.db if args.db else find_messages_db_in_backups()
    print(f"Using database: {db_path}")

    query = """
    SELECT
        m.text            AS text,
        m.attributedBody  AS attributedBody,
        m.is_from_me      AS is_from_me,
        m.date            AS date,
        h.id              AS handle_id
    FROM message AS m
    LEFT JOIN handle AS h
        ON m.handle_id = h.ROWID
    """

    with sqlite3.connect(db_path) as con:
        df = pd.read_sql_query(query, con)

    # Convert date
    df["date_dt"] = df["date"].apply(apple_coredata_to_datetime)
    df["date"] = df["date_dt"].apply(lambda x: x.isoformat(
        timespec="seconds") if x is not None else None)

    # Fill missing text from attributedBody
    def _body(row):
        if row["text"] is not None and str(row["text"]).strip() != "":
            return row["text"]
        return decode_attributed_body(row["attributedBody"])

    df["text"] = df.apply(_body, axis=1)

    # Now filter out null/empty bodies (after decoding)
    df = df[df["text"].notna()]
    df = df[df["text"].astype(str).str.strip() != ""]

    # Sender
    df["Sender"] = df.apply(
        lambda r: "Me" if int(r["is_from_me"] or 0) == 1 else r["handle_id"],
        axis=1,
    )

    # Final columns
    df_final = df[["text", "is_from_me", "date",
                   "handle_id", "Sender", "date_dt"]].copy()
    df_final.rename(columns={"handle_id": "id"}, inplace=True)

    # Full export (most recent on top)
    df_full = df_final.sort_values(
        by="date_dt", ascending=False, kind="mergesort").drop(columns=["date_dt"])
    export_csv(df_full, args.out)

    conversation_meta = export_all_conversations(
        df_final, args.conversations_dir)
    print(
        f"Exported {len(conversation_meta):,} conversations to {args.conversations_dir}"
    )

    # Optional filtering / selection
    filter_value = args.filter_value
    if filter_value is None and sys.stdin.isatty():
        show_top_ids(df_final)
        print(
            "\nOptional: enter digits from a phone number, or enter a name to search "
            "within the first 100 messages of each conversation."
        )
        print("Press Enter to skip.")
        filter_value = input("Conversation to filter: ").strip() or None

    if filter_value:
        selected, message = select_conversation(filter_value, conversation_meta)
        print(message)
        if selected is None:
            sys.exit(1)
        copy_selected_export(selected["export_path"], os.getcwd())
    else:
        print("No specific conversation selected; done.")


if __name__ == "__main__":
    main()
