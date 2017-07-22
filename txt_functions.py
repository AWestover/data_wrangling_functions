# A compilation of all of my useful and general text parsing functions
# has to run in power shell with setting
# chcp 65001
# to set the encoding
# if running in pycharm you can't print anything...
# https://stackoverflow.com/questions/32382686/unicodeencodeerror-charmap-codec-cant-encode-character-u2010-character-m


# libraries
import os
import pdb
import re

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
            txt_file = open(txt_file_loc, 'r')  # if this creates an error try setting encoding='utf-8' or 'Latin 1'
        else:
            txt_file = open(txt_file_loc, 'r', encoding=encoding)
        for row in txt_file:
            all_text += row
        txt_file.close()

    else:
        print("Put an invalid file name in to txt_to_array. Cannot find", txt_file_loc)
    return all_text


# splits up a string of text by spacing and returns an array of words
def string_to_words(string: str, remove_punctuation='no', to_lower_case=False) -> list:
    if to_lower_case:
        string = string.lower()
    all_words = string.split(' ')
    if remove_punctuation == 'yes':
        punctuation_list = [',', '.', '!', '?', '\n']
        for i in range(0, len(all_words)):
            for punctuation in punctuation_list:
                all_words[i] = all_words[i].replace(punctuation, '')
    if remove_punctuation == 'For math!':
        punctuation_list = [',', '!', '?', '\n']
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
def split_by_footer(txt_file_loc, footer, encoding=False):
    sections = []
    if valid_txt_file(txt_file_loc):
        if not encoding:
            txt_file = open(txt_file_loc, 'r')
        else:
            txt_file = open(txt_file_loc, 'r', encoding=encoding)
        cur_section = ''
        for row in txt_file:
            cur_section += row
            if footer in row:
                sections.append(cur_section)
                cur_section = ''
        txt_file.close()
    else:
        print("Put an invalid file name in to split_by_full. Cannot find", txt_file_loc)
    return sections


# puts a string into a text file
def string_to_txt_file(string, file_loc, encoding=False):
    if not encoding:
        f = open(file_loc, 'w')
    else:
        f = open(file_loc, 'w', encoding=encoding)
    f.write(string)
    f.close()


# turns an array of strings (which are presumably rows of a text file) in to a string with line breaks
def rows_to_string(array):
    out_string = ''
    for row in array:
        out_string += row + '\n'
    return out_string


# checks if a string is equal to any other string in a list
def any_string_matches(string, list_of_strings):
    match_found = False
    for a_string in list_of_strings:
        if a_string == string:
            match_found = True
    return match_found


# after the program sees a key work it looks for the next instance
# of something else and returns the strip of text encapsulated by the range words
# this will return all of the excerpts of this kind
# mark_words must contain only 2 words
def txt_word_range(mark_words, txt_string):
    all_words = string_to_words(txt_string, to_lower_case=True, remove_punctuation='For math!')
    mark = 0
    excerpts = []
    string_mark = 0
    for i in range(0, len(all_words)):
        if mark_words[mark] in all_words[i]:
            if mark == 0:
                mark = 1
                string_mark = i
            else:
                mark = 0
                excerpts.append(all_words[string_mark:i+1])
    return excerpts


# gets all of the percents (by looking for % signs and then backing up to look for a number)
# assumes that the percent is either formatted as num% (we remove all the spaces so spacing doesn't matter). Other formats are BAD!!!
def get_all_percents(string):
    better_string = string.replace(' ', '')
    all_percents = []
    for i in range(0, len(better_string)):
        if better_string[i] == "%":
            backwards_i = 1
            while better_string[i - backwards_i] == '.' or better_string[i - backwards_i].isdigit() or better_string[i - backwards_i] == ' ':
                backwards_i += 1
            all_percents.append(better_string[i-backwards_i+1:i+1])
    return all_percents


# pubmed analysis execution
entries = split_by_footer('data/pubmed_result.txt', 'PMID', encoding='utf-8')
for i in range(0, 20):
    # print(txt_word_range(["specificity", "%"], entries[i]))
    # string_to_txt_file(entries[i], "data/excerpt"+str(i)+".txt", encoding='utf-8')
    print(get_all_percents(entries[i]))


'''
on pubmed you can do advanced searches as drop down menu logic
and this is what it looks like in parentheses:
this one yielded over 100,000 abstracts.  I'm not sure how much more restrictive to be.
(((((((sensitivity) AND specificity) AND human) NOT genetic) NOT AUC) NOT ROC) NOT receiver operating curve) AND english[Language] AND "predictive value" AND diagnostic
the idea was to avoid genetics, and avoid people reporting AUC or ROC values (where random chance is obvious).


ideas:
1. extract all percent and nums from each file to their  entry in a json
2. get the closest instance of a statistical term to each thing
send
closest flexible([sens, spec, pos, neg]), float, '%' pair
'''



