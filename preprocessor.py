from typing import Optional, Union
from Strategy.PreprocessorStrategy import IPreprocessorStrategy
from pipeline import Component
from utils import Csv, Logging
import pandas as pd

PLAN_STRATEGY_MODULE = "Strategy.PreprocessorStrategy"


class Preprocessor(Component):
    def __init__(
        self,
        strategy: IPreprocessorStrategy,
        column_name: str = "",
        logger: Union[Logging, Optional[None]] = Logging(),
        **kwargs
    ) -> None:
        super().__init__(strategy, logger=logger, **kwargs)

        # remove unnecessary parameters for strategy
        self._kwargs.pop("missing_rate")
        self._kwargs.pop("query")
        self._kwargs.pop("column_name")
