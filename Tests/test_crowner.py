import unittest
from unittest.mock import Mock, patch
import pandas as pd
from crowner import KNN, Crowner, Mean, NormalDistribution
import os

from utils import CategoricalDataException, Logging


class TestCrowner(unittest.TestCase):
    def setUp(self):
        self.input_file = "iris_missing.csv"
        self.input_file_non_categorical = "iris_missing_noncategorical.csv"
        self.output_file = "crowner_test.csv"

    def test_crowner_mean_strategy_success(self):
        """
        Should fill missing values with mean
        """

        # Arrange
        logging_mock = Mock(Logging)
        column_name = "sepal.length"
        strategy = Mean()

        crowner = Crowner(strategy, column_name, logging_mock)
        df_before = pd.read_csv(self.input_file)

        count_nan = df_before[column_name].isna().sum()
        count_non_nan = df_before[column_name][
            df_before[column_name].isna() == False
        ].count()

        # Act

        crowner(self.input_file)
        count_nan_after = crowner._output[column_name].isna().sum()
        total = crowner._output[column_name].count()

        # Assert
        self.assertEqual(0, count_nan_after)
        self.assertEqual(total, count_nan + count_non_nan)

    def test_crowner_normal_distribution_strategy_success(self):
        """
        Should fill missing values with mean
        """

        # Arrange
        logging_mock = Mock(Logging)
        column_name = "sepal.length"
        strategy = NormalDistribution()

        crowner = Crowner(strategy, column_name, logging_mock)
        df_before = pd.read_csv(self.input_file)

        count_nan = df_before[column_name].isna().sum()
        count_non_nan = df_before[column_name][
            df_before[column_name].isna() == False
        ].count()

        # Act

        crowner(self.input_file)
        count_nan_after = crowner._output[column_name].isna().sum()
        total = crowner._output[column_name].count()

        # Assert
        self.assertEqual(0, count_nan_after)
        self.assertEqual(total, count_nan + count_non_nan)

    def test_crownerl_knn_strategy_should_raise_exception_if_csv_has_categorical_data(
        self,
    ):
        """
        Should fill missing values with mean
        """

        # Arrange
        logging_mock = Mock(Logging)
        column_name = "sepal.length"
        strategy = KNN()

        crowner = Crowner(strategy, column_name, logging_mock)
        # Act/Assert
        with self.assertRaises(CategoricalDataException) as e:
            crowner(self.input_file)

    def test_crowner_knn_strategy_success(self):
        """
        Should fill missing values with mean
        """

        # Arrange
        logging_mock = Mock(Logging)
        column_name = "sepal.length"
        strategy = KNN()

        crowner = Crowner(strategy, column_name, logging_mock)
        df_before = pd.read_csv(self.input_file_non_categorical)

        count_nan = df_before[column_name].isna().sum()
        count_non_nan = df_before[column_name][
            df_before[column_name].isna() == False
        ].count()

        # Act

        crowner(self.input_file_non_categorical)
        count_nan_after = crowner._output[column_name].isna().sum()
        total = crowner._output[column_name].count()

        # Assert
        self.assertEqual(0, count_nan_after)
        self.assertEqual(total, count_nan + count_non_nan)


if __name__ == "__main__":
    unittest.main()
