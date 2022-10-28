import sys
import os
from csv_combiner import CSVCombiner
import test_generatefixtures
import unittest
import pandas as pd
from io import StringIO

class TestCombineMethod(unittest.TestCase):
    def __init__(self, path) -> None:
        self.path = os.path.dirname(__file__)

    # initialize all paths
    csv_combiner_path = "./csv_combiner.py"
    accessories_path = "./test_fixtures/accessories.csv"
    clothing_path = "./test_fixtures/clothing.csv"
    household_cleaners_path = "./test_fixtures/household_cleaners.csv"
    ef_path = "./test_fixtures/empty_file.csv"
    out_path = "./test_csv_output.csv"

    # initialize the test output
    backup = sys.stdout
    test_output = open(out_path, 'w+')
    combiner = CSVCombiner(os.path.dirname(__file__))
    combiner.main()

    @classmethod
    def setUpClass(cls):
        # generate the test fixture files located in ./test_fixtures/
        test_generatefixtures.main()
        # redirect the output to ./test_output.csv
        sys.stdout = cls.test_output

    @classmethod
    def tearDownClass(cls):

        cls.test_output.close()
        li = [cls.accessories_path, cls.clothing_path, cls.household_cleaners_path, cls.ef_path, cls.out_path]
        for temp_path in li:
            if os.path.exists(temp_path):
                os.remove(cls.temp_path)
        if os.path.exists("./test_fixtures"):
            os.rmdir("./test_fixtures")

    def setUp(self):
        # setup
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.out_path, 'w+')

    def tearDown(self):
        self.test_output.close()
        self.test_output = open(self.out_path, 'w+')
        sys.stdout = self.backup
        self.test_output.truncate(0)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

    def test_empty_files(self):

        # run csv_combiner with an empty file
        argv = [self.csv_combiner_path, self.ef_path]
        self.combiner.combine_csv(argv)

        self.assertIn("Warning: The following file is empty: ", self.output.getvalue())

    def test_non_existent_files(self):

        # run csv_combiner with a file that doesn't exist
        argv = [self.csv_combiner_path, "non_existent.csv"]
        self.combiner.combine_csv(argv)

        self.assertTrue("Error: File or directory not found:" in self.output.getvalue())

    def test_filename_column_added(self):

        # run csv_combiner with valid arguments
        argv = [self.csv_combiner_path, self.accessories_path, self.clothing_path]
        self.combiner.combine_csv(argv)

        # update the test_output.csv file
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        # check if the column exists in the produced data-frame
        with open(self.out_path) as f:
            df = pd.read_csv(f)
        self.assertIn('filename', df.columns.values)

    def test_filename_added_to_rows(self):
        # run csv_combiner with valid arguments
        argv = [self.csv_combiner_path, self.accessories_path, self.clothing_path]
        self.combiner.combine_csv(argv)

        # update the test_output.csv file
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        # check if a filename value exists in the produced data-frame
        with open(self.out_path) as f:
            df = pd.read_csv(filepath_or_buffer=f, lineterminator='\n')
        self.assertIn('accessories.csv', df['filename'].tolist())