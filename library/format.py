# code text formatter
# Puts "please" at every new line

"""
# FUTURE: Puts indents when it sees if-statements (and later for-loops, and de-indents at any end-if's).
"""

from sys import *
from importlib import import_module
import importlib.util


progress_bar = ''

def clean():
    print('\n---Formatter Starting---')
    file_name = '../text.txt'
    text = get_text(file_name)
    update_progress_bar_display()
    text = reformat(text)
    rewrite_file(file_name, text)
    print('---Formatter Finished---\n')

def get_text(file_name):
    # with open(file_name, 'r') as f:
    #     text = f.readlines()
    # return text
    # just get one long string to parse
    return open(file_name, 'r').read()

def reformat(text):
    # put each "please" at every new line
    text = text.lower().replace('\n ','\n').replace(' please','\nplease') # just one long string to parse
    
    # FUTURE: put indents when it sees if-statements (and later for-loops, and de-indents at any end-if's).
    
    return text

def rewrite_file(file_name, text):
    new_file_name = file_name[:-4]+'_FORMATTED.txt'
    # create or clear formatted file
    open(new_file_name, 'w').write('')
    # append each new line of text
    for line in text:
        with open(new_file_name, 'a') as f:
            f.write(line)
            update_progress_bar_display()

def update_progress_bar_display():
    global progress_bar
    progress_bar += '.'
    print(progress_bar)

clean()
