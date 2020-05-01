# Change current directory to data directory
# always import this file first

# get string for current directory and change it to the data directory
import os
#os.chdir("..")
datadir = os.path.abspath(os.curdir) + '\\data\\input'
os.chdir(datadir)