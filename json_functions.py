# A compilation of all of my json functions

# libraries
import json


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
