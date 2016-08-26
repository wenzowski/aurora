import sys
# import numpy as np
# import matplotlib.pyplot as plt
#
# pageHeadSectionFile = open(sys.argv[1],'r')
# data = pageHeadSectionFile.read()
# pageHeadSectionFile.close()
# rows = data.split("\n")
# #note the values for these two arrays start on index 1
# latArray = rows[1].split(",")
# lonArray = rows[1].split(",")
# for i in rows
#   if i > docLen
# print output
# Open file
f = open(sys.argv[1], 'r')

# Read and ignore header lines
header1 = f.readline()
header2 = f.readline()
header3 = f.readline()

# Loop over lines and extract variables of interest
for line in f:
    line = line.strip()
    columns = line.split()
    name = columns[2]
    j = float(columns[3])
    print(name, j)

f.close()
