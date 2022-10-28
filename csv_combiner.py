# Write a command line program that takes several CSV files as arguments. Each CSV file (found in the fixtures directory of this repo) will have the same columns. Your script should output a new CSV file to stdout that contains the rows from each of the inputs along with an additional column that has the filename from which the row came (only the file's basename, not the entire path). Use filename as the header for the additional column.
# Devansh Shah

import sys
import os
from os.path import exists
import pandas as pd
import time


class CSVCombiner():
    def __init__(self, path) -> None:
        self.path = os.path.dirname(__file__)

    def check(self, argv):
        # Store the command line arguments passed as a array 
        # Sample List generated from command line arguments= [input1.csv input2.csv output.csv]
        cmd_arg = argv

        # List to store path of all file if they exists
        cmd_arg_files = []
        for ar in cmd_arg[1:-1]:
            file_path = self.path +"\\"+ ar
            # Only append the file path if file exits
            if exists(file_path):
                cmd_arg_files.append(file_path)
            # check if given filename from command line argument is not found
            elif not exists(file_path):
                print("Error! File not found " + ar)
            # check if the given file is empty
            elif os.stat(file_path).st_size == 0:
                print("Error! Empty File (Warning) " + ar)
        return cmd_arg_files

    def combine_csv(self, argv: list):
        df_temp = []
        cmd_arg_files = self.check(argv)

        # After validation, if cmd_arg_files list is not emptry then we have combine csv files
        if cmd_arg_files:
            for f in cmd_arg_files:
                # Used try, except block to test a block of code for errors and handle the errors.
                try:
                    # Read csv files based on the given path
                    # temp = pd.read_csv(f)
                    # Instead of reading entire csv at a time, read as chunks to avoid memory issues
                    for temp_chunk in pd.read_csv(f, chunksize=10**4):
                    # First, Assign new column (Filename) to a DataFrame and Append CSV data to a list
                        df_temp.append(temp_chunk.assign(filename=os.path.basename(f)))
                
                # Handle the exception raised in pd.read_csv when empty data or header is encountered 
                except pd.errors.EmptyDataError:
                    print("{" + os.path.basename(f) + "}" + " Emptry file, Skipping it!")
                    continue

            # We have list of DataFrames in df_temp, Use concat method to concatenate pandas objects
            df_concat = pd.concat(df_temp, ignore_index=True)

            # Rearrange the "filename" column as the last column in final DataFrame
            new_cols = []
            for col in df_concat.columns:
                if col != "filename":
                    new_cols.append(col)
            new_cols.append("filename")
            df_concat = df_concat[new_cols]

            # Print new CSV file to stdout
            std_out_li = []
            std_out_li.append(df_concat)
            
            # flag for a header to be included in the final csv file
            header = True
            print()
            # combine all chunks, to print entire csv file to STDOUT
            for chunk in std_out_li:
                # read as chunks to avoid memory issues
                print(chunk.to_csv(index=False, header=header, chunksize=10**4, lineterminator='\n'), end='')
                header = False

            # Write object to a comma-separated values (csv) file
            df_concat.to_csv(self.path + "\\" + argv[-1], index = False)
            print("\nSuccess! Combined csv file is generated at -> " + self.path + "\\" + argv[-1])
        
        else:
            print("\nNo file found, Try again!")
            return

    def main(self):
        self.combine_csv(sys.argv)

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    obj = CSVCombiner(path)

    # To check the execution time of entire program to combine the csv files
    start_time = time.time()
    obj.main()
    print("\n\n--- Execution Time : %s seconds ---" % (time.time() - start_time))
