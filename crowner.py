from abc import ABC, abstractmethod
from typing import Optional, Union
from .utils import Csv, Debugger


class AbstractImputationPlan(ABC):
    """
        Abstract base class ImputationPlan.
        All imputation plans needs inherit from this base class.
    """
    ...

    @abstractmethod
    def __run__(self):
        """"""
            Abstract
        """
        raise NotImplementedError()

class Mean(AbstractImputationPlan):
    """
        Implement a imputation plan strategy.
    """
    def strategy(self):
        ...


class Crowner:
    def __init__(
        self,
        csv: Csv,
        column_name: str,
        strategy: AbstractImputationPlan,
        debugger: Union[Debugger, Optional[None]] = Debugger,
    ) -> None:
        self.csv = csv
        self.column_name = column_name
        self.strategy = strategy
        self.debugger = debugger

    def run(self) -> None:
        raise NotImplementedError()

    def save_result(self, path: Optional[str], name: Optional[str]) -> None:
        raise NotImplementedError()
