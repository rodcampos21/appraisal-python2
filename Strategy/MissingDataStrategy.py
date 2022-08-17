from abc import ABC, abstractmethod
from numpy import NaN
import pandas as pd
import re

from utils import Logging


class IMissingDataStrategy(ABC):
    """
    Interface for implementing missing data mechanisms with strategy pattern
    """

    @abstractmethod
    def execute(
        self,
        df: pd.Series,
        column_name: str,
        missing_rate: float,
        query: str,
        logger: Logging,
    ) -> None:
        pass


class MCAR(IMissingDataStrategy):
    """
    MCAR mechanism strategy
    """

    def execute(
        self,
        df: pd.Series,
        column_name: str,
        missing_rate: float,
        query: str,
        logger: Logging,
    ) -> pd.Series:
        """
        Erase values from a series with MCAR pattern
        """
        print(f"Erasing values with MCAR pattern.\n Missing rate: {missing_rate}")
        df[column_name] = df[column_name].sample(frac=1 - missing_rate)
        return df


class MAR(IMissingDataStrategy):
    """
    MAR mechanism strategy
    """

    def execute(
        self,
        df: pd.Series,
        column_name: str,
        missing_rate: float,
        query: str,
        logger: Logging,
    ) -> pd.Series:
        """
        Erase values from a series with MAR pattern
        """
        raise NotImplementedError


class NMAR(IMissingDataStrategy):
    """
    NMAR mechanism strategy
    """

    def execute(
        self,
        df: pd.Series,
        column_name: str,
        missing_rate: float,
        query: str,
        logger: Logging,
    ) -> pd.Series:
        """
        Erase values from 'column' with NMAR pattern, filtering column by 'query' at a rate of 'missing_rate'
        """
        aux = pd.DataFrame({"x": df[column_name]})
        trimmed_query = re.sub("[\s+]", "", query)

        try:
            filtered_df = aux.query(f"{trimmed_query}")

        except:
            raise ValueError(f"Invalid query '{query}' for NMAR mechanism.")

        else:
            print(f"Erasing values with NMAR pattern.")
            print(f"Query: x in {column_name} where {query}")
            print(f"Missing rate: {missing_rate}")

            aux.loc[filtered_df.sample(frac=missing_rate).index, "x"] = NaN

            df[column_name] = aux.x

            return df
