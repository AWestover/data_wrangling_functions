# functions to help with ftp reading (and maybe writing someday...)


# Importing necessary libraries
import ftplib
import os
import zipfile
import pandas as pd
import shutil
import time


# General function first

# A function that makes sure your input is accepted (No need to look at this function really)
# It basically just catches errors in user input
def validInput(question, condition):
    if type(condition) == type:
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


# Useful for parsing file names. This function removes the first instance of a phrase in a longer string (like a file name).
def rm_first_pho(big_phrase, bad_phrase):
    for i in range(0, len(big_phrase)):
        if big_phrase[i] == bad_phrase[0]:
            if big_phrase[i:len(bad_phrase)] == bad_phrase:
                return big_phrase[0:i] + big_phrase[i+len(bad_phrase):len(big_phrase)]


# Useful for parsing file names and other text.
# I use this to avoid downloading certain file types if they are not good.
# It is used elsewhere too.
def any_phrase_occurs(big_phrase, possible_phrases, case_sensitive=True):
    occurred = False
    for possible_phrase in possible_phrases:
        if case_sensitive:
            if possible_phrase in big_phrase:
                occurred = True
                break
        if not case_sensitive:
            if possible_phrase.lower() in big_phrase.lower():
                occurred = True
                break
    return occurred


# Helps with name guessing, if there are multiple possible names for one such file
def get_real_name(tdoc, guesses):
    for guess in guesses:
        if guess in tdoc:
            return guess


# this makes a list of years that I will not be downloading
# You can configure this to download more or less of the data
oldest_download = 54
bad_years = ['00']
for i in range(1, 54):
    if i < 10:
        bad_years.append('0'+str(i))
    else:
        bad_years.append(str(i))


# Now the FTP specific functions

# Gets all the tdocs. It starts in the directory direc and the ftp tp. It then proceeds to all the contents of the directory.
# For all the contents of the directory if it sees another directory in the first directory this function is recursively called again
# on the inside of the new directory. This allows the program to get to all the branches of the file tree. It then downloads all of the
# files unless they are zips or pdfs or docs or ppts
def get_all_Tdocs(ftp, direc):
    root_dir = ftp.pwd()
    contents = ftp.nlst(ftp.pwd()+direc)
    act_contents = [rm_first_pho(content, ftp.pwd()) for content in contents]
    print(act_contents, contents, direc, root_dir)
    for file in act_contents:
        try:
            if '.' not in file and not any_phrase_occurs(file, bad_years):
                print("DIRECTORY " + root_dir + file)
                # Looks inside this directory, (recursion)
                get_all_Tdocs(ftp, file)
            # if it is not a directory the filename will have a dot in it before the extension
            # if it is a file, but its not a zip or pdf or doc or ppt we download it
            # Adjust the list of allowed downloads as desired
            elif '.' in file and not any_phrase_occurs(file, bad_years+['.zip', '.pdf', '.doc', '.ppt', '.txt'], case_sensitive=False):
                alone_file_name = rm_first_pho(file, direc+"/")
                cd(ftp, rm_first_pho(direc, "/"))
                getFile(ftp, alone_file_name)
                cd(ftp, root_dir)
        except ftplib.error_perm as error:  # Handle 550 not found etc
            print("SORRY ERROR ERROR ERROR", file)


