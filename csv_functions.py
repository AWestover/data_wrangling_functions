# A compilation of all my general useful csv parsing functions

# libraries
import sys
import pandas as pd
import csv
import shutil
import os
import time
import json


# functions galore
def df_to_array(df):
    my_dict = df.to_dict()
    return list(my_dict.values())


def array_to_dict(array, headers):
    my_dict = {}
    for j in range(0, len(headers)):
        my_dict[headers[j]] = [row[j] for row in array]
    return my_dict


# csv is the file name, wanted is a thing to extract, column is where to look for it
def split(csv_loc, column, wanted, new_file_name='_clean.csv'):
    my_csv = csv.reader(open(csv_loc, 'r'))
    rows = []
    for row in my_csv:
        rows.append(row)
    marked_rows = []
    for i in range(0, len(rows)):
        if wanted.lower() in rows[i][column].lower():
            marked_rows.append(i)

    new_headers = []
    for i in range(0, len(rows[0])):
        if rows[0][i] == '':
            new_headers.append('Column '+str(i))
        else:
            new_headers.append(rows[0][i])

    my_dict = array_to_dict([rows[marked_row] for marked_row in marked_rows], new_headers)
    df = pd.DataFrame.from_dict(my_dict)
    df.to_csv(new_file_name, index=False)


# list version of above function
def split_all(csv_loc, column, wanteds, new_file_names=None):
    if not new_file_names:
        new_file_names = len(wanteds)*["_clean.csv"]
    for i in range(0, len(wanteds)):
        split(csv_loc, column, wanteds[i], new_file_name=new_file_names[i])


def clean_folder(directory, folder):
    if folder in os.listdir(directory):
        print("Im deleting you csvs folder")
        print("you have 10 seconds to move it before I through it away")
        time.sleep(1)
        shutil.rmtree(directory+'/'+folder)
    os.mkdir(directory + '/' + folder)


def get_column(csv_loc, column_index):
    my_csv = csv.reader(open(csv_loc, 'r'))
    column = []
    for row in my_csv:
        column.append(row[column_index])
    return column


# csv is the file name, wanted is a thing to extract, column is where to look for it
def filter_creator(csv_loc, column, wanteds):
    my_csv = csv.reader(open(csv_loc, 'r'))
    rows = []
    for row in my_csv:
        rows.append(row)
    marked_rows = []
    for i in range(0, len(rows)):
        for wanted in wanteds:
            if wanted == rows[i][column]:
                marked_rows.append(i)
                break

    my_dict = array_to_dict([rows[marked_row] for marked_row in marked_rows], rows[0])

    df = pd.DataFrame.from_dict(my_dict)
    df.to_csv(csv_loc.replace('.csv', "_clean.csv"), index=False)


# gets the header row of a csv
def get_headers(csv_loc):
    my_df = pd.read_csv(csv_loc)
    return list(my_df)


# takes a csv and looks up the index of a certain header
def header_to_index(csv_loc, header):
    headers = get_headers(csv_loc)
    return headers.index(header)


# splits the date and time in a column of a csv (header is a string)
# for if the date and time where in the same column but seperated by a space
def The_Date_Time_Seperator(csv_loc, header, new_column_name, delete_old_column=False):
    try:
        my_csv = pd.read_csv(csv_loc)
        header_column = df_to_array(my_csv[header])
        times = []
        dates = []
        for time_date in header_column:
            if type(time_date) == str:
                splittimedate=time_date.split(" ")
                dates.append(splittimedate[0])
                times.append(splittimedate[1])
            else:
                dates.append("")
                times.append("")
        if delete_old_column:
            del my_csv[header]
        my_csv[new_column_name + " _Times"] = times
        my_csv[new_column_name + " _Dates"] = dates
        my_csv.to_csv(csv_loc, index=False)
        print("Time and Date successfully separated in " + header + ' column of ' + csv_loc)
    except:
        print("Something went kind of wrong with the date time separator...")


# list of keys and values into a dictionary
def key_vals_to_dict(keys, vals):
    my_dict = {}
    for i in range(0, len(keys)):
        my_dict[keys[i]] = vals[i]
    return my_dict


# returns each row as a dictionary into a json like object
def csv_to_json(csv_loc, wanted_columns='all'):
    if wanted_columns == 'all':
        wanted_columns = get_headers(csv_loc)
    wanted_columns_indices = [header_to_index(csv_loc, a_header) for a_header in wanted_columns]
    my_csv = csv.reader(open(csv_loc, 'r'))
    my_dicts = []
    for row in my_csv:
        wanted_vals = [row[wanted_columns_index] for wanted_columns_index in wanted_columns_indices]
        my_dicts.append(key_vals_to_dict(wanted_columns, wanted_vals))
    return my_dicts


# checks if a string is equal to any other string in a list
def any_string_matches(string, list_of_strings):
    match_found = False
    for a_string in list_of_strings:
        if a_string == string:
            match_found = True
    return match_found


# deletes the weird brackets around a json and all of the other curly brackets and deletes all of the quotes. Danger, you might lose information
def json_string_to_pretty_text(json_string):
    pretty_out_string = ''
    for char in json_string:
        if not any_string_matches(char, ['"', "{", "}", "[", "]", ","]):
            pretty_out_string += char
        elif char == ",":
            pretty_out_string += "\n"
        elif char == "}":
            pretty_out_string += "---------------"
    return pretty_out_string


# puts python stuff (array or dict) into a json
def data_to_json(json_file_loc, my_data, sort_keys=False, indent=0):
    with open(json_file_loc, 'w') as fp:
        json.dump(my_data, fp, sort_keys=sort_keys, indent=indent)


# unlikely to be useful, jsons are already nice, but this turns a json into a string
def json_to_string(json_file_loc):
    json_data = open(json_file_loc).read()
    my_string = ''
    for char in json_data:
        my_string += char
        if char == ',':
            my_string += '\n'
    return my_string


# puts a string into a text file
def string_to_txt_file(string, file_loc, encoding=False):
    if not encoding:
        f = open(file_loc, 'w')
    else:
        f = open(file_loc, 'w', encoding=encoding)
    f.write(string)
    f.close()


