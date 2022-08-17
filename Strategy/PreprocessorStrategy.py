from abc import ABC, abstractmethod
import pandas as pd

from utils import Csv, Logging


class IPreprocessorStrategy(ABC):
    """
    Abstract base class ImputationPlan.
    All imputation plans needs inherit from this base class.
    """

    @abstractmethod
    def execute(self, df: pd.DataFrame, logger: Logging) -> None:
        pass


class CategoricalDataStrategy(IPreprocessorStrategy):
    """
    Categorical data strategy, try to remove categorical data.
    """

    def execute(self, df: pd.DataFrame, logger: Logging) -> pd.DataFrame:
        """_summary_

        Args:
            df (DataFrame): An Pandas dataframe.
            column_name (str): A column name from the dataframe.

        Returns:
            DataFrame: Return the computed dataframe.
        """
        size = len(df.columns)
        aux = []
        for i in df.columns:
            if type(df[i][0]) == str:
                aux.append(i)
        variables = df[aux]
        dummies = pd.get_dummies(variables, drop_first=True)

        print(dummies.head())

        df = df.drop(aux, axis=1)
        df = pd.concat([df, dummies], axis=1)

        return df
