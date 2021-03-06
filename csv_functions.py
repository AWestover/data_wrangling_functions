# A compilation of all my general useful csv parsing functions

# libraries
import sys
import pandas as pd
import csv
import shutil
import os
import time
import json
from distutils.dir_util import copy_tree


# functions galore
def df_to_array(df):
    my_dict = df.to_dict()
    return list(my_dict.values())


# out puts a list of the unique elements in a list
def unique(array: list) -> list:
    return list(set(array))


# turns an array into a dictionary, by assigning the elements to the header keys
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


# makes a folder in the given directory if none exists, and clears out the old stuff from the folder if it already exists
def clean_folder(directory, folder):
    if folder in os.listdir(directory):
        print("I am putting the contents of your " + folder + " folder in the directory old inside your folders current directory")
        print("This is so that my program can create files in the new folder.")
        if 'old' not in os.listdir(directory):
            os.mkdir(directory + '/old')
        copy_tree(directory+"/"+folder, directory + '/old')
        shutil.rmtree(directory+'/'+folder)
    os.mkdir(directory + '/' + folder)


# gets a column from a csv by its index
def get_column(csv_loc, column_index, header=True):
    my_csv = csv.reader(open(csv_loc, 'r'))
    column = []
    for row in my_csv:
        column.append(row[column_index])
    if not header:
        column.pop(0)
    return column


# csv is the file name, wanted is a thing to extract, column is where to look for it
# looks in one column for anything in a list of wanteds and returns a df with only rows that had a wanted in the column
# that we are inspecting
# this is different than split bc wanteds is a list not a value
# exclude specifies whether the wanteds are wanted for exclusion or inclusion
# if you say exclusion=True the new csv will have no rows with a column that contains a wanted
# but if you say exclude=False all of the rows will have a column with a wanted in it
def filter_creator(csv_loc, column, wanteds, exclude=False):
    my_csv = csv.reader(open(csv_loc, 'r'))
    good_rows = []
    for row in my_csv:
        if not exclude:
            if row[column] in wanteds:
                good_rows.append(row)
        else:
            if row[column] not in wanteds:
                good_rows.append(row)
    my_dict = array_to_dict(good_rows, get_headers(csv_loc))
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


# makes a json more readable as a string that is better in a txt file
def simple_json_to_pretty_text(json_data):
    out_string = ''
    if type(json_data) == dict:
        all_keys = list(json_data.keys())
        for a_key in all_keys:
            out_string += a_key + ": " + json_data[a_key]+ "\n"
    elif type(json_data) == list:
        for element in json_data:
            out_string += simple_json_to_pretty_text(element) + "-"*30 + "\n"
    return out_string


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


# puts out a new df without only specified columns
def column_excluder(df, not_wanteds):
    try:
        headers = list(df)
        new_columns = []
        for header in headers:
            if header not in not_wanteds:
                new_columns.append(header)
        out_df = df[new_columns]  # yes i know that is an array inside of an array deal with it
        return out_df
    except PermissionError:
        print("Please close all files that you would like Python to work with!")
        return None


# gets all rows of a df where a phrase occours in a column in the row
def get_phrase_rows(csv_loc, column, phrase, case_sensitive=False, exclusion=False):
    my_csv = csv.reader(open(csv_loc, 'r'))
    good_rows = []
    headers = False
    column_index = 0
    for row in my_csv:
        if not headers:
            headers = row
            column_index = headers.index(column)
        else:
            if case_sensitive:
                if not exclusion:
                    if phrase in row[column_index]:
                        good_rows.append(row)
                else:
                    if phrase not in row[column_index]:
                        good_rows.append(row)
            else:
                if not exclusion:
                    if phrase.lower() in row[column_index].lower():
                        good_rows.append(row)
                else:
                    if phrase.lower() not in row[column_index].lower():
                        good_rows.append(row)
    my_dict = array_to_dict(good_rows, headers)
    return pd.DataFrame.from_dict(my_dict)

