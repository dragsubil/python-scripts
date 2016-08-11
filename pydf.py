#!usr/bin/env python3
#show df with a progress bar

import subprocess
import re
import os

def printDfWithBar(column_titles,line,percent):
    progress_complete = '#'*(percent//5)
    progress_incomplete = '-'*((100 - percent)//5)
    column_titles = column_titles[:-1]
    line = line[:-1]   #removes the \n at the end
    print(column_titles + "  Progress bar")
    print(line + "          [{}{}]".format(progress_complete,progress_incomplete))



df_output_file = open("tmpfile",'w+',encoding='UTF-8')


subprocess.run(["df","-h"],stdout=df_output_file)
df_output_file.seek(0)
column_titles = df_output_file.readline()
for line in df_output_file:
    if re.search(r'^/dev/sd',line):   # I'm only considering the storage drives
       separated_fields = line.split(" ")
       percent = int(separated_fields[-2][0:-1])
       printDfWithBar(column_titles,line,percent)

df_output_file.close()
os.remove("tmpfile")
