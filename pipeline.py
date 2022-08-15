from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from crowner import Crowner
    from eraser import Eraser
    from reviewer import Reviewer

from pandas import DataFrame as _DataFrame
import pandas as pd


from Strategy.ImputationPlanStrategy import IImputationPlanStrategy, Mean
from Strategy.MeasureStrategy import IMeasureStrategy
from Strategy.MissingDataStrategy import IMissingDataStrategy
from utils import Logging


class Pipeline:
    def __init__(self, *args, **kwargs) -> None:
        self._logger = None
        self._input = None
        self._output = None

        self._components = set()

    def config(self) -> object:
        ...

    def input(self) -> object:
        ...

    def save(self) -> None:
        ...

    def output(self) -> None:
        ...

    def __call__(self) -> _DataFrame:
        ...


class Component:
    def __init__(
        self, strategy, column_name, query=None, missing_rate=None, logger=None
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
        }

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

        print("Imputation of values succeeded.")
        print(f"File {output} successfully generated.")

    def __call__(self, input: _DataFrame) -> object:
        self._input = input
        if isinstance(input, str):
            self._input = pd.read_csv(input)

        self._output = self._strategy.execute(self._input, **self._kwargs)


class PipelineComponentBuilder:
    def __init__(self, Component) -> None:
        self.Componet = Component
        self._kwargs = dict()

    def strategy(self, strategy):
        self._kwargs["strategy"] = strategy
        return self

    def column_name(self, column_name: str):
        self._kwargs["column_name"] = column_name
        return self

    def query(self, query: str):
        if isinstance(self.Component, Eraser):
            self._kwargs["query"] = query
        else:
            raise TypeError("Query cannot be used with {} type".format(self.Componet))

        return self

    def missing_rate(self, missing_rate: float):
        if isinstance(self.Component, Eraser):
            self._kwargs["missing_rate"] = missing_rate
        else:
            raise TypeError(
                "missing rate cannot be used with {} type".format(self.Componet)
            )
        return self

    def __call__(self) -> object:
        return self.Componet(**self._kwargs)

    def __init__(
        self,
        component_class: Union[Eraser, Crowner, Reviewer],
        strategy: Union[
            IImputationPlanStrategy, IMeasureStrategy, IMissingDataStrategy
        ],
        data: dict,
    ):
        self._component_class = component_class
        self._strategy = strategy
        self._data = data
        self.input: _DataFrame = None
        self.output: _DataFrame = None

    def __call__(self, pipeline_input: Union[str, _DataFrame], logger) -> object:
        self.input = pipeline_input

        self.output = self._component_class(
            input=input, strategy=self._strategy, logger=logger, **self._data
        )
        return self


if __name__ == "__main__":
    p = PipelineComponent(Crowner, Mean, {"column_name": "iris_missing"})
    csv = pd.read_csv("iris_missing.csv")
    print(p(csv, Logging()))
