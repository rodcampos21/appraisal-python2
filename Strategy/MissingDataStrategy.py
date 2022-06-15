from abc import ABC, abstractmethod
from numpy import NaN
import pandas as pd

class IMissingDataStrategy(ABC):
    """
    Interface for implementing missing data mechanisms with strategy pattern
    """
    @abstractmethod
    def execute(self, attribute, missing_rate) -> None:
        pass


class MCAR(IMissingDataStrategy):
    """
    MCAR mechanism strategy
    """
    def execute(self, column: pd.Series, missing_rate: float) -> pd.Series:
        """
        Erase values from a series with MCAR pattern
        """
        print(f"Erasing values with MCAR pattern.\n Missing rate: {missing_rate}")
        return column.sample(frac=1-missing_rate)


class MAR(IMissingDataStrategy):
    """
    MAR mechanism strategy
    """
    def execute(self, column: pd.Series, missing_rate: float) -> pd.Series:
        """
        Erase values from a series with MAR pattern
        """
        raise NotImplementedError


class NMAR(IMissingDataStrategy):
    """
    NMAR mechanism strategy
    """

    def input_operator(self) -> str:
        """
        Input and validate an operator
        """
        operator = input("Type in one of the following operators: ==, >, >=, <, <=\n")

        if operator not in ["==", ">", ">=", "<", "<="]:
            raise ValueError(f"Invalid operator '{operator}'. Should be one of (==, >, >=, <, <=)")

        return operator

    def input_value(self) -> str:
        """
        Input and validate a value
        """
        value = input("Type in a value: ")
        try:
            return float(value)
        except:
            raise TypeError(f"Invalid value '{value}'. Should be a number.")


    def execute(self, column: pd.Series, missing_rate: float) -> pd.Series:
        """
        Erase values from a series with NMAR pattern
        """
        print("Choose a condition to apply NMAR pattern over the column\n")
        operator = self.input_operator()
        value = self.input_value()
        
        print(f"Erasing values with NMAR pattern.\n Condition: col_value {operator} {value} \n Missing rate: {missing_rate}")

        df = pd.DataFrame({'col': column})

        df.loc[df.query(f"col {operator} {value}").sample(frac=missing_rate).index, 'col'] = NaN

        return df.col
