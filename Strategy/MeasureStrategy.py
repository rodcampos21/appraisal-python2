from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import scipy.spatial.distance as sp
from sklearn.metrics import mean_squared_error

from utils import Logging


class IMeasureStrategy(ABC):
    """
    Interface for implementing validation algorithms for reviewe module
    """

    @abstractmethod
    def execute(
        self,
        original_file: pd.Series,
        filled_file: pd.Series,
        column_name: str,
        logger: Logging,
    ) -> None:
        pass


class MSE(IMeasureStrategy):
    """
    Executes a Mean Squared Error validation using both columns
    Returns the MSE value
    """

    def execute(
        self,
        original_file: pd.Series,
        filled_file: pd.Series,
        column_name: str,
        logger: Logging,
    ) -> float:

        return mean_squared_error(filled_file[column_name], original_file[column_name])


class EUC(IMeasureStrategy):
    """
    Executes an Euclidian distance validation using both columns
    Returns the EUC value
    """

    def execute(
        self,
        original_file: pd.Series,
        filled_file: pd.Series,
        column_name: str,
        logger: Logging,
    ) -> float:

        return sp.euclidean(filled_file[column_name], original_file[column_name])


class MAN(IMeasureStrategy):
    """
    Executes a Manhattan distance validation using both columns
    Returns the MAN value
    """

    def execute(
        self,
        original_file: pd.Series,
        filled_file: pd.Series,
        column_name: str,
        logger: Logging,
    ) -> float:

        return sp.cityblock(filled_file[column_name], original_file[column_name])


class MAH(IMeasureStrategy):
    """
    Executes a Malahanobis distance validation using both columns
    Returns the MAH value
    """

    def execute(
        self,
        original_file: pd.Series,
        filled_file: pd.Series,
        column_name: str,
        logger: Logging,
    ) -> float:

        cov_mat = np.stack(
            (original_file[column_name], filled_file[column_name]), axis=1
        ).squeeze()
        cov = np.cov(cov_mat)
        inv_cov = np.linalg.pinv(cov)
        return sp.mahalanobis(
            filled_file[column_name], original_file[column_name], inv_cov
        )
