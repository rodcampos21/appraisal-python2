from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import scipy.spatial.distance as sp
from sklearn.metrics import mean_squared_error

class IMeasureStrategy(ABC):
    """
    Interface for implementing validation algorithms for reviewe module
    """
    @abstractmethod
    def execute(self, original_column: pd.Series, column_filled: pd.Series) -> None:
        pass


class MSE(IMeasureStrategy):
    """
    Executes a Mean Squared Error validation using both columns
    Returns the MSE value
    """
    def execute(self, original_column: pd.Series, column_filled: pd.Series) -> float:

        return mean_squared_error(column_filled, original_column)


class EUC(IMeasureStrategy):
    """
    Executes an Euclidian distance validation using both columns
    Returns the EUC value
    """
    def execute(self, original_column: pd.Series, column_filled: pd.Series) -> float:

        return sp.euclidean(column_filled, original_column)


class MAN(IMeasureStrategy):
    """
    Executes a Manhattan distance validation using both columns
    Returns the MAN value
    """

    def execute(self, original_column: pd.Series, column_filled: pd.Series) -> float:

        return sp.cityblock(column_filled, original_column)


class MAH(IMeasureStrategy):
    """
    Executes a Malahanobis distance validation using both columns
    Returns the MAH value
    """

    def execute(self, original_column: pd.Series, column_filled: pd.Series) -> float:

        cov_mat = np.stack((original_column, column_filled), axis = 1).squeeze()
        cov = np.cov(cov_mat)
        inv_cov = np.linalg.pinv(cov)
        return sp.mahalanobis(column_filled, original_column, inv_cov)
