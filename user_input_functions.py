# A compilation of all of my user input parsing functions

# libraries
import os
import sys
# use raw_input for Python 27, this is for python 3.X
# sys.version > 3.5.2


# checks for valid input
def valid_input(question, condition):
    if condition == "valid file name":
        uin = "not a file"
        while not os.path.exists(uin) or '.' not in uin:
            uin = input(question)

    elif condition == "valid csv":
        uin = "not a file"
        while not os.path.exists(uin) or '.csv' not in uin:
            uin = input(question)

    elif condition == "valid folder":
        uin = "not a path"
        while not os.path.exists(uin) or '.' in uin:
            uin = input(question)

    elif condition == "valid json":
        uin = "not a file"
        while not os.path.exists(uin) or '.json' not in uin:
            uin = input(question)

    elif condition == "valid xls":
        uin = "not a file"
        while not os.path.exists(uin) or '.xls' not in uin:
            uin = input(question)

    elif type(condition) == type:
        uin = None
        while type(uin) != condition:
            uin = input(question)
            try:
                uin = condition(uin)
            except:
                pass
    elif type(condition) == list:
        uin = None
        for i in range(0, len(condition)):
            if type(condition[i]) == int or type(condition[i]) == float or type(condition[i]) == bool:
                condition[i] = str(condition[i])
        while uin not in condition:
            uin = input(question)
    else:
        print("Please carefully input your answer to comply with the following condition : "+condition)
        uin = input(question)
    return uin
