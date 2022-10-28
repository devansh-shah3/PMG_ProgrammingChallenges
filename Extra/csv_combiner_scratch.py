import sys
import os
import csv

import time
start_time = time.time()

cmd_arg = sys.argv
current_path = os.path.dirname(__file__)
# print(current_path)
#cmd_arg_files = glob.glob(current_path + "/*.csv")
cmd_arg_files = []
for ar in cmd_arg[1:-1]:
    cmd_arg_files.append(current_path +"\\"+ ar)
# print(cmd_arg_files)
#path = r'path_to_files/' 
#cmd_arg_files = glob.glob(path + "/*.csv")

#with open(current_path + '\\output.csv','w+', newline='') as opfile:
with open(current_path + "\\" + cmd_arg[-1],'w+', newline='') as opfile:
    out_write = csv.writer(opfile)
    first = True
    for new_file in cmd_arg_files:
        fname = new_file.split("\\")
        with open(new_file, "r+") as nf_data:
            r_data = csv.reader(nf_data)
            # for row in r_data:
                # print(row)
            # skip header line, except for the first file
            row = next(r_data)
            if first:
                print(row)
                row.append("filename")
                out_write.writerow(row)
                first = False                                  
            for row in r_data:
                row.append(fname[-1])
                out_write.writerow(row)
                    

print("--- %s seconds ---" % (time.time() - start_time))