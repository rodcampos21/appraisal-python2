""" For me (Leonardo) to be able to use reviewer locally
    Change path as needed """
import sys
sys.path.insert(0, '/Users/super/Desktop/Projeto_Appraisal') 
"""  """

import unittest
from sklearn.metrics import mean_squared_error
from reviewer import reviewer, reviewer_euc, reviewer_mah, reviewer_man, reviewer_min, reviewer_mse
import pandas as pd
import scipy.spatial.distance as sp
import numpy as np

class test_reviewer(unittest.TestCase):
    """  (for the sake of testing, the iris_filled file has been created already with the crowner)  """

    @classmethod
    def setUpClass(cls):
        cls.original_file = pd.read_csv("iris.csv")
        cls.filled_file = pd.read_csv("iris_filled.csv")

    def test_mse(cls):

        """ Checks to see if the column returns the correct MSE value
         """
         
        result = reviewer_mse(cls.original_file[['sepal.length']], cls.filled_file[['sepal.length']])
        expected_result = mean_squared_error(cls.filled_file[['sepal.length']], cls.original_file[['sepal.length']])
        cls.assertEqual(result, expected_result)

    def test_euc(cls):

        """ Checks to see if the column returns the correct Euclidian distance
         """
         
        result = reviewer_euc(cls.original_file[['sepal.length']], cls.filled_file[['sepal.length']])
        expected_result = sp.euclidean(cls.filled_file[['sepal.length']], cls.original_file[['sepal.length']])
        cls.assertEqual(result, expected_result)

    def test_min(cls):

        """ Checks to see if the column returns the correct Minkowski distance
         """
         
        result = reviewer_min(cls.original_file[['sepal.length']], cls.filled_file[['sepal.length']])
        expected_result = sp.minkowski(cls.filled_file[['sepal.length']], cls.original_file[['sepal.length']])
        cls.assertEqual(result, expected_result)

    def test_man(cls):

        """ Checks to see if the column returns the correct Manhattan distance
         """
         
        result = reviewer_man(cls.original_file[['sepal.length']], cls.filled_file[['sepal.length']])
        expected_result = sp.cityblock(cls.filled_file[['sepal.length']], cls.original_file[['sepal.length']])
        cls.assertEqual(result, expected_result)

    def test_mah(cls):

        """ Checks to see if the column returns the correct Mahalanobis distance
         """
         
        result = reviewer_mah(cls.original_file[['sepal.length']], cls.filled_file[['sepal.length']])
        cov_mat = np.stack((cls.original_file[['sepal.length']], cls.filled_file[['sepal.length']]), axis = 1).squeeze()
        cov = np.cov(cov_mat)
        inv_cov = np.linalg.pinv(cov)
        expected_result = sp.mahalanobis(cls.original_file[['sepal.length']], cls.filled_file[['sepal.length']], inv_cov)
        cls.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()