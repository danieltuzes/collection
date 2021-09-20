# Cascading selection

Assign properties to entries in pandas dataframe
based on the values of the entries.
Multiple selection criteria can be created,
including collisions,
which is resolved on a priority basis defined by the user.

## Usage

The functionality is provided by the `cascading_selection.py` python file with 2 interfaces:

- a command line interface, where the script can be called with python and the arguments can be passed in the CLI. Call the script with `-h` option for more information.
- a python API by importing the function `cascading_assignment` from the python file. Read the docstring for further information.

## Example

The example below shows how to use this python program to assign new values
to set of data based on different subset of the data set
identified by the properties of the entries within the data.

Example data with the necessary files can be generated with the `example_creator.py` file.

Execute the program with
`python cascading_selection.py people.csv selection_rules.csv 5 -o result.csv`. Open the input files `people.csv` and `selection_rules.csv`, and the output file `result.csv` to easier follow the steps of this example.

In this example data from people are stored in a file `people.csv`. The first few lines
contain the followings:

| personal ID | family name | given name | fav color | visitor |
| ----------: | :---------- | :--------- | :-------- | :------ |
|           0 | GARCIA      | Mohamed    | blue      | False   |
|           1 | SMITH       | Mohamed    | green     | True    |
|           2 | BROWN       | Wei        | magenta   | True    |
|           3 | BROWN       | Jose       | yellow    | True    |
|           4 | DAVIS       | Ahmed      | magenta   | True    |
|           5 | MARTINEZ    | Nushi      | red       | False   |
|           6 | BROWN       | Muhammad   | yellow    | True    |
|          27 | SMITH       | Ali        | blue      | True    |
|         333 | SMITH       | Maria      | red       | True    |

Each entry corresponds to a single person. The data starts with an ID,
followed by the family name, given name and the favorite color of the person.
The last column tells if the person is going to attend a charity event or not.

Based on the these properties, the charity event organizer
would like to group the people, and assign different conference room for them,
and different buffets where they can use their coupons. The organizer would
like to append 2 more columns containing these information.

The assignment rules are contained within the file `selection_rules.csv`.
The whole content of the file is
shown below (the leftmost column is not part of the file):

|     | personal ID | family name | given name | fav color | visitor | hall     | buffet |
| --- | ----------: | :---------- | :--------- | :-------- | :------ | :------- | :----- |
| 0   |             |             |            | red       | True    | prim     | 1st    |
| 1   |             |             |            | green     | True    | prim     | 1st    |
| 2   |             |             |            | blue      | True    | prim     | 2nd    |
| 3   |             |             | Maria      | red       | True    | common   | 1st    |
| 4   |             | SMITH       |            | red       | True    | common   | 2nd    |
| 5   |             | SMITH       | Maria      |           | True    | famiglia | 3rd    |
| 6   |           0 |             |            |           | True    | VIP      | 2nd    |
| 7   |           1 |             |            |           | True    | VIP      | 1st    |
| 8   |          42 |             |            |           | True    | VIP      | 2nd    |
| 9   |             |             |            |           | True    | base     | 3rd    |

The first 5 columns can be found in `people.csv` too.
These columns are used to select different groups of people.
The columns are in priority order, meaning that if 2 selection rules
can be applied, then the one which has selection rules on the left
precedes the other rule.

The last 2 columns assign the conference hall and buffet to each group.
The values of hall and buffet has no particular meaning in this case.

From line 0 to 8 the rules are more and more specific, but the 9th is the most general
selection rule. (This shows that lines do not need to be in a priority order. The priority
order is defined by the order of the columns.)

Line 9 tells that if a person is a visitor, assign that person the hall "base"
and the buffet "3rd". Of course hall and buffet are assigned to visitors only,
so every other filtering criteria contains the same requirement for visitor.

Line 0, 1 and 2 tells that if a person is not only a visitor, but if their
favorite color is red green or blue, the hall "prim" is assigned to them, and
from buffet, the values "1st", "1st" and "2nd" are assigned, respectively.

Line 3 and 4 tells that those whose favorite color is red,
but are called Maria (as given name) or Smith (as family name),
will be directed to the hall "common" and to the buffet "1st" and "2nd", respectively.

Line 5 tells that all Smith Marias will be all in 1 special hall "famiglia", and will
eat in buffet "3rd".

Line 6, 7 and 8 tell that these people (if they are visitors), will be in the hall
"VIP", and will eat in different buffets.

The first few lines of the results are shown in the table below.

| personal ID | family name | given name | fav color | visitor | hall     | buffet |
| ----------: | :---------- | :--------- | :-------- | :------ | :------- | :----- |
|           0 | GARCIA      | Mohamed    | blue      | False   |          |        |
|           1 | SMITH       | Mohamed    | green     | True    | VIP      | 1st    |
|           2 | BROWN       | Wei        | magenta   | True    | base     | 3rd    |
|           3 | BROWN       | Jose       | yellow    | True    | base     | 3rd    |
|           4 | DAVIS       | Ahmed      | magenta   | True    | base     | 3rd    |
|           5 | MARTINEZ    | Nushi      | red       | False   |          |        |
|           6 | BROWN       | Muhammad   | yellow    | True    | base     | 3rd    |
|          27 | SMITH       | Ali        | blue      | True    | prim     | 2nd    |
|         333 | SMITH       | Maria      | red       | True    | famiglia | 3rd    |

- persons with personal ID 0 and 5 don't have assigned hall and buffet, because they don't match any criteria.
- the person with personal ID 1 is in the VIP hall, because selection rule 7 applies.
- persons with id 2,3,4 and 6 are selected based on the lowest priority selection rule, rule 9. They all go to the hall base.
- person with ID 27 is called Smith, but matches only rule 2.
- person with ID 333 matches rule 4 and 5 too, but because given name is on the left side of fav color, rule 5 has higher priority.
