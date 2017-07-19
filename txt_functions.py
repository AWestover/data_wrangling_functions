# A compilation of all of my useful and general text parsing functions

# libraries
import os


# functions


# Checks if a location (file or folder name) exists on your computer
def location_exists(name: str) -> bool:
    return os.path.exists(name)


# checks if a file 1. exists and 2. is a text file
def valid_txt_file(name: str) -> bool:
    if type(name) != str:
        return False
    else:
        return location_exists(name) and '.txt' in name


# takes in a file path of a txt file and turns it in to an array with each element being a string form row of text
def txt_file_to_array(txt_file_loc):
    all_rows = []
    if valid_txt_file(txt_file_loc):
        txt_file = open(txt_file_loc, 'r')
        for row in txt_file:
            all_rows.append(row)
        txt_file.close()

    else:
        print("Put an invalid file name in to txt_to_array. Cannot find", txt_file_loc)
    return all_rows


# takes in a file path of a txt file and turns it in to an string of the text
def txt_file_to_string(txt_file_loc, encoding=False):
    all_text = ''
    if valid_txt_file(txt_file_loc):
        if not encoding:
            txt_file = open(txt_file_loc, 'r') # if this creates an error try setting encoding='utf-8' or 'Latin 1'
        else:
            txt_file = open(txt_file_loc, 'r', encoding=encoding)
        for row in txt_file:
            print (row)
            all_text += row
        txt_file.close()

    else:
        print("Put an invalid file name in to txt_to_array. Cannot find", txt_file_loc)
    return all_text


# splits up a string of text by spacing and returns an array of words
def string_to_words(string: str, remove_punctuation=False, to_lower_case=False) -> list:
    if to_lower_case:
        string = string.lower()
    all_words = string.split(' ')
    if remove_punctuation:
        punctuation_list = [',', '.', '!', '?']
        for i in range(0, len(all_words)):
            for punctuation in punctuation_list:
                all_words[i] = all_words[i].replace(punctuation, '')
    return all_words


# takes text and moves every letter up by a standard key
def caesar_shifter(message, key):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    new_message = ''
    used = False
    for char in message:
        for k in range(0, len(alphabet)):
            if char.lower() == alphabet[k]:
                new_message += alphabet[(k + int(key)) % len(alphabet)]
                used = True
        if not used:
            new_message += char
    return new_message


# makes sure that a number is turned into a string of a specific length with leading zeros added as needed to increase the length
def pad(total_length, num):
    out_string = str(num)
    if len(out_string) < total_length:
        out_string = "0"*(total_length-len(out_string)) + out_string
    elif len(out_string) > total_length:
        out_string = out_string[0:total_length]
    return out_string


# reverses padding, deleting leading zeros and letters until it gets to something that it can turn in to an integer
def depad(padded_num):
    while (str(padded_num[0]).lower() in [str(chr(i)) for i in range(97, 123)] or padded_num[0] == '0') and len(padded_num) > 0:
        padded_num = padded_num[1:len(padded_num)]  # CHECK
    return int(padded_num)


# Split a text document by known footers (ie. you have a bunch of stories that say blah blah \nThe End. And you want to separate the stories)
def split_by_footer(txt_file_loc, encoding=False):
    print(valid_txt_file(txt_file_loc))
