# A compilation of all of my json functions

# libraries
import json
import pandas as pd
import csv


# functions

# unlikely to be useful, jsons are already nice
def json_to_list(json_file_loc):
    json_data = open(json_file_loc).read()
    data = json.loads(json_data)
    my_list = []
    for item in data:
        my_list.append(item)
    return my_list


# unlikely to be useful, jsons are already nice, but this turns a json into a string
def json_to_string(json_file_loc):
    json_data = open(json_file_loc).read()
    my_string = ''
    for char in json_data:
        my_string += char
        if char == ',':
            my_string += '\n'
    return my_string


# puts python stuff (array or dict) into a json
def data_to_json(json_file_loc, my_data, sort_keys=False, indent=0):
    with open(json_file_loc, 'w') as fp:
        json.dump(my_data, fp, sort_keys=sort_keys, indent=indent)


# checks if a string is equal to any other string in a list
def any_string_matches(string, list_of_strings):
    match_found = False
    for a_string in list_of_strings:
        if a_string == string:
            match_found = True
    return match_found


# makes a json more readable
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


# turns a list of tuples into a nice string
def tuple_list_to_nice_string(tuple_list):
    nice_string = ''
    for tup in tuple_list:
        nice_string += str(tup) + ", "
    nice_string = nice_string[0:len(nice_string)-2]
    return nice_string


# list of keys and values into a dictionary
def key_vals_to_dict(keys, vals):
    my_dict = {}
    for i in range(0, len(keys)):
        my_dict[keys[i]] = vals[i]
    return my_dict


# returns each row as a dictionary into a json like object
def csv_to_json(csv_loc, wanted_columns='all'):
    my_csv = pd.read_csv(csv_loc)
    if wanted_columns == 'all':
        wanted_columns = list(my_csv)
    wanted_columns_indices = [list(my_csv).index(a_header) for a_header in wanted_columns]
    my_csv = csv.reader(open(csv_loc, 'r'))
    my_dicts = []
    for row in my_csv:
        wanted_vals = [row[wanted_columns_index] for wanted_columns_index in wanted_columns_indices]
        my_dicts.append(key_vals_to_dict(wanted_columns, wanted_vals))
    return my_dicts


# makes a json more readable, WARNING VERY SPECIALIZED, NOT REALLY REUSABLE
def simple_json_to_extra_pretty_text(json_data, split_parenths=False):
    out_string = ''
    if type(json_data) == dict:
        all_keys = list(json_data.keys())
        for a_key in all_keys:
            if split_parenths:  # splits tuples
                cur_string_list = json_data[a_key]
                cur_string_list = cur_string_list.replace(',', ' ')
                cur_string_list = cur_string_list.replace("'", '')
                cur_string_list = cur_string_list.split(')  (')
                out_string += "\n"+a_key + ":\n"
                for element in cur_string_list:
                    c_element = element.replace(')','')
                    c_element = c_element.replace('(', '')
                    out_string += c_element + "\n"
            else:  # default
                out_string += a_key + ": " + json_data[a_key]+ "\n\n"
    elif type(json_data) == list:
        for element in json_data:
            out_string += simple_json_to_extra_pretty_text(element, split_parenths = split_parenths) + "-"*140 + "\n"
    return out_string


'''
# usage example

print(json_to_list("data/test_json.json"))
my_info = {
    'asd': 'asd',
    'as': 'df'
}
more_info = {
    'asd': 'asd',
    'as': 'df'
}
all_info = [my_info, more_info]
data_to_json('data/new_json.json', all_info, sort_keys=True, indent=4)
print(json_to_list("data/new_json.json"))

print(simple_json_to_pretty_text(all_info))
'''
