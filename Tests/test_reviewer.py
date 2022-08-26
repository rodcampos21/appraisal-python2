import unittest
from sklearn.metrics import mean_squared_error
from reviewer import Reviewer
from Strategy.MeasureStrategy import MSE, EUC, MAH, MAN
import pandas as pd
import scipy.spatial.distance as sp
import numpy as np


class test_reviewer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.original_file = pd.read_csv("iris.csv")
        cls.original_file_name = "iris.csv"
        cls.filled_file = pd.read_csv("Tests/iris_filled.csv")
        cls.filled_file_name="Tests/iris_filled.csv"

    def test_mse(cls):

        """Checks to see if the column returns the correct MSE value"""
        
        # Arrange
        expected_result = mean_squared_error(
            cls.filled_file[["sepal.length"]], cls.original_file[["sepal.length"]]
        )

        reviewer = Reviewer(MSE(), "sepal.length")

        # Act
        result = reviewer(
            cls.original_file_name, cls.filled_file_name
        )

        # Assert
        cls.assertAlmostEqual(result._output, expected_result)


    def test_euc(cls):

        """Checks to see if the column returns the correct Euclidian distance"""
        
        #  Arrange
        expected_result = sp.euclidean(
            cls.filled_file[["sepal.length"]], cls.original_file[["sepal.length"]]
        )

        reviewer = Reviewer(EUC(), "sepal.length")

        # Act
        result = reviewer(
            cls.original_file_name, cls.filled_file_name
        )

        # Assert
        cls.assertAlmostEqual(result._output, expected_result)


    def test_man(cls):

        """Checks to see if the column returns the correct Manhattan distance"""

        # Arrange
        expected_result = sp.cityblock(
            cls.filled_file[["sepal.length"]], cls.original_file[["sepal.length"]]
        )

        reviewer = Reviewer(MAN(), "sepal.length")

        # Act
        result = reviewer(
            cls.original_file_name, cls.filled_file_name
        )

        # Assert
        cls.assertAlmostEqual(result._output, expected_result)


    def test_mah(cls):

        """Checks to see if the column returns the correct Mahalanobis distance"""
        
        # Arrange

        reviewer = Reviewer(MAH(), "sepal.length")

        cov_mat = np.stack(
            (cls.original_file[["sepal.length"]], cls.filled_file[["sepal.length"]]),
            axis=1,
        ).squeeze()

        cov = np.cov(cov_mat)
        inv_cov = np.linalg.pinv(cov)
        
        expected_result = sp.mahalanobis(
            cls.original_file[["sepal.length"]],
            cls.filled_file[["sepal.length"]],
            inv_cov,
        )

        # Act
        result = reviewer(
            cls.original_file_name, cls.filled_file_name
        )

        # Arrange
        cls.assertAlmostEqual(result._output, expected_result)


if __name__ == "__main__":
    unittest.main()
