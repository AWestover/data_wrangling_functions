# various functions which help parse csvs (and user filename input)

#libraries
import sys
import pandas as pd
import csv
import shutil
import os
import time

#functions galore
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
def split_all(csv_loc, collumn, wanteds, new_file_names=None):
    if not new_file_names:
        new_file_names = len(wanteds)*["_clean.csv"]
    for i in range(0, len(wanteds)):
        split(csv_loc, collumn, wanteds[i], new_file_name=new_file_names[i])


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


# checks for valid input
def validInput(question, condition):
    if condition == "valid file name":
        uin = "not a path"
        while not os.path.exists(uin):
            uin = input(question)
    elif type(condition) == type:
        uin=None
        while type(uin) != condition:
            uin = input(question)
            try:
                uin = condition(uin)
            except:
                pass
    elif type(condition) == list:
        uin = None
        for i in range(0, len(condition)):
            if type(condition[i])==int or type(condition[i])==float or type(condition[i])==bool:
                condition[i]=str(condition[i])
        while uin not in condition:
            uin = input(question)
    else:
        print("Please carefully input your answer to comply with the following condition : "+condition)
        uin = input(question)
    return uin
