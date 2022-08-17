from __future__ import annotations
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from typing import TYPE_CHECKING
from typing import Union


from pandas import DataFrame as _DataFrame
import pandas as pd

from utils import CategoricalDataException, Logging, missing_rate_float, str_to_class


class Pipeline:
    def __init__(self, logger=Logging()) -> None:
        self._logger = logger
        self._input = None
        self._output = None
        self._n = 0
        self._components = list()
        self._review_output = None

    def __repr__(self) -> str:
        return "[{}]".format(self.__class__.__name__)

    def __len__(self):
        return len(self._components)

    def __iter__(self):
        return self

    def __next__(self):
        if self._n < len(self):
            aux = self._components[self._n]
            self._n += 1
            return aux
        else:
            raise StopIteration()

    def add_component(self, component):
        self._components.append(component)
        return self

    def add_component_list(self, component_list: list):
        self._components.extend(component_list)
        return self

    def save(self, output) -> None:
        self._output.to_csv(output, index=False)
        self._logger.info(f"{self} File {output} successfully generated.")

    @property
    def output(self) -> None:
        return self._output

    @property
    def review_output(self) -> None:
        return self._review_output

    def __call__(self, input: _DataFrame) -> _DataFrame:
        self._logger.info("{} Starting pipeline...".format(self))
        aux = input

        try:
            for c in self:
                if c.__class__.__name__.upper() == "REVIEWER":
                    aux = c(input, aux)._output
                    self._review_output = aux
                else:
                    aux = c(aux)._output
                    self._output = aux
        except CategoricalDataException as e:
            self._logger.info("{} Input {}...".format(self, str(e)))
        except Exception as e:
            self._logger.info(
                "{} Unexpected error while processing the pipeline..., {}".format(
                    self, str(e)
                )
            )

        self._logger.info("{} Finishing pipeline...".format(self))

        return self


class Component:
    def __init__(
        self,
        strategy,
        column_name="",
        query=None,
        missing_rate=None,
        logger: Logging = Logging(),
    ):
        self._strategy = strategy
        self._logger = logger
        self._column_name = column_name
        self._query = query
        self._missing_rate = missing_rate
        self._output: _DataFrame = None

        self._kwargs = {
            "column_name": column_name,
            "missing_rate": missing_rate,
            "query": query,
            "logger": self._logger,
        }

    def __repr__(self) -> str:
        return "[{}-{}]".format(
            self.__class__.__name__, self._strategy.__class__.__name__
        )

    def save(self, output: str):
        """_summary_

        Args:
            name (Optional[str], optional): _description_. Defaults to None.

        Raises:
            Exception: _description_
        """
        if self._output.empty:
            raise Exception("unhandled exception.")

        self._output.to_csv(output, index=False)

        self._logger.info(f"{self} File {output} successfully generated.")

    def __call__(self, input: _DataFrame) -> object:
        self._input = input
        if isinstance(input, str):
            self._logger.info(
                "{} Input is a string, going to read as csv.".format(self)
            )
            self._input = pd.read_csv(input)

        self._logger.info("{} Starting strategy.".format(self))
        self._output = self._strategy.execute(self._input, **self._kwargs)
        self._logger.info("{} strategy worked successfully.".format(self))

        return self


class ComponentBuilder:
    def __init__(self, Component) -> None:
        self.Component = Component
        self._kwargs = dict()

    def strategy(self, strategy):
        self._kwargs["strategy"] = strategy
        return self

    def column_name(self, column_name: str):
        self._kwargs["column_name"] = column_name
        return self

    def query(self, query: str):
        self._kwargs["query"] = query
        return self

    def missing_rate(self, missing_rate: float):
        self._kwargs["missing_rate"] = missing_rate
        return self

    def build(self) -> object:
        return self.Component(**self._kwargs)


def main():
    """
    Main function
    """
    # local import to not interfere in global imports::
    from eraser import Eraser, MISSING_DATA_STRATEGY_MODULE
    from crowner import Crowner, PLAN_STRATEGY_MODULE
    from reviewer import Reviewer, MEASURE_STRATEGY_MODULE

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
    parser.add_argument(
        "-em",
        "--eraser-mechanism",
        default="MCAR",
        choices=("MCAR", "MAR", "NMAR"),
        help="Missing data mechanism to be applied",
    )
    parser.add_argument(
        "-cp",
        "--crowner-plan",
        default="Mean",
        choices=("Mean", "nd", "NormalDistribution", "KNN"),
        help="imputation plan to be used. The default value of this is mean",
    )
    parser.add_argument(
        "-rm",
        "--reviewer-measure",
        default="MSE",
        choices=("MSE", "EUC", "MIN", "MAN", "MAH"),
        help="Input measure to be used",
    )
    args = vars(parser.parse_args())

    input_file = args["input_file"]
    output_file = args["output_file"]
    attribute = args["attribute"]
    missing_rate = args["missing_rate"]
    query = args["query"]
    eraser_mechanism = args["eraser_mechanism"]
    crowner_plan = args["crowner_plan"]

    if crowner_plan == "nd":
        crowner_plan = "NormalDistribution"

    reviewer_measure = args["reviewer_measure"]

    eraser_strategy = str_to_class(MISSING_DATA_STRATEGY_MODULE, eraser_mechanism)
    crowner_strategy = str_to_class(PLAN_STRATEGY_MODULE, crowner_plan)
    reviewer_strategy = str_to_class(MEASURE_STRATEGY_MODULE, reviewer_measure)

    p = (
        Pipeline()
        .add_component(
            ComponentBuilder(Eraser)
            .column_name(attribute)
            .missing_rate(missing_rate)
            .strategy(eraser_strategy)
            .build()
        )
        .add_component(
            ComponentBuilder(Crowner)
            .column_name(attribute)
            .strategy(crowner_strategy)
            .build()
        )
        .add_component(
            ComponentBuilder(Reviewer)
            .column_name(attribute)
            .strategy(reviewer_strategy)
            .build()
        )
    )(input_file)

    p.save(output_file)
    # python3 pipeline.py -i bla.csv -o wtf.csv -a sepal.length -em MCAR -cp mean -rm MSE


if __name__ == "__main__":
    main()
