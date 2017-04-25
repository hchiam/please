from sys import *


# functions:

def interpret():
    text = open_file(argv[1]) # so you can use this Terminal command: python interpreter.py text.txt
    text = text.lower() # lowercase
    sentences = get_sentences(text)
    # print(sentences)
    words_grouped = get_words_grouped_by_sentence(sentences)
    # print(words_grouped)
    run_commands(words_grouped)

def open_file(file_name):
    text = open(file_name, 'r').read()
    return text

def get_sentences(text):
    sentences = text.split('please')
    return sentences

def get_words_grouped_by_sentence(sentences):
    word_groups = [] # instead of "= sentences", which would pass by reference
    for sentence in sentences:
        words = list(sentence.strip().split(' '))
        word_groups.append(words)
    return word_groups

def run_commands(words_grouped):
    for sentence in words_grouped:
        # print('sentence = ' + str(sentence))
        words_count = len(sentence)
        for i, word in enumerate(sentence): # need to track number of words left in sentence while read each word
            words_left = words_count - i
            sentence_data = sentence_info(word, words_left)
            check_print(sentence_data)
            check_math(sentence_data)
            check_spell(sentence_data)

"""
example:
please print this string of words
"""
def check_print(sentence_data):
    global print_state
    global print_string
    word = sentence_data.word
    words_left = sentence_data.words_left
    if print_state == False and word == 'print':
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
            # reset variables
            print_state = False
            print_string = ''

"""
example:
please one plus two
"""
def check_math(sentence_data):
    global math_state
    global math_string
    word = sentence_data.word
    words_left = sentence_data.words_left
    uses_math_keyword = (word in math_words_numbers or word in math_words_operators)
    if math_state == False and uses_math_keyword:
        math_state = True
        math_string += word
    elif math_state == True:
        if words_left > 1 and uses_math_keyword:
            if math_string != '':
                math_string += ' ' + word
            else:
                math_string += word
        elif words_left > 1 and not uses_math_keyword:
            print(eval_math(translate_math(math_string)))
            # reset variables
            math_state = False
            math_string = ''
        elif words_left == 1:
            if uses_math_keyword:
                math_string += ' ' + word
            print(eval_math(translate_math(math_string)))
            # reset variables
            math_state = False
            math_string = ''

def translate_math(expression_string):
    global math_words_numbers
    output_string = ''
    expression = expression_string.split(' ')
    for word in expression:
        if word in math_words_numbers:
            output_string += str(math_words_numbers[word])
        elif word in math_words_operators:
            output_string += str(math_words_operators[word])
    return output_string

def eval_math(expression):
    return eval(expression,{"__builtins__":None},{}) # use ,{"__builtins__":None},{} to make eval function safer

"""
example:
please spell with the first letters of
Neptune unicorn moose panda Yoda
"""
def check_spell(sentence_data):
    global spell_state
    global spell_string
    global spell_phrase_index
    global spell_checkphrase
    word = sentence_data.word
    words_left = sentence_data.words_left
    if spell_state == False:
        checkword = spell_checkphrase[spell_phrase_index]
        if word == checkword:
            if spell_phrase_index == len(spell_checkphrase)-1:
                spell_state = True
            else:
                spell_phrase_index += 1
        else:
            spell_phrase_index = 0
    elif spell_state == True:
        if words_left > 1:
            spell_string += word[0]
        elif words_left == 1:
            spell_string += word[0]
            print(spell_string)
            # reset variables
            spell_state = False
            spell_string = ''
            spell_phrase_index = -1


# initialize global variables:
print_state = False
print_string = ''
math_state = False
math_string = ''
math_result = ''
math_words_numbers = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'hundred':'00','thousand':'000','million':'000000','billion':'000000000','trillion':'000000000'}
math_words_operators = {'plus':'+','minus':'-','times':'*','divide':'/'}
spell_state = False
spell_string = ''
spell_phrase_index = 0
spell_checkphrase = ['spell','with','the','first','letters','of']
class sentence_info():
    word = ''
    words_left = 0
    def __init__(self, word, words_left):
        self.word = word
        self.words_left = words_left


# run this interpreter:
interpret()