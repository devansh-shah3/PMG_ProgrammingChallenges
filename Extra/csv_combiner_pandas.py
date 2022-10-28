import sys
import os
import csv
import pandas as pd
from os.path import exists
import time

start_time = time.time()
cmd_arg = sys.argv
current_path = os.path.dirname(__file__)

cmd_arg_files = []
for ar in cmd_arg[1:-1]:
    path = current_path +"\\"+ ar
    if exists(path):
        cmd_arg_files.append(path)
    else:
        print("File not found " + ar)

# cmd_arg_files.sort(key = lambda x: x[1], reverse=True)

#sort files based on column size, so we can get filename column at last
# cmd_arg_files = []
# for ar in cmd_arg[1:-1]:
    # size = pd.read_csv(current_path +"\\"+ ar).shape[1]
    # cmd_arg_files.append((current_path +"\\"+ ar, size))
# cmd_arg_files.sort(key = lambda x: x[1], reverse=True)


# df = pd.DataFrame()
# for new_file in cmd_arg_files:
    # fname = new_file.split("\\")
    # if new_file.endswith('.csv'):
        # df_new = pd.read_csv(new_file)
        # df_new['filename'] = fname[-1]
        # df = df.append(df_new, ignore_index=True)
# df.to_csv(current_path + "\\" + cmd_arg[-1], index = False)

# df = pd.DataFrame()
# for new_file in cmd_arg_files:
    # print(new_file)
    # fname = new_file[0].split("\\")
    # print(fname)
    # if new_file[0].endswith('.csv'):
        # df_new = pd.read_csv(new_file[0])
        # df_new['filename'] = fname[-1]
        # df = df.append(df_new, ignore_index=True)
# df.to_csv(current_path + "\\" + cmd_arg[-1], index = False)


df_temp = []
for f in cmd_arg_files:
    try:
        temp = pd.read_csv(f)
        df_temp.append(temp.assign(filename=os.path.basename(f)))
    except pd.errors.EmptyDataError:
        print("Emptry file, Skipping it!")
        continue
df_concat = pd.concat(df_temp, ignore_index=True)
# df_concat = pd.concat([pd.read_csv(f).assign(filename=os.path.basename(f)) for f in cmd_arg_files], ignore_index=True)

new_cols = []
for col in df_concat.columns:
    if col != "filename":
        new_cols.append(col)
new_cols.append("filename")
# new_cols = [col for col in df_concat.columns if col != 'filename'] + ['filename']

df_concat = df_concat[new_cols]
df_concat.to_csv(current_path + "\\" + cmd_arg[-1], index = False)

print("--- Execution Time : %s seconds ---" % (time.time() - start_time))
print("Success! Combined csv file is generated at -> " + current_path + "\\" + cmd_arg[-1])