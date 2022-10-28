# PMG_ProgrammingChallenges

# CSV Combiner

Write a command line program that takes several CSV files as arguments. Each CSV file (found in the fixtures directory of this repo) will have the same columns. Your script should output a new CSV file to stdout that contains the rows from each of the inputs along with an additional column that has the filename from which the row came (only the file's basename, not the entire path). Use filename as the header for the additional column.


# Example
This example is provided as one of the ways your code should run. It should also be able to handle more than two inputs, inputs with different columns, and very large (> 2GB) files gracefully.


# How to run the csv_combiner.py
python csv_combiner.py ./fixtures/accessories.csv ./fixtures/clothing.csv combined.csv

Given two input files named clothing.csv and accessories.csv. Generated output file name combined.csv