# Cleans a tdoc by extracting useful rows and columns after verifying that the correct names are being used
# For each row and column. Also has to make sure it is in the right sheet
# Puts useful information in to the all_tdocs.csv file
# Suggestions with ways to improve this section would be helpful
# I can't actually tell if I am getting all the good data
def clean_tdoc(old_name):
    tdoc_andfluf = pd.ExcelFile(old_name)
    alternate_tdoc_names = ['Tdoc', 'tdoc', 'TDoc', 'TDOC']
    for sheet in tdoc_andfluf.sheet_names:
        if any_phrase_occurs(sheet, ['tdoc'], case_sensitive=False):
            tdoc = tdoc_andfluf.parse(sheet)
            real_collumns = [get_real_name(tdoc, ['status', 'Status', 'Tdoc status', 'TDoc status', 'tdoc status', 'Tdoc Status', 'TDoc Status']),
            get_real_name(tdoc, alternate_tdoc_names),
            get_real_name(tdoc, ['Source', 'source', 'sources', 'Sources']), get_real_name(tdoc, ['Type', 'type']),
            get_real_name(tdoc, ['title'])]
            bettertdoc = tdoc[real_collumns]
            ericssonSources = []
            for i in range(0, len(bettertdoc['Source'])):  # bettertdoc.shape[0] = len(bettertdoc['Source'])
                if type(bettertdoc['Source'][i]) == str:
                    if 'Ericsson' in bettertdoc['Source'][i]:
                        ericssonSources.append(i)
            besttdoc = bettertdoc.ix[ericssonSources]
            with open('all_tdocs.csv', 'a') as f:
                # this puts the information into your csv, only including a header if the file is empty already
                if os.path.getsize('all_tdocs.csv') > 0:
                    besttdoc.to_csv(f, header=False, index=False)
                else:
                    besttdoc.to_csv(f, header=True, index=False)


# Gets a file and unzips it if it is a zip
def getFile(ftp, file):
    try:
        print("Getting", file)
        ftp.retrbinary('RETR ' + file, open(file, 'wb').write)
        print("File succesfully downloaded")
        prevName = file
        newName = 'documents/' + prevName
        if os.path.exists(newName):
            os.remove(newName)
        os.rename(prevName, newName)
        if os.path.splitext(newName)[1] == '.zip':
            zip_archive = zipfile.ZipFile(newName)
            zip_archive.extractall('documents')
            zip_archive.close()
            os.remove(newName)
    except ftplib.error_perm as error:  # Handle 550 not found etc
        print("There was an Error", error)


# Makes a list of a directories contents. It is very hard to read.
# Much better to just look on the website, but this exists if you really want.
def find_full_tree_recursive(ftp, direc):
    contents = ftp.nlst(direc)
    full_tree = []
    for file in contents:
        try:
            if '.' not in file:
                full_tree.append([file, find_full_tree_recursive(ftp, file)])  # Warning recursion might not work
            else:
                full_tree.append(file)
        except ftplib.error_perm as error:  # Handle 550 not found etc
            print("SORRY TOUGHT LUCK", file)
    return full_tree


# Writes the tree contents to a text file
def print_tree_contents(ftp):
    full_tree = find_full_tree_recursive(ftp, ftp.pwd())
    out_file = open('full_tree.txt', 'w')
    out_file.write(str(full_tree))
    out_file.close()


# Change directory in the ftp
def cd(ftp, newdir):
    try:
        ftp.cwd(newdir)
    except ftplib.error_perm as error:  # Handle 550 not found etc
        print("There was an Error", error)


# Connect to the ftp site. Usually takes a while to start up a connection.
# This will then run a list of already written commands
def ftpAutomatedConnect(siteAdress, commandList):
    try:
        with ftplib.FTP(siteAdress) as ftp:
            ftp.login()
            ftpAutomatedComand(ftp, commandList)
    except ftplib.all_errors as error:
        print("Failed to connect. Check the adress and your credentials.\n", error)


# Connects to the ftp site without requiring a list of commands, this will call a function that allows you to perform different functions
def ftp_manual_connect():
    while True:  # break quits the loop
        siteAdress = input("What is the site address of the ftp you want to see?\n\
(The answer is probably 'www.3gpp.org')\n")
        try:
            with ftplib.FTP(siteAdress) as ftp:
                ftp.login()
                print(ftp.getwelcome())
                print('Current Directory',ftp.pwd())
                ftp.dir()
                print("Valid commands are [cd, get, ls, get_all_Tdocs, exit] - ex:get readme.txt")
                manual_ftp_command(ftp)
                break  # ftp_command will loop until the user says exit
        except ftplib.all_errors as error:
            print("Failed to connect. Check the address and your credentials.\n", error)


