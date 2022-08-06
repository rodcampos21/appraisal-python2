from argparse import ArgumentParser
from typing import Optional, Union
from Strategy.ImputationPlanStrategy import IImputationPlanStrategy, KNN, Mean, NormalDistribution
from utils import Csv, Logging
import pandas as pd

class Crowner:

    def __init__(
        self,
        csv: Csv,
        column_name: str,
        strategy: IImputationPlanStrategy,
        debugger: Union[Logging, Optional[None]] = Logging(),
    ) -> None:
        self.csv = csv
        self.column_name = column_name
        self.strategy = strategy
        self.debugger = debugger
        self._result = None
        self._df = None

    def run(self) -> None:
        """
        Execute the Cronwer runner.
        """
        df = pd.read_csv(self.csv)
        self._df = df
        df_result = self.strategy.execute(df, self.column_name)
        self._result = df_result

    def save_result(self, name: Optional[str] = None) -> None:
        """_summary_

        Args:
            name (Optional[str], optional): _description_. Defaults to None.

        Raises:
            Exception: _description_
        """
        if self._result.empty:
            raise Exception("unhandled exception.")

        self._result.to_csv(name, index=False)

        print("Imputation of values succeeded.")
        print(f"File {name} successfully generated.")

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

    with Csv(input_file, "r") as csv:
        column_name = column_name
        crowner = Crowner(csv, column_name, strategy)
        crowner.run()
        crowner.save_result(output_file)


def main():
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_file", help="Name of the input file")
    parser.add_argument("-o", "--output_file", help="Name of the output file")
    parser.add_argument(
        "-a", "--attribute", help="Name of the column with erased values to fill."
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
