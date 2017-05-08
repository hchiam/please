# code text formatter
# Puts "please" at every new line

"""
FUTURE: Puts indents when it sees if-statements (and later for-loops, and de-indents at any end-if's).
"""

import sys
import re



def clean():
    file_name = 'text.txt'
    text = ''
    print('\n---Formatter Starting---\n')
    # first try getting from folder above
    file_name_dir = '../'+file_name
    try:
        text = get_text(file_name_dir)
    except:
        # then try getting from local folder
        try:
            file_name_dir = file_name
            text = get_text(file_name_dir)
        except:
            print('\n***FILE NOT FOUND***\n')
    update_progress_bar_display()
    text = reformat(text)
    rewrite_file(file_name, text)
    finish_progress_bar_display()
    print('\n---Formatter Finished---\n')

def get_text(file_name):
    # with open(file_name, 'r') as f:
    #     text = f.readlines()
    # return text
    # just get one long string to parse
    return open(file_name, 'r').read()

def reformat(text):
    # put each "please" at new lines
    text = text.lower().replace(' please','\nplease') # just one long string to parse
    
    # FUTURE: put indents when it sees if-statements (and later for-loops, and de-indents at any end-if's).
    text = format_lines(text)
    
    return text

def format_lines(text):
    # edit line by line instead of as one long string (so can track indents)
    sentences = text.split('please')[1:] # index 0 is []
    text = ''
    num_indents = 0
    newline_after_endif = False
    for sentence in sentences:
        # immediately de-indent an end-if line
        if sentence[:7] == ' end if' or sentence[:8] == ' end for' or sentence[:13] == ' end function': # or sentence[:10] == ' end class':
            num_indents -= 1
            newline_after_endif = True
        # remove multiple consecutive space characters per line
        sentence = remove_multi_spaces(sentence)
        # add indents as needed
        text += '\t'*num_indents + 'please ' + sentence + '\n' + newline_after_endif*'\n'
        # indent the next line after a if-statement (multiline ones, not the one-liner if-statements)
        checkphrase = '.*if (.+) then$' # $ for end of sentence
        is_multiline_if_statement = re.match(checkphrase, sentence)
        if is_multiline_if_statement or sentence[:4] == 'for ' or sentence[:16] == 'define function ': # or sentence[:14] == 'define class ':
            num_indents += 1
        # reset
        newline_after_endif = False
    return text

def remove_multi_spaces(sentence):
    return ' '.join(sentence.strip().split())

def rewrite_file(file_name, text):
    put_in_library_folder = 'library/'
    new_file_name = put_in_library_folder + file_name[:-4] + '_FORMATTED.txt'
    # create or clear formatted file
    open(new_file_name, 'w').write('')
    # append each new line of text
    for line in text:
        with open(new_file_name, 'a') as f:
            f.write(line)
            update_progress_bar_display()

def update_progress_bar_display():
    sys.stderr.write('.') # adds to Terminal output without creating new line

def finish_progress_bar_display(): # so that print() starts on new line
    sys.stderr.write('\n')



if __name__ == '__main__': # only perform the following if running this file directly
    clean()
