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

    # put index to a regular column so that merge keeps it
    ret.reset_index(inplace=True)

    sns = _calc_scores(sel_r, priority)  # scores and selectors

    sns.sort_values("score", inplace=True)
    for _, rule_property in sns.drop_duplicates("score").iterrows():
        score, selectors = rule_property[["score", "selectors"]]

        rule_group = sel_r.loc[sns["score"] == score, [*selectors, *val_n]]
        merged = pd.merge(ret[[data.index.name, *priority]],
                          rule_group,
                          how="inner",
                          on=selectors)
        ret.update(merged.set_index(data.index.name)[val_n])
    ret.set_index(data.index.name)
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
dat.index.name = "pd index"
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
