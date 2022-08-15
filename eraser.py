from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import pandas as pd
from Strategy.MissingDataStrategy import IMissingDataStrategy
from pipeline import Component
from utils import Logging, missing_rate_float, str_to_class

MISSING_DATA_STRATEGY_MODULE = "Strategy.MissingDataStrategy"


class Eraser(Component):

    strategy: IMissingDataStrategy

    def __init__(
        self, strategy, column_name, missing_rate, query=None, logger=Logging()
    ) -> None:
        print(query)
        super().__init__(
            strategy,
            column_name,
            query=query,
            missing_rate=missing_rate,
            logger=logger,
        )


def main():
    """
    Main function
    """
    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "-i", "--input_file", help="Name of the input file", required=True
    )
    parser.add_argument(
        "-o", "--output_file", help="Name of the output file", required=True
    )
    parser.add_argument(
        "-a", "--attribute", help="Name of the attribute to erase values", required=True
    )
    parser.add_argument(
        "-m",
        "--mechanism",
        default="MCAR",
        choices=("MCAR", "MAR", "NMAR"),
        help="Missing data mechanism to be applied",
    )
    parser.add_argument(
        "-r",
        "--missing_rate",
        type=missing_rate_float,
        default=0.3,
        help="The rate in which the attribute values will be erased",
    )
    parser.add_argument(
        "-q",
        "--query",
        default="",
        help="The query to apply NMAR mechanism. A string as in the example 'x > 3 & x < 5 | x == 7', where x represents values in the chosen column. Valid tokens: x, ==, >, >=, <, <=, &, |, (, )",
    )
    args = vars(parser.parse_args())

    input_file = args["input_file"]
    output_file = args["output_file"]
    attribute = args["attribute"]
    mechanism = args["mechanism"]
    missing_rate = args["missing_rate"]
    query = args["query"]

    strategy = str_to_class(MISSING_DATA_STRATEGY_MODULE, mechanism)
    eraser = Eraser(strategy, attribute, query, missing_rate)
    eraser(input_file)
    eraser.save(output_file)


if __name__ == "__main__":
    main()
