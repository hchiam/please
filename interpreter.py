from sys import *


# global variables
print_state = False
print_string = ''


# functions

def interpret():
    text = open_file(argv[1])
    text = text.lower()
    get_words(text)

def open_file(file_name):
    text = open(file_name, 'r').read()
    return text

def get_words(text):
    words = text.split(' ')
    for word in words:
        check_print(word)

def check_print(word):
    global print_state
    global print_string
    if word == 'print':
        print_state = True
    elif print_state == True:
        if word != 'please':
            if print_string != '':
                print_string += ' ' + word
            else:
                print_string += word
        elif word == 'please':
            print(print_string)
            # reset print variables
            print_state = False
            print_string = ''
    elif word == 'please':
        # reset all variables?
        print_state = False
        print_string = ''


# run interpreter
interpret()