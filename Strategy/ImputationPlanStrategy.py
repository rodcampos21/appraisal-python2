from abc import ABC, abstractmethod
from abc import ABC, abstractmethod
from utils import CategoricalDataException, Csv, Logging
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler


class IImputationPlanStrategy(ABC):
    """
    Abstract base class ImputationPlan.
    All imputation plans needs inherit from this base class.
    """

    @abstractmethod
    def execute(self, df: DataFrame, column_name: str, logger: Logging) -> None:
        pass


class Mean(IImputationPlanStrategy):
    """
    Implement a imputation plan strategy.
    """

    def execute(self, df: DataFrame, column_name: str, logger: Logging) -> DataFrame:
        """_summary_

        Args:
            df (DataFrame): An Pandas dataframe.
            column_name (str): A column name from the dataframe.

        Returns:
            DataFrame: Return the computed dataframe.
        """
        _mean = df[column_name].mean()
        df[column_name] = df[column_name].replace(np.nan, _mean)
        return df


class NormalDistribution(IImputationPlanStrategy):
    """
    Implement a imputation plan strategy.

    Compute the missing values, inserting random data from
    a normal distribution.
    """

    def execute(self, df: DataFrame, column_name: str, logger: Logging) -> DataFrame:
        """_summary_

        Args:
            df (DataFrame): An Pandas dataframe.
            column_name (str): A column name from the dataframe.

        Returns:
            DataFrame: Return the computed dataframe.
        """
        column_data = df[column_name]

        _not_missing_data = df[column_data.notnull()][column_name]

        missing_size = df[column_name].size - _not_missing_data.size

        mean = np.mean(_not_missing_data)
        std = np.std(_not_missing_data)

        r = np.random.normal(mean, std, missing_size)

        _loc = df[column_name].loc()
        _loc[df[column_name].isnull()] = r

        return df


class KNN(IImputationPlanStrategy):
    """
    Implement a imputation plan strategy.

    Compute the missing values, inserting random data with KNN.
    """

    def execute(self, df: DataFrame, column_name: str, logger: Logging) -> DataFrame:
        """_summary_

        Args:
            df (DataFrame): A Pandas dataframe.
            column_name (str): A column name from the dataframe.

        Returns:
            DataFrame: Return the computed dataframe.
        """
        try:
            scaler = MinMaxScaler()
            knn = KNNImputer(n_neighbors=5)

            df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
            df_knn = pd.DataFrame(
                knn.fit_transform(df_scaled), columns=df_scaled.columns
            )

            return df_knn

        except ValueError as e:
            raise CategoricalDataException(
                "csv contains categorical data, preprocess the dataset before."
            ) from e
