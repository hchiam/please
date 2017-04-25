from sys import *


# global variables
print_state = False
print_string = ''
class sentence_info():
    word = ''
    words_left = 0
    def __init__(self, word, words_left):
        self.word = word
        self.words_left = words_left


# functions

def interpret():
    text = open_file(argv[1])
    text = text.lower()
    get_words(text)

def open_file(file_name):
    text = open(file_name, 'r').read()
    return text

def get_words(text):
    sentences = text.split('please')
    for sentence in sentences:
        words = sentence.split(' ')
        # print(words)
        words_count = len(words)
        for i, word in enumerate(words):
            words_left = words_count - i
            sentence_data = sentence_info(word, words_left)
            check_print(sentence_data)

def check_print(sentence_data):
    global print_state
    global print_string
    word = sentence_data.word
    words_left = sentence_data.words_left
    if word == 'print':
        print_state = True
    elif print_state == True:
        if words_left > 1:
            if print_string != '':
                print_string += ' ' + word
            else:
                print_string += word
        elif words_left == 1:
            print_string += ' ' + word
            print(print_string)
            # reset print variables
            print_state = False
            print_string = ''


# run interpreter
interpret()