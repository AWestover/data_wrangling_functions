
These programs aim to parse usefull information from a word document form.

The input is a collection of .docm files with similar format

To parse out information

First go into the data dirrectory and run 
unzip a.docm

Next make sure all of your regular expressions and column names are in place
regexpal is usefull in generating these. 
Note that your text base should be stuff.txt 
because that is what the text the program reads looks like

Next run bsr.py to generate a nice csv with all the columns that you coded regular
expressions in for

Next run checks.py to generate a csv with binary indicators for each check box
as to whether or not it is checked


Note: to run on Windows install Beautiful soup and change file paths
