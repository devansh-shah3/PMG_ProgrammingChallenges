import pandas as pd
import sys
import test_generatefixtures
import unittest
import os
from csv_combiner import CSVCombiner
from io import StringIO


class TestCombineMethod(unittest.TestCase):
    def __init__(self, path) -> None:
        self.path = os.path.dirname(__file__)
        
    # initialize all paths
    test_output_path = "./test_output.csv"
    csv_c_path = "./csv_combiner.py"
    acc_path = "./test_fixtures/accessories.csv"
    clo_path = "./test_fixtures/clothing.csv"
    hc_path = "./test_fixtures/household_cleaners.csv"
    ef_path = "./test_fixtures/empty_file.csv"

    # initialize the test output
    backup = sys.stdout
    test_output = open(test_output_path, 'w+')
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

        if os.path.exists(cls.acc_path):
            os.remove(cls.acc_path)
        if os.path.exists(cls.clo_path):
            os.remove(cls.clo_path)
        if os.path.exists(cls.hc_path):
            os.remove(cls.hc_path)
        if os.path.exists(cls.ef_path):
            os.remove(cls.ef_path)
        if os.path.exists(cls.test_output_path):
            os.remove(cls.test_output_path)
        if os.path.exists("./test_fixtures"):
            os.rmdir("./test_fixtures")

    def setUp(self):
        # setup
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.test_output_path, 'w+')

    def tearDown(self):
        self.test_output.close()
        self.test_output = open(self.test_output_path, 'w+')
        sys.stdout = self.backup
        self.test_output.truncate(0)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

    def test_empty_files(self):

        # run csv_combiner with an empty file
        argv = [self.csv_c_path, self.ef_path]
        self.combiner.combine_files(argv)

        self.assertIn("Warning: The following file is empty: ", self.output.getvalue())

    def test_non_existent_files(self):

        # run csv_combiner with a file that doesn't exist
        argv = [self.csv_c_path, "non_existent.csv"]
        self.combiner.combine_files(argv)

        self.assertTrue("Error: File or directory not found:" in self.output.getvalue())

    def test_filename_column_added(self):

        # run csv_combiner with valid arguments
        argv = [self.csv_c_path, self.acc_path, self.clo_path]
        self.combiner.combine_files(argv)

        # update the test_output.csv file
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        # check if the column exists in the produced data-frame
        with open(self.test_output_path) as f:
            df = pd.read_csv(f)
        self.assertIn('filename', df.columns.values)

    def test_filename_added_to_rows(self):
        # run csv_combiner with valid arguments
        argv = [self.csv_c_path, self.acc_path, self.clo_path]
        self.combiner.combine_files(argv)

        # update the test_output.csv file
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        # check if a filename value exists in the produced data-frame
        with open(self.test_output_path) as f:
            df = pd.read_csv(filepath_or_buffer=f, lineterminator='\n')
        self.assertIn('accessories.csv', df['filename'].tolist())