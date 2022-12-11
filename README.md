## Objective

The objective of this work is the portability of the appraisal system to the Python language and, in addition, to provide a tool that supports this system, in other words, to develop a framework.

## [](https://github.com/leomath42/appraisal#o-que-%C3%A9-o-appraisal-)What is Appraisal?

**Appraisal** is a system for imputing missing data in tabular datasets in AM (Machine Learning) projects and this system can also generate and validate new values for this missing data based on different approaches.

## Installation

We recommend installing the dependencies and running the application in a virtual environment

    $ pip install virtualenv
    $ virtualenv venv
    $ . venv/bin/activate

Installation of dependencies:

    $ pip install -r requirements.txt

## Modules

### Eraser

Module responsible for erasing values from a given column of the provided dataset.

Syntax:

    python eraser.py -i <ifile> -o <ofile> -m <mech> -a <att> -r <missing_rate>

In the syntax above:

- **ifile**: input file name, in csv format.
- **ofile**: output file name, in csv format.
- **att**: attribute name on which simulate missing values.
- **mech**: absence mechanism to be applied. Possible mechanisms  (all described in this  [document](https://eic.cefet-rj.br/~jsoares/wp-content/uploads/2021/03/Imputac%CC%A7a%CC%83o-Hot-Deck-Uma-Revisa%CC%83o-Sistema%CC%81tica-da-Literatura-versa%CC%83o-final.pdf)) are:

  - "**MCAR**" (Missing Completely At Random)

  - "**MAR**" (Missing At Random)

  - "**NMAR**" (Not Missing At Random)

- **missing_rate**: value between 0 and 1, which defines the rate of missing values to be produced.

An example of a Eraser module call is : 

    python eraser.py -i iris.csv -o iris_missing.csv -m MCAR -a sepal.length -r .3

In case the mechanism chosen is NMAR, an additional query parameter must be included, which receives an expression to filter the 'x' values of the column of the chosen attribute. Accepted Tokens: x, ==, >, >=, <, <=, &, |, (,).

An example of usage for this case is :

    python eraser.py -i iris.csv -o iris_missing.csv -m NMAR -a "sepal.length" -r .7 -q "x >= 1 | x<=6"

### Crowner

Module responsible for imputing data in a column.

Syntax:

    python crowner.py -i <ifile> -o <ofile> -p <plan> -a <att>

In the syntax above:

- **ifile**: input file name, in csv format.
- **ofile**: output file name, in csv format.
- **att**:  attribute name on which  fill in missing values.
- **plan**: imputation plan to be used. The default value of this argument should be "mean", which means that missing values must be filled in with the average of the existing values. 

A call example of the Crowner Module is : 

    python crowner.py -i iris_missing.csv -o iris_filled.csv -p mean -a sepal.length

### Reviewer

Module responsible for measuring the relative error between the original data and the imputed data.

Syntax:

    python reviewer.py -o <ofile> -f <ffile> -m <measure> -a <att>

In the syntax above:

- **ofile**: name of the original file, without missing data, in csv format.
- **ffile**: name of the file resulting from the execution of an imputation plan (using the Crowner module), in csv format.
- **att**: name of the attribute on which to compare.
- **measure**: measure: error metric to be used. 

An example of a Reviewer Module call is: 

    python reviewer.py -o iris.csv -f iris_filled.csv -m MSE -a sepal.length

### Pipeline 

Module responsible for managing the appraisal pipeline, using all other modules as components.

Syntax:

    python pipeline.py -i <ifile> -o <ofile> -a <att> -r <missing_rate> -q <query> -em <eraser_mech> -cp <crowner_plan> -rm <reviwer_measure> 


In the syntax above:

- **ofile**: name of the original file, without missing data, in csv format.
- **ffile**:: name of the file resulting from the execution of an imputation plan (using the Crowner module), in csv format.
- **att**: name of the attribute on which to compare.
- **missing_rate**: value between 0 and 1, which defines the rate of missing values to be produced.
- **query**: query to be used in the eraser module (Optional, only used in some strategies).
- **eraser_mech**: absence mechanism to be applied.
- **crowner_plan**: imputation plan to use. The default value of this argument should be "mean", which means that missing values must be filled in with the average of the existing values.
- **reviwer_measure**: error metric to use.

An example of a Pipeline module call is:

python3 pipeline.py -i iris_non_categorical.csv -o test.csv -a "sepal.length" -q "x>= 1 | x<=6" -r .3 -em NMAR -cp KNN -rm MSE


### Unitary tests

Unit test modules are grouped in the 'Tests' folder.

An example of running the unit tests of a module:


    python -m unittest Tests/test_eraser.py

To run all unit tests:

    python -m unittest discover Tests