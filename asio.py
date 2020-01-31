#!/usr/bin/env python3
#Alan's Simple IO module (ASIO)

#The purpose of this module is to make IO simpler.
#You can open a file with a single function call.
#You can write data to a file with a single function call.
#You can open and load data from a file with a single function call.
#You can download a file with a single function call.
#You can download a file and write it to disk with a single function call.


import sys
import requests
import io
import os
import shutil


#=====Exception functions=====
#used for many functions in this module
#exits when there's an exception
def ex_exit(e):
    print(e)
    print(e.args)
    sys.exit(1)

#displays a message about the exception
def ex_msg(filename, e, e_str, operation):
    msg = "(" + e_str + ") IO exception when " + operation
    msg += " " + filename + ":"
    print(msg)
    ex_exit(e)



#=====Deletion functions=====

#delete a file that is assumed to exist
def delete(filename):
    try:
        os.remove(filename)
    except IOError as e:
        ex_msg(filename, e, "delete", "deleting")

#clear the contents of a file
def clear_file(filename):
    try:
        f = open(filename, "w")
        f.write("")
        f.close()
    except IOError as e:
        ex_msg(filename, e, "clear_file", "clearing")

#confirmation
#exampe usage: confirm("example.txt", "delete")
def confirm(operation, filename):
    question = "Are you sure you want to "
    question += operation + " " + filename + "? y/n: "
    choice = input(question)
    if ((choice.lower() == "n") or (choice.lower() == "no")):
        #user does not want to proceed with IO operation
        return False
    else:
        return True

#ask a user before deleting something
def confirm_delete(filename):
    if (confirm("delete", filename)):
        delete(filename)

#delete all files in a given directory
#but does not delete the folder itself
def clear_directory(folder):
    for filename in os.listdir(folder):
        delete(filename)

#delete an entire directory
def delete_directory(folder):
    try:
        shutil.rmtree(folder)
    except IOError as e:
        ex_msg(folder, e, "delete_directory", "deleting")

#when delete_directory() doesn't work, try this force_delete instead
#but be very careful when using it!
def force_delete_directory(folder):
    try:
        #exit the program if this function is used in an unsafe way
        if ((folder == "/") or ("no-preserve-root" in folder)):
            print("Error: dangerous usage of force_delete_directory()!")
            print("Argument provided: " + str(folder))
            print("Exiting")
            sys.exit(1)
        #proceed with deletion
        cli_str = "rm -rf " + str(folder)
        os.system(cli_str)
    except IOError as e:
        ex_msg(folder, e, "force_delete_directory", "force-deleting")

#make a new directory
def make_directory(folder):
    try:
        os.mkdir(folder)
    except IOError as e:
        ex_msg(folder, e, "make_directory", "creating directory")

#=====Existence functions=====
#check if file exists
def exists(filename):
    try:
        return os.path.exists(filename)
    except IOError as e:
        ex_msg(filename, e, "exists", "reading")

def does_not_exist(filename):
    try:
        return (not os.path.exists(filename))
    except IOError as e:
        ex_msg(filename, e, "does_not_exist", "reading")

#check if a file exists, and then delete it if it does
def delete_if_exists(filename):
    if (exists(filename)):
        delete(filename)

#create a new blank file if it does not exist
def create_if_dne(filename):
    if (does_not_exist(filename)):
        clear_file(filename)


#=====Write functions=====

#functions that start in "write" are OVERWRITE functions

#function for safely downloading utf8 text data
#won't work for binary files i.e. jpeg or exe
#usage example: safe_write_text("something.html", response.text)
def write_utf8(filename, data):
    try:
        write_file = io.open(filename, "w", encoding="utf-8")
        write_file.write(data)
        write_file.close()
    except IOError as e:
        ex_msg(filename, e, "write_utf8", "writing")


#regular text file write function
#example: safe_write("results.xml", response.text)
def write_text(filename, data):
    try:
        write_file = open(filename, "w")
        write_file.write(data)
        write_file.close()
    except IOError as e:
        ex_msg(filename, e, "write_text", "writing")

#write binary data to a file
#example: write_binary("something.jpg", response.content)
def write_binary(filename, data):
    try:
        write_file = open(filename, "wb")
        write_file.write(data)
        write_file.close()
    except IOError as e:
        ex_msg(filename, e, "write_binary", "writing")

#create a blank file
def create_blank(filename):
    clear_file(filename)


#=====Copy functions=====
def copy_file(filename):
    print("not done")

def copy_directory(folder):
    print("not done")

def move_file(filename):
    print("not done")

def move_directory(folder):
    print("not done")



#=====Append functions=====
#append operations
#append mode for binary: "r+b"

