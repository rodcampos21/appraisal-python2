from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from sklearn.metrics import mean_squared_error
import pandas as pd

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--original_file", help="Name of the original file")
parser.add_argument("-f", "--filled_file", help="Name of the file with the input plan applied")
parser.add_argument("-m", "--measure", default="MSE", choices=("MSE"), help="Input measure to be used")
parser.add_argument("-a", "--attribute", help="Name of the column to validate")
args = vars(parser.parse_args())

def reviewer_mse(column_original, column_filled):
    """
    Executes a Mean Squared Error validation using both columns
    Returns the MSE value
    """
    return mean_squared_error(column_filled, column_original)

def execute_validation_mechanism(mechanism, column_original, column_filled):
    """
    Chooses the validation mechanism function to execute base on the input
    Takes both columns to apply the mechanism to
    Returns a call to the mechanism function
    """
    if (mechanism == "MSE"):
        return reviewer_mse(column_original, column_filled)
    elif (mechanism == "other"):
        pass

def reviewer(original_file, filled_file, column, mechanism):
    """
    Reads data from two csv's, 'original_file' and 'filled_file', and calculates validates the values from a selected 'column'
    Based on a mechanism specified by the user
    Outputs the result as a print to the console
    """
    original = pd.read_csv(original_file)
    filled = pd.read_csv(filled_file)
    result = execute_validation_mechanism(mechanism, original[column], filled[column])
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
