# code text formatter
# Puts "please" at every new line
# Puts indents when it sees if (and later for loops, and de-indents at any end-if's).


from sys import *
from importlib import import_module
import importlib.util


progress_bar = ''

def clean():
    print('---Formatter Starting---')
    file_name = '../text.txt'
    text = get_text(file_name)
    update_progress_bar_display()
    text_lines = reformat(text)
    rewrite_file(file_name, text_lines)
    print('---Formatter Finished---')

def get_text(file_name):
    # with open(file_name, 'r') as f:
    #     text = f.readlines()
    # return text
    # just get one long string to parse
    return open(file_name, 'r').read()

def reformat(text):
    # put each "please" at every new line
    text_lines = text.lower().split('please')
    
    # TRY THIS : REGEX FIND NOT \N PLEASE AND ONLY REPLACE PLEASE WITHOUT \N BEFORE IT
    
    # put indents when it sees if (and later for loops, and de-indents at any end-if's).
    return text_lines

def rewrite_file(file_name, text):
    # create or clear formatted file
    open(file_name[:-4]+'_formatted.txt', 'w').write('')
    # append each new line of text
    for line in text:
        with open(file_name[:-4]+'_formatted.txt', 'a') as f:
            f.write(line)
            update_progress_bar_display()

def update_progress_bar_display():
    global progress_bar
    progress_bar += '_'
    print(progress_bar)

clean()