#append utf8
def append_utf8(filename, append_data):
    if (exists(filename)):
        try:
            write_file = io.open(filename, "a", encoding="utf-8")
            write_file.write(append_data)
            write_file.close()
        except IOError as e:
            ex_msg(filename, e, "append_utf8", "appending")


#append text
def append_text(filename, append_data):
    if (exists(filename)):
        try:
            append_file = open(filename, "a")
            append_file.write(append_data)
            append_file.close()
        except IOError as e:
            ex_msg(filename, e, "append_text", "appending")



#append binary
def append_binary(filename, append_data):
    if (exists(filename)):
        try:
            append_file = open(filename, "ab")
            append_file.write(append_data)
            append_file.close()
        except IOError as e:
            ex_msg(filename, e, "append_binary", "appending")

#DNE: Does Not Exist
#write data to a given filename
#if a file with that filename doesn't already exist
def write_dne_utf8(filename, data):
    if (does_not_exist(filename)):
        write_utf8(filename, data)

#write if does not exist text

def write_dne_text(filename, data):
    if (does_not_exist(filename)):
        write_text(filename, data)

#write if does not exist binary
def write_dne_binary(filename, data):
    if (does_not_exist(filename)):
        write_binary(filename, data)


#to-do
#write to a new file if it does not exist already
#if it does exist, then append to it

#write new file if it doesn't exist
#or append if it does
#for utf8
def wa_utf8(filename, data):
    if (does_not_exist(filename)):
        write_utf8(filename, data)
    else:
        append_utf8(filename, data)

#write new file if it doesn't exist
#or append if it does
#for text (ascii)
def wa_text(filename, data):
    if (does_not_exist(filename)):
        write_text(filename, data)
    else:
        append_text(filename, data)

#write new file if it doesn't exist
#or append if it does
#for binary data
def wa_binary(filename, data):
    if (does_not_exist(filename)):
        write_binary(filename, data)
    else:
        append_binary(filename, data)




#=====Download functions=====

#spoof user agent, makes crawling and whatnot easier
#without this, you'd probably get a 403 forbidden error
#quite a lot of the time
def get_user_agent():
    ua_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    return ua_headers

#function for safely downloading a web page
#returns the response object
#if you want to write the response object to a file, do something like
#response.text
def download(dl_url):
    dl_headers = get_user_agent()
    response = ""
    try:
        response = requests.get(dl_url, dl_headers)
    except requests.RequestException as e:
        print("Request exception:")
        ex_exit(e)
    status = response.status_code
    #HTTP 200 means OK
    if (status != 200):
        print("Error code: " + str(status))
        sys.exit(1)
    elif (response == ""):
        print("Response error")
        sys.exit(1)
    else:
        #file downloaded successfully, but it's only stored in RAM,
        #not written to disk at this point
        return response

#~~~Functions that download files and then write to disk~~~

#download and save binary
def dl_write_bin(dl_url, filename):
    response = download(dl_url)
    write_binary(filename, response.content)


#download and save text
def dl_write_text(dl_url, filename):
    response = download(dl_url)
    write_text(filename, response.text)


#download and save UTF-8
def dl_write_utf8(dl_url, filename):
    response = download(dl_url)
    write_utf8(filename, response.text)




#=====Open functions=====

#open (for reading) and return UTF-8

def open_utf8(filename):
    try:
        return io.open(filename, "r", encoding="utf-8")
    except IOError as e:
        ex_msg(filename, e, "open_utf8", "opening")

#open and return text
def open_text(filename):
    try:
        return open(filename, "r")
    except IOError as e:
        ex_msg(filename, e, "open_text", "opening")

#open and return binary
def open_binary(filename):
    try:
        return open(filename, "rb")
    except IOError as e:
        ex_msg(filename, e, "open_binary", "opening")




#=====Search functions=====

#search utf8-encoded file for a certain string
def search_utf8(str_to_find, filename):
    try:
        file_to_search = open(filename, encoding="utf8", mode="r")
        if str_to_find in file_to_search.read():
            file_to_search.close()
            return True
        else:
            file_to_search.close()
            return False
    except IOError as e:
        ex_msg(filename, e, "search_utf8", "searching")

#search text file for a certain string
def search_text(str_to_find, filename):
    try:
        file_to_search = open(filename, "r")
        if str_to_find in file_to_search.read():
            file_to_search.close()
            return True
        else:
            file_to_search.close()
            return False
    except IOError as e:
        ex_msg(filename, e, "search_text", "searching")

#search binary file for certain data
def search_binary(data_to_find, filename):
    try:
        file_to_search = open(filename, "rb")
        if data_to_find in file_to_search.read():
            file_to_search.close()
            return True
        else:
            file_to_search.close()
            return False
    except IOError as e:
        ex_msg(filename, e, "search_binary", "searching")



