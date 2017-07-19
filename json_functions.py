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


# puts python stuff (array or dict) into a json
def dict_to_json(json_file_loc, my_data, sort_keys=False, indent=0):
    with open(json_file_loc, 'w') as fp:
        json.dump(my_data, fp, sort_keys=sort_keys, indent=indent)

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
dict_to_json('data/new_json.json', all_info, sort_keys=True, indent=4)
print(json_to_list("data/new_json.json"))
'''
