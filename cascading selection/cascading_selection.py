"""Filter and select data to which values are assigned."""

from typing import List
import argparse
import logging
import pandas as pd

__version__ = "1.0.0"


def cascading_assignment(data: pd.DataFrame,
                         sel_r: pd.DataFrame,
                         priority: List[str]) -> pd.DataFrame:
    """Assigns values to the data based on the cascading selection rules.

    Parameters
    ----------
    data : pd.DataFrame
        The data which contains the entries with properties
        and to which further properties should be added.
    sel_r : pd.DataFrame
        The selection rules and property values to be assigned.
        Column names contained within the priority list and
        properties on which the filters can be applied, the remaining
        are the new properties that needed to be assigned to
        the data. Use nan values to represent a selection rules that
        applies to all entries, aka * or ALL.
    priority : List[str]
        The name of the columns containing properties on which
        selection rules can be applied.

    Returns
    -------
    pd.DataFrame
        The data together with the newly assigned properties.
        Keeps the order of entries (aka stable).
    """
    # check if rules are non-colliding and make them unique
    if sel_r[[*priority]].duplicated().any():
        logging.error("Selection rule collision: two or more rules "
                      "set the properties for the same set of "
                      "property values. The first rule(s) are kept."
                      "Colliding rule e.g.:\n%s\nvs\n%s",
                      sel_r[sel_r.duplicated(subset=[*priority],
                                             keep=False)].iloc[[0], :],
                      sel_r[sel_r.duplicated(subset=[*priority])].iloc[[0], :])
        sel_r.drop_duplicates(subset=[*priority], inplace=True)

    # identify the column names containing the values needed to be assigned
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
        if score == 0:  # default assignment
            def_vals = sel_r.loc[sns["score"] == score, [*val_n]]
            assert len(def_vals) == 1
            ret[[*val_n]] = def_vals.iloc[0].to_list()
            continue
        rule_group = sel_r.loc[sns["score"] == score, [*selectors, *val_n]]
        merged = pd.merge(ret[[data.index.name, *priority]],
                          rule_group,
                          how="inner",
                          on=selectors)
        ret.update(merged.set_index(data.index.name)[val_n])
    ret.set_index(data.index.name, inplace=True)
    return ret


def _calc_scores(m_rule: pd.DataFrame, priority) -> None:
    """Assign the priority scores to the selection rules."""

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=('Assign properties to '
                                                  'entries based on '
                                                  'cascading selection '
                                                  'rules.'))
    parser.add_argument('data_fname',
                        metavar='data.csv',
                        help=('The filename that contains the data to which'
                              ' new properties need to be assigned.'))
    parser.add_argument('sel_prop_fname',
                        metavar='rules.csv',
                        help=('The filename that contains the selection rules '
                              'and the properties that are needed to be '
                              'assigned to the data. The columns must be '
                              'ordered in a decreasing priority order, '
                              'followed by the columns of the properties.'))
    parser.add_argument('nof_sel_col',
                        metavar="N",
                        help=('The number of columns containing the selection '
                              'rules.'),
                        type=int)
    parser.add_argument('--output_fname', '-o',
                        metavar='data_with_properties.csv',
                        help=('If given, the output is written '
                              'to this file in csv format '
                              'instead of the stdout in padded text format.'))
    args = parser.parse_args()

    dat = pd.read_csv(args.data_fname)
    dat.index.name = "df index"  # it must not be None
    dat.add_prefix("_")  # add prefix so name collision can be precented
    sel_rule = pd.read_csv(args.sel_prop_fname)
    sel_rule.index.name = "line num"
    priori = sel_rule.columns[:args.nof_sel_col]

    result = cascading_assignment(dat, sel_rule, priori)

    # remove what has been added
    dat.columns = dat.columns.str.replace(r'^_', '', regex=True)

    if args.output_fname is not None:
        result.to_csv(args.output_fname, index=False)
    else:
        print(result.to_string(index=False))