#return a single line that contains a search term
#from a utf-8 file
def utf8_get_line_with(str_to_find, filename):
    try:
        #open file and read line by line
        if (exists(filename)):
            search_file = open_utf8(filename)
            line = search_file.readline()
            while line:
                if (str_to_find in line):
                    search_file.close()
                    return line
                line = search_file.readline()
            search_file.close()
            return "not_found"
    except IOError as e:
        ex_msg(filename, e, "get_line_contains", "searching")




#return single line that contains a search term
#from a text file
def text_get_line_with(str_to_find, filename):
    print("not done")

#return single line that contains certain data
#from a binary file
def binary_get_line_with(data_to_find, filename):
    print("not done")


#take a string that has stuff at the beginning and end, and get a string out of it
#assumes that you've already searched to see if the string is in fact in the line

#find the last instance of a string that starts with beginning and ends in ending
#from a big line string called line
#example:
#example_string = "http://example.com http://google.com/whatever"
#output = get_last_string_from_line_utf8("http", "com", example_string)
#print(output)
#http://google.com
#this one is used for downloading example files, don't mess with it
#if you want different string-slicing behavior, make another function
def get_last_string_from_line_utf8(beginning, ending, line):
    start_index = line.rfind(beginning)
    line = line[start_index:]
    end_index = line.find(ending)
    end_index = end_index + 1
    line = line[:end_index]
    return line


#this one is... ehhh... not very well done
#it works for my specific use in clone_all.py
#also ends 1 index value earlier than normal
#which is intended for a specific use-case but not for general stuff
def get_first_string_from_line_utf8(beginning, ending, line):
    start_index = line.find(beginning)
    line = line[start_index:]
    end_index = line.find(ending)
    line = line[:end_index]
    return line
#the above function is used for getting repo links from downloaded html github repo pages



#find last instance of string from text line
#that starts with a certain string and ends with another string
#print(get_last_string_from_line_text("abc", "def", "123abcdefabcAAAdef444"))
#result: abcAAAdef
def get_last_string_from_line_text(beginning, ending, line):
    print("not done")

#find last instance of data from binary data
def get_last_string_from_line_binary(beginning, ending, line_data):
    print("not done")



#get all lines with a search string

#get all lines in a utf8-encoded file that contain a string
#appends to the list that is passed into the function as an arg
def utf8_get_lines_with(str_to_find, filename, line_list):
    found_at_least_one = False
    try:
        #open file and read line by line
        if (exists(filename)):
            search_file = open_utf8(filename)
            line = search_file.readline()
            while line:
                if (str_to_find in line):
                    #add search result to the list
                    line_list.append(line)
                    found_at_least_one = True
                line = search_file.readline()
            search_file.close()

    except IOError as e:
        ex_msg(filename, e, "utf8_get_lines_with", "searching")


#get all lines in a text file
#that contain a certain string
def text_get_lines_with(str_to_find, filename, line_list):
    print("not done")

#get all lines in a binary file
#that contain certain data
def binary_get_lines_with(str_to_find, filename, line_list):
    print("not done")


#clean multiple lines instead of just one
#like get_last_string_from_line_utf8 but for a list of lines
def clean_lines_utf8(beginning, ending, line_list):
    #I think I can just use get_last_string_from_line_utf8 and a loop
    for i in range(0, len(line_list)):
        line_list[i] = get_first_string_from_line_utf8(beginning, ending, line_list[i])








def clean_lines_text(beginning, ending, line_list):
    print("not done")

def clean_lines_binary(beginning, ending, line_list):
    print("not done")


#find first occurrence in a file and replace with something else

def find_replace_one_utf8(str_to_find, filename):
    print("not done")

def find_replace_one_text(str_to_find, filename):
    print("not done")

def find_replace_one_binary(str_to_find, filename):
    print("not done")




#find all occurences in a file and replace them with something else

def find_replace_all_utf8(str_to_find, filename):
    print("not done")

def find_replace_all_text(str_to_find, filename):
    print("not done")

def find_replace_all_binary(data_to_find, filename):
    print("not done")






#=====TO-DO=====


#=====Upload functions=====

#https://stackoverflow.com/questions/68477/send-file-using-post-from-a-python-script

#upload utf-8 file
def post_utf8(post_url, filename):
    print("not done")

#upload text file
def post_text(post_url, filename):
    print("not done")

#upload binary file
def post_binary(post_url, filename):
    print("not done")

#=====FTP functions=====

def ftp_dl_file():
    print("not done")

def ftp_upload_file():
    print("not done")

