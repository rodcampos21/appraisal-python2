from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, ArgumentTypeError
import pandas as pd

def missing_rate_float(x):
    """
    Custom type function for validating the "missing_range" argument
    """
    try:
        x = float(x)
    except ValueError:
        raise ArgumentTypeError("%r not a floating-point literal" % (x,))

    if x < 0.0 or x > 1.0:
        raise ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

# Parse command line arguments
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--input_file", help="Name of the input file")
parser.add_argument("-o", "--output_file", help="Name of the output file")
parser.add_argument("-a", "--attribute", help="Name of the column to erase values")
parser.add_argument("-m", "--mechanism", default="MCAR", choices=("MCAR", "MAR", "NMAR"), help="Missing data mechanism to be applied")
parser.add_argument("-r", "--missing_rate", type=missing_rate_float, default=0.3, help="The rate in which the column values will be erased")
args = vars(parser.parse_args())

def erase_mcar(column, missing_rate):
    """
    Erase values from a dataframe column using 'MCAR' mechanism
    Takes a dataframe column and the missing rate as parameters
    Returns the column with values randomly replaced by NaN at the missing rate 
    """
    return column.sample(frac=1-missing_rate)

def execute_missing_data_mechanism(mechanism, column, missing_rate):
    """
    Chooses the missing data mechanism function to execute based on the input
    Takes the missing data mechanism, the column to apply the mechanism and the missing rate.
    Returns a call to the mechanism function
    """
    if (mechanism == "MCAR"):
        return erase_mcar(column, missing_rate)
    elif (mechanism == "MAR"):
        pass
    elif (mechanism == "NMAR"):
        pass

def handle_output_file_name(output_file):
    """
    Checks the output_file extension. Adds '.csv' if not specified.
    """
    if ".csv" in output_file:
        return output_file
    else:
        return f"{output_file}.csv"

def eraser(input_file, output_file, column, mechanism, missing_rate):
    """
    Reads data from a csv 'input_file' and erase values from 'column' using a missing data 'mechanism' at a 'missing_rate'
    Outputs the result to a csv 'output_file' file
    """
    data = pd.read_csv(input_file)
    data[column] = execute_missing_data_mechanism(mechanism, data[column], missing_rate)
    data.to_csv(handle_output_file_name(output_file), index=False)

def main():
    """
    Main function
    """
    input_file = args["input_file"]
    output_file = args["output_file"]
    column = args["attribute"]
    mechanism = args["mechanism"]
    missing_rate = args["missing_rate"]
    eraser(input_file, output_file, column, mechanism, missing_rate) 

if __name__ == '__main__': 
    main()
