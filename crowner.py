from argparse import ArgumentParser
from typing import Optional, Union
from Strategy.ImputationPlanStrategy import (
    IImputationPlanStrategy,
    KNN,
    Mean,
    NormalDistribution,
)
from pipeline import Component
from utils import Csv, Logging
import pandas as pd


class Crowner(Component):
    def __init__(
        self,
        strategy: IImputationPlanStrategy,
        column_name: str,
        logger: Union[Logging, Optional[None]] = Logging(),
    ) -> None:
        super().__init__(strategy, column_name, logger=logger)

        # remove unnecessary parameters for strategy
        self._kwargs.pop("missing_rate")
        self._kwargs.pop("query")


def crowner(input_file, output_file, column_name, plan):
    """_summary_

    Args:
        input_file (_type_): input file
        output_file (_type_): output file
        column_name (_type_): column name to be filled.
        plan (_type_): plan to be used.

    Raises:
        Exception: _description_
    """

    strategy = None

    plan = plan.lower()

    if plan == "mean":
        strategy = Mean()
    elif plan in ["nd", "normal_distribution"]:
        strategy = NormalDistribution()
    elif plan in ["knn"]:
        strategy = KNN()
    else:
        raise Exception("")

    crowner = Crowner(strategy, column_name)
    crowner(input_file)
    crowner.save(output_file)


def main():
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_file", help="Name of the input file")
    parser.add_argument("-o", "--output_file", help="Name of the output file")
    parser.add_argument(
        "-a",
        "--attribute",
        help="Name of the column with erased values to fill.",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--plan",
        default="mean",
        help="imputation plan to be used. The default value of this is mean",
    )
    args = vars(parser.parse_args())

    input_file = args["input_file"]
    output_file = args["output_file"]
    attribute = args["attribute"]
    plan = args["plan"]
    crowner(input_file, output_file, attribute, plan)


if __name__ == "__main__":
    main()
