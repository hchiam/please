from sys import *


# functions:

def interpret():
    text = open_file(argv[1]) # to use this Terminal command: python interpreter.py text.txt
    text.lower() # lowercase
    sentences = get_sentences(text)
    # print(sentences)
    words_grouped = get_words_grouped_by_sentence(sentences)
    # print(words_grouped)
    check_commands(words_grouped)

def open_file(file_name):
    text = open(file_name, 'r').read()
    return text

def get_sentences(text):
    sentences = text.split('please')
    return sentences

def get_words_grouped_by_sentence(sentences):
    word_groups = [] # instead of "= sentences", which would pass by reference
    for i in range(len(sentences)):
        words = list(sentences[i].strip().split(' '))
        word_groups.append(words)
    return word_groups

def check_commands(words_grouped):
    for sentence in words_grouped:
        # print('sentence = ' + str(sentence))
        words_count = len(sentence)
        for i, word in enumerate(sentence):
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


# initialize global variables:
print_state = False
print_string = ''
class sentence_info():
    word = ''
    words_left = 0
    def __init__(self, word, words_left):
        self.word = word
        self.words_left = words_left


# run this interpreter:
interpret()