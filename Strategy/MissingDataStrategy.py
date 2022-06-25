from abc import ABC, abstractmethod
from multiprocessing.sharedctypes import Value
from numpy import NaN
import pandas as pd
import re

class IMissingDataStrategy(ABC):
    """
    Interface for implementing missing data mechanisms with strategy pattern
    """
    @abstractmethod
    def execute(self, attribute: pd.Series, missing_rate: float, query: str) -> None:
        pass


class MCAR(IMissingDataStrategy):
    """
    MCAR mechanism strategy
    """
    def execute(self, column: pd.Series, missing_rate: float, query: str) -> pd.Series:
        """
        Erase values from a series with MCAR pattern
        """
        print(f"Erasing values with MCAR pattern.\n Missing rate: {missing_rate}")
        return column.sample(frac=1-missing_rate)


class MAR(IMissingDataStrategy):
    """
    MAR mechanism strategy
    """
    def execute(self, column: pd.Series, missing_rate: float, query: str) -> pd.Series:
        """
        Erase values from a series with MAR pattern
        """
        raise NotImplementedError


class NMAR(IMissingDataStrategy):
    """
    NMAR mechanism strategy
    """
    def execute(self, column: pd.Series, missing_rate: float, query: str) -> pd.Series:
        """
        Erase values from 'column' with NMAR pattern, filtering column by 'query' at a rate of 'missing_rate'
        """
        df = pd.DataFrame({'x': column})
        trimmed_query = re.sub('[\s+]', '', query)

        try:
            filtered_df = df.query(f"{trimmed_query}")

        except:
            raise ValueError(f"Invalid query '{query}' for NMAR mechanism.")

        else:
            print(f"Erasing values with NMAR pattern.")
            print(f"Query: x in {column.name} where {query}")
            print(f"Missing rate: {missing_rate}")

            df.loc[filtered_df.sample(frac=missing_rate).index, 'x'] = NaN

            return df.x
