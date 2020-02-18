from reader import reader,collectHeadings
import os

cwd = os.getcwd()
print(cwd)
for filename in os.listdir(cwd):
    if '.pdf' in filename:
        full_text = reader(filename)
        print(collectHeadings(full_text))
        print('---------------------------------------------------\n')