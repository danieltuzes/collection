"""Create example entries for the data and selection rules."""

import pandas as pd
import numpy as np
np.random.seed(0)

family_names = ["SMITH", "JOHNSON", "WILLIAMS", "BROWN", "JONES", "GARCIA",
                "MILLER", "DAVIS", "RODRIGUEZ", "MARTINEZ", "HERNANDEZ"]

given_names = ["Maria", "Nushi", "Mohammed", "Jose", "Muhammad", "Mohamed",
               "Wei", "Mohammad", "Ahmed", "Yan", "Ali", "John", "David", "Li"]

colors = ["red", "green", "blue", "yellow", "cyan", "magenta"]

LENGTH = len(colors) * len(given_names) * len(family_names)

p_data = {"PID": range(LENGTH),
          "family name": np.random.choice(family_names, LENGTH),
          "given name": np.random.choice(given_names, LENGTH),
          "fav color": np.random.choice(colors, LENGTH),
          "visitor": np.random.choice([True, False], LENGTH)}


def create_data():
    """Create the data file to which we want to assing values."""

    people = pd.DataFrame(data=p_data)
    people.to_csv("people.csv", index=False)


def create_selector():
    """Create the file of selection rules and assigned values."""
    sel_r_data = {"visitor": True,
                  "hall": "base",
                  "buffet": np.random.choice(["1st", "2nd", "3rd"], 10)}
    columns = [*p_data, "hall", "buffet"]
    sel_r = pd.DataFrame(data=sel_r_data, columns=[*columns])

    sel_r.loc[0, ["visitor", "buffet", "hall"]] = (pd.NA, "street", pd.NA)
    sel_r.loc[1, "hall"] = "base"

    sel_r.loc[2, ["fav color", "hall"]] = ["red", "prim"]
    sel_r.loc[3, ["fav color", "hall"]] = ["green", "prim"]
    sel_r.loc[4, ["fav color", "hall"]] = ["blue", "prim"]

    sel_r.loc[5, ["given name",
                  "fav color",
                  "hall"]] = ["Maria", "red", "common"]
    sel_r.loc[6, ["family name",
                  "fav color",
                  "hall"]] = ["SMITH", "red", "common"]
    sel_r.loc[7, ["family name",
                  "given name",
                  "hall"]] = ["SMITH", "Maria", "famiglia"]

    sel_r.loc[8, ["PID", "hall"]] = [0, "VIP"]
    sel_r.loc[9, ["PID", "hall"]] = [1, "VIP"]
    sel_r.loc[10, ["PID", "hall"]] = [42, "VIP"]

    sel_r.to_csv("selection_rules.csv", index=False)


create_data()
create_selector()
