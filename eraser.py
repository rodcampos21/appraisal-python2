from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import pandas as pd
from Strategy.MissingDataStrategy import IMissingDataStrategy
from utils import missing_rate_float, str_to_class

MISSING_DATA_STRATEGY_MODULE = "Strategy.MissingDataStrategy"

class Eraser:
    strategy: IMissingDataStrategy

    def eraser(self, 
        input_file: str, 
        output_file: str, 
        attribute: str, 
        mechanism: str = "MCAR",
        missing_rate: float = 0.3,
        query: str = "", 
    ) -> None: 
        """
        Reads data from a csv 'input_file' and erase values from 'attribute' column using a missing data 'mechanism' at a 'missing_rate'
        Outputs the result to a csv 'output_file' file
        """
        self.strategy = str_to_class(MISSING_DATA_STRATEGY_MODULE, mechanism)
        data = pd.read_csv(input_file)
        data[attribute] = self.strategy.execute(data[attribute], missing_rate, query)
        data.to_csv(self.handle_output_file_name(output_file), index=False)
        print(f"File '{self.handle_output_file_name(output_file)}' successfully generated")
    
    def handle_output_file_name(self, output_file) -> str:
        """
        Checks the output_file extension. Adds '.csv' if not specified.
        """
        if ".csv" in output_file:
            return output_file
        else:
            return f"{output_file}.csv"

def main():
    """
    Main function
    """
    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--input_file", help="Name of the input file")
    parser.add_argument("-o", "--output_file", help="Name of the output file")
    parser.add_argument("-a", "--attribute", help="Name of the attribute to erase values")
    parser.add_argument("-m", "--mechanism", default="MCAR", choices=("MCAR", "MAR", "NMAR"), help="Missing data mechanism to be applied")
    parser.add_argument("-r", "--missing_rate", type=missing_rate_float, default=0.3, help="The rate in which the attribute values will be erased")
    parser.add_argument("-q", "--query", default="", help="The query to apply NMAR mechanism. A string as in the example 'x > 3 & x < 5 | x == 7', where x represents values in the chosen column. Valid tokens: x, ==, >, >=, <, <=, &, |, (, )")
    args = vars(parser.parse_args())

    input_file = args["input_file"]
    output_file = args["output_file"]
    attribute = args["attribute"]
    mechanism = args["mechanism"]
    missing_rate = args["missing_rate"]
    query = args["query"]

    eraser = Eraser()
    eraser.eraser(input_file, output_file, attribute, mechanism, missing_rate, query)

if __name__ == '__main__': 
    main()