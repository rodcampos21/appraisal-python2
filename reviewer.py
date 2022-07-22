from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import scipy.spatial.distance as sp

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--original_file", help="Name of the original file")
parser.add_argument("-f", "--filled_file", help="Name of the file with the input plan applied")
parser.add_argument("-m", "--measure", default="MSE", choices=("MSE", "EUC", "MIN", "MAN", "MAH"), help="Input measure to be used")
parser.add_argument("-a", "--attribute", help="Name of the column to validate")
args = vars(parser.parse_args())

def reviewer_mse(column_original, column_filled):
    """
    Executes a Mean Squared Error validation using both columns
    Returns the MSE value
    """
    return mean_squared_error(column_filled, column_original)

def reviewer_euc(column_original, column_filled):
    """
    Executes an Euclidian distance validation using both columns
    Returns the EUC value
    """
    return sp.euclidean(column_filled, column_original)

def reviewer_min(column_original, column_filled):
    """
    Executes a Minkowski distance validation using both columns
    Returns the MIN value
    """
    return sp.minkowski(column_filled, column_original, p=2)

def reviewer_man(column_original, column_filled):
    """
    Executes a Manhattan distance validation using both columns
    Returns the MAN value
    """
    return sp.cityblock(column_filled, column_original)

def reviewer_mah(column_original, column_filled, cov = None):
    """
    Executes a Malahanobis distance validation using both columns
    Returns the MAH value
    """
    cov_mat = np.stack((column_original, column_filled), axis = 1).squeeze()
    cov = np.cov(cov_mat)
    inv_cov = np.linalg.pinv(cov)
    return sp.mahalanobis(column_filled, column_original, inv_cov)

def execute_validation_mechanism(mechanism, column_original, column_filled):
    """
    Chooses the validation mechanism function to execute base on the input
    Takes both columns to apply the mechanism to
    Returns a call to the mechanism function
    """
    if (mechanism == "MSE"):
        return reviewer_mse(column_original, column_filled)
    elif (mechanism == "EUC"):
        return reviewer_euc(column_original, column_filled)
    elif (mechanism == "MIN"):
        return reviewer_min(column_original, column_filled)
    elif (mechanism == "MAN"):
        return reviewer_man(column_original, column_filled)
    elif (mechanism == "MAH"):
        return reviewer_mah(column_original, column_filled)

def reviewer(original_file, filled_file, column, mechanism):
    """
    Reads data from two csv's, 'original_file' and 'filled_file', and calculates validates the values from a selected 'column'
    Based on a mechanism specified by the user
    Outputs the result as a print to the console
    """
    original = pd.read_csv(original_file)
    filled = pd.read_csv(filled_file)
    result = execute_validation_mechanism(mechanism, original[[column]], filled[[column]])
    print('Measure:', float(f'{result:.4f}'))

def main():
    """
    Main function
    """
    original_file = args["original_file"]
    filled_file = args["filled_file"]
    column = args["attribute"]
    mechanism = args["measure"]
    reviewer(original_file, filled_file, column, mechanism) 

if __name__ == '__main__': 
    main()
