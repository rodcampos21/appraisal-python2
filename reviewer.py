from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from textwrap import fill
from Strategy.MeasureStrategy import IMeasureStrategy
import pandas as pd
from pipeline import Component
from utils import Csv, Logging, str_to_class

import pandas as pd
from pandas import DataFrame as _DataFrame

MEASURE_STRATEGY_MODULE = "Strategy.MeasureStrategy"


class Reviewer(Component):
    def __init__(self, strategy, column_name, logger=Logging()) -> None:
        super().__init__(strategy, column_name, logger=logger)
        self._kwargs.pop("missing_rate")
        self._kwargs.pop("query")

    def __call__(self, original_file: _DataFrame, filled_file: _DataFrame) -> object:

        if isinstance(filled_file, str):
            filled_file = pd.read_csv(filled_file)

        self._kwargs["filled_file"] = filled_file

        return super().__call__(original_file)


def main():
    """
    Main function
    """
    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-o", "--original_file", help="Name of the original file", required=True
    )
    parser.add_argument(
        "-f",
        "--filled_file",
        help="Name of the file with the input plan applied",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--measure",
        default="MSE",
        choices=("MSE", "EUC", "MIN", "MAN", "MAH"),
        help="Input measure to be used",
    )
    parser.add_argument(
        "-a", "--attribute", help="Name of the column to validate", required=True
    )
    args = vars(parser.parse_args())

    original_file = args["original_file"]
    filled_file = args["filled_file"]
    column = args["attribute"]
    mechanism = args["measure"]

    strategy = str_to_class(MEASURE_STRATEGY_MODULE, mechanism)
    reviewer = Reviewer(strategy, column)
    reviewer(original_file, filled_file)

    print("Measurenment succeeded")
    print("Measure:", float(f"{reviewer._output:.4f}"))


if __name__ == "__main__":
    main()