# This is what happens when you enter a command.
# Your command is taken and the appropriate function is called with appropriate arguments
def handle_command(ftp, command):
    if command[0] == 'cd':
        cd(ftp, command[1])

    elif command[0] == 'get':  # download file
        getFile(ftp, command[1])

    elif command[0] == 'ls':  # print directory listing
        print("Directory of ", ftp.pwd())
        ftp.dir()

    elif command[0] == 'exit':  # exit
        ftp.quit()

    elif command[0] == 'print_full_tree':  # print full tree
            print_tree_contents(ftp)

    elif command[0] == 'get_all_Tdocs':  # get all of the Tdocs
        get_all_Tdocs(ftp, '')


# Runs a list of commands
def ftpAutomatedComand(ftp, commandList):
    for i in range(0, len(commandList)):
        commands = commandList[i].split()
        handle_command(ftp, commands)


# Lets the user input an unlimited amount of commands and runs them all
def manual_ftp_command(ftp):
    while True:  # runs until break/exit
        command = input("Enter a command\n")  # Change to valid input later
        commands = command.split()
        handle_command(ftp, commands)
        if commands[0] == "exit":
            break


# Configures files in your directory to help organize things
# Looks at the documents folder (if it exists)
if 'documents' in os.listdir():
    print("The documents folder takes a long time to create.")
    confirm = validInput("Are you sure you want to delete the documents folder?(y/n)\n", ['y', 'n', 'yes', 'no']).lower()
    if any_phrase_occurs(confirm, ['y'], case_sensitive=False):
        shutil.rmtree('documents')
    else:
        print("That is probably safer, but you should probably get the documents folder out of this directory to help the program work correctly")
        continue_process = validInput("Are you ready to continue?\n", ['yes', 'y', 'ye'])

if 'all_tdocs.csv' in os.listdir():
    delete_all_tdocs = validInput("Would you like to delete the compilation of all the tdocs?('y'/'n). \n\
This action is strongly advised against unless you know your tdoc list is incorrect.\n", ['y', 'yes', 'n', 'no'])
    if any_phrase_occurs(delete_all_tdocs, ['y'], case_sensitive=False):
        os.remove('all_tdocs.csv')
    else:
        print("You probably made the correct choice")
        print("You should probably either terminate the program or move your tdoc file somewhere else")
        continue_process = validInput("Are you ready to continue?\n", ['yes', 'y', 'ye'])

if 'documents' not in os.listdir():
    os.mkdir('documents')
if 'all_tdocs.csv' not in os.listdir():
    file = open('all_tdocs.csv', 'w')
    file.close()


who_commands = validInput('Would you like to be able to type commands yourself, (kind of like in the terminal)\n\
or would you like the computer take care of everything for you? Input either "flexible" / "not flexible" or \n\
controller is "me" / "computer"\n', ["flexible", "not flexible", "me", "computer"])
if "me" in who_commands or who_commands == "flexible":
    print("OK I'll give you relatively free reign over what you chose to do now.\n")
    ftp_manual_connect()
else:
    choice = validInput("Do you want to download all the files, or just clean up your documents folder? ('download all'/'clean')\n", ['download', 'download all', 'clean']).lower()
    if any_phrase_occurs(choice, ['download'], case_sensitive=False):
        tdocCommands = ['cd tsg_ran/WG1_RL1', 'get_all_Tdocs', 'exit']
        ftpAutomatedConnect('www.3gpp.org', tdocCommands)
    else:
        print("Ok the cleaning will begin shortly")

    for file in os.listdir('documents'):
        if not any_phrase_occurs(file, ['tdoc'], case_sensitive=False):
            os.remove(os.path.join('documents', file))
        else:
            clean_tdoc(os.path.join('documents', file))


if 'documents' in os.listdir():
    print("The documents folder takes a long time to create.")
    print("But by now it might be empty")
    print("Here is a list of the contents of the document folder")
    print(os.listdir('documents'))
    confirm = validInput("Do you want to delete the documents folder?(y/n)\n", ['y', 'n', 'yes', 'no']).lower()
    if any_phrase_occurs(confirm, ['y'], case_sensitive=False):
        shutil.rmtree('documents')
    else:
        print("OK. the program may not have acted correctly so you should probably look to make sure it did.")



