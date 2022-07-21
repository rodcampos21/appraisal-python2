import unittest
from unittest.mock import patch
import pandas as pd
from eraser import Eraser
import os


class TestEraserMCAR(unittest.TestCase):

    def setUp(self):
        self.input_file = "iris.csv"
        self.output_file = "iris_missing.csv"


    def tearDown(self):
        if os.path.exists("iris_missing.csv"):
            os.remove("iris_missing.csv")


    def test_eraser_mcar_success_case(self):
        """
            Should erase values from column 'attribute' with the expected 'missing rate' passed in the input
        """
        # Arrange
        input_file = self.input_file
        output_file = self.output_file
        attribute = "sepal.length"
        mechanism = "MCAR"
        missing_rate = 0.3

        original_csv = pd.read_csv(input_file)
        original_column = original_csv[attribute]
        number_of_non_null_values_original_column = original_column.count()

        # Act
        eraser = Eraser()
        eraser.eraser(input_file, output_file, attribute, mechanism, missing_rate)

        # Assert
        new_csv = pd.read_csv(output_file)
        new_column = new_csv[attribute]
        number_of_non_null_values_new_column = new_column.count()

        rate_of_erased_values = 1 - number_of_non_null_values_new_column / number_of_non_null_values_original_column
        
        self.assertAlmostEqual(rate_of_erased_values, missing_rate)


    def test_eraser_mcar_error_reading_column(self):
        """
            Should raise exception if a column that does not exist in the csv is passed 
            in the 'attribute' parameter
        """
        # Arrange
        input_file = self.input_file
        output_file = self.output_file
        attribute = "FAKE_COLUMN"
        mechanism = "MCAR"
        missing_rate = 0.3

        # Act
        eraser = Eraser()

        with self.assertRaises(KeyError):
            eraser.eraser(input_file, output_file, attribute, mechanism, missing_rate)


class TestEraserNMAR(unittest.TestCase):
    def setUp(self):
        self.input_file = "iris.csv"
        self.output_file = "iris_missing.csv"

    def tearDown(self):
        if os.path.exists("iris_missing.csv"):
            os.remove("iris_missing.csv")

    def test_eraser_nmar_success_case(self):
        """
            Should erase values that satisfy the argument 'query' from column 'attribute' 
            with the expected 'missing rate' passed in the input
        """
        # Arrange
        input_file = self.input_file
        output_file = self.output_file
        attribute = "sepal.length"
        mechanism = "NMAR"
        missing_rate = 0.3
        query = "x > 3"

        original_csv = pd.read_csv(input_file)
        number_of_values_that_satisfy_query_original_column = len(original_csv[original_csv[attribute] > 3])

        # Act
        eraser = Eraser()
        eraser.eraser(input_file, output_file, attribute, mechanism, missing_rate, query)

        # Assert
        new_csv = pd.read_csv(output_file)
        number_of_values_that_satisfy_query_new_column =  len(new_csv[new_csv[attribute] > 3])

        rate_of_erased_values = 1 - number_of_values_that_satisfy_query_new_column / number_of_values_that_satisfy_query_original_column
        
        self.assertAlmostEqual(rate_of_erased_values, missing_rate)

    def test_eraser_nmar_error_invalid_query(self):
        """
            Should raise exception if the query provided to NMAR is invalid
        """
        # Arrange
        input_file = self.input_file
        output_file = self.output_file
        attribute = "sepal.length"
        mechanism = "NMAR"
        missing_rate = 0.3
        query = "INVALID_QUERY"

        # Act
        eraser = Eraser()

        with self.assertRaises(ValueError):
            eraser.eraser(input_file, output_file, attribute, mechanism, missing_rate, query)

        

if __name__ == '__main__':
    unittest.main()