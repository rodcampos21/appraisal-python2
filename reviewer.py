from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from Strategy.MeasureStrategy import IMeasureStrategy
import pandas as pd
from utils import Csv, str_to_class

MEASURE_STRATEGY_MODULE = "Strategy.MeasureStrategy"

class Reviewer:
    strategy: IMeasureStrategy

    def reviewer(self, 
        original_file: Csv, 
        filled_file: Csv, 
        column: pd.DataFrame, 
        mechanism: str = "MSE"
    ) -> None: 
        """
        Reads data from a csv 'input_file' and erase values from 'attribute' column using a missing data 'mechanism' at a 'missing_rate'
        Outputs the result to a csv 'output_file' file
        """
        self.strategy = str_to_class(MEASURE_STRATEGY_MODULE, mechanism)
        original = pd.read_csv(original_file)
        filled = pd.read_csv(filled_file)
        result = self.strategy.execute(original[[column]], filled[[column]])
        print('Measurenment succeeded')
        print('Measure:', float(f'{result:.4f}'))


def main():
    """
    Main function
    """
    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-o", "--original_file", help="Name of the original file")
    parser.add_argument("-f", "--filled_file", help="Name of the file with the input plan applied")
    parser.add_argument("-m", "--measure", default="MSE", choices=("MSE", "EUC", "MIN", "MAN", "MAH"), help="Input measure to be used")
    parser.add_argument("-a", "--attribute", help="Name of the column to validate")
    args = vars(parser.parse_args())


    original_file = args["original_file"]
    filled_file = args["filled_file"]
    column = args["attribute"]
    mechanism = args["measure"]

    reviewer = Reviewer()
    reviewer.reviewer(original_file, filled_file, column, mechanism) 

if __name__ == '__main__': 
    main()
