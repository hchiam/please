from sys import *

def open_file(file_name):
    text = open(file_name, 'r').read()
    return text

def get_words(text):
    words = text.split(' ')
    print(words)

def interpret():
    text = open_file(argv[1])
    get_words(text)

interpret()