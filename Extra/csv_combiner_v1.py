import sys
import os
from os.path import exists
import csv
import pandas as pd
import time

# To check the execution time of entire program to combine the csv files
start_time = time.time()

# Store the command line arguments passed as a array 
# Sample List generated from command line arguments= [input1.csv input2.csv output.csv]
cmd_arg = sys.argv

# special variable __file__ contains the path to the current file
current_path = os.path.dirname(__file__)

# List to store path of all file if they exists
cmd_arg_files = []
for ar in cmd_arg[1:-1]:
    path = current_path +"\\"+ ar
    # Only append the file path if file exits
    if exists(path):
        cmd_arg_files.append(path)
    # check if given filename from command line argument is not found
    elif not exists(path):
        print("Error! File not found " + ar)
    # check if the given file is empty
    elif os.stat(path).st_size == 0:
        print("Error! Empty File (Warning) " + ar)

df_temp = []
for f in cmd_arg_files:
    # Used try, except block to test a block of code for errors and handle the errors.
    try:
        # Read csv files based on the given path
        temp = pd.read_csv(f)
        # First, Assign new column (Filename) to a DataFrame
        # Append CSV data to a list
        df_temp.append(temp.assign(filename=os.path.basename(f)))
    # Handle the exception raised in pd.read_csv when empty data or header is encountered 
    except pd.errors.EmptyDataError:
        print("{" + os.path.basename(f) + "}" + " Emptry file, Skipping it!")
        continue

# We have list of DataFrames in df_temp
# Used concat to concatenate pandas objects
df_concat = pd.concat(df_temp, ignore_index=True)

# Rearrange the "filename" column as the last column in final DataFrame
new_cols = []
for col in df_concat.columns:
    if col != "filename":
        new_cols.append(col)
new_cols.append("filename")

df_concat = df_concat[new_cols]

# Write object to a comma-separated values (csv) file
df_concat.to_csv(current_path + "\\" + cmd_arg[-1], index = False)

print("--- Execution Time : %s seconds ---" % (time.time() - start_time))
print("Success! Combined csv file is generated at -> " + current_path + "\\" + cmd_arg[-1] +"\n\n")

std_out_li = []
std_out_li.append(df_concat)
header = True
for chunk in std_out_li:
    print(chunk.to_csv(index=False, header=header, chunksize=10**4, lineterminator='\n'), end='')
    header = False