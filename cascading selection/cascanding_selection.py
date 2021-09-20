"""Filter and select data to which values are assigned."""

from typing import Hashable, List
import pandas as pd


def cascading_assignment(data: pd.DataFrame,
                         sel_r: pd.DataFrame,
                         priority: List[Hashable]) -> pd.DataFrame:
    """Assigns values to the data based on the cascading selection rules.

    Parameters
    ----------
    data : pd.DataFrame
        The data which contains the entries with properties
        and to which further properties should be added.
    sel_r : pd.DataFrame
        [description]
    priority : List[Hashable]
        [description]

    Returns
    -------
    pd.DataFrame
        [description]
    """
    # identify the column names containing hte values needed to be assigned
    val_n = sel_r.columns.to_list()
    for item in priority:
        val_n.remove(item)

    ret = data.assign(**{ass_val_name: None for ass_val_name in val_n})
    sns = _calc_scores(sel_r, priority)  # scores and selectors

    sns.sort_values("score", inplace=True)
    for _, rule_property in sns.drop_duplicates("score").iterrows():
        score, selectors = rule_property[["score", "selectors"]]

        rule_group = sel_r.loc[sns["score"] == score, [*selectors, *val_n]]
        merged = pd.merge(ret,
                          rule_group,
                          how="inner",
                          on=selectors,
                          suffixes=[None, " new"])

        col_tr = {old_name + " new": old_name for old_name in val_n}
        ret[val_n] = merged.filter(like=" new").rename(columns=col_tr)
    return ret


def _calc_scores(m_rule: pd.DataFrame, priority) -> None:
    """Calculate the scores and list the selectors."""

    scores = {item: 2**(len(priority)-i-1) for i, item in enumerate(priority)}
    sns = pd.DataFrame(index=m_rule.index)
    sns["score"] = 0
    sns["selectors"] = [[] for i in range(len(sns))]
    for item, score in scores.items():
        sns.loc[~m_rule[item].isna(), "score"] += score
        sns.loc[~m_rule[item].isna(), "selectors"] = \
            sns.loc[~m_rule[item].isna(), "selectors"].apply(
                lambda x: [*x, item])  # pylint: disable=cell-var-from-loop
    return sns


dat = pd.read_csv("people.csv")

sel_rule = pd.read_csv("selection_rules.csv",
                       dtype={"personal ID": "Int64",
                              "family name": str,
                              "given name": str,
                              "fav color": str,
                              "visitor": bool,
                              "hall": str,
                              "buffet": str})

priori = ["personal ID", "family name", "given name", "fav color", "visitor"]

result = cascading_assignment(dat, sel_rule, priori)

print("Done")
