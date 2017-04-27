# interpret() function is where you should start reading to understand this code.
# interpret() has to be called at the bottom of this file for things to work.


from sys import *
from importlib import import_module
import importlib.util


# functions:

def interpret():
    text = open_file(argv[1]) # so you can use this Terminal command: python interpreter.py text.txt
    text = text.lower() # lowercase
    sentences = get_sentences(text)
    # printplz('  DEBUG OUTPUT: ' + str(sentences))
    words_grouped = get_words_grouped_by_sentence(sentences)
    # printplz('  DEBUG OUTPUT: ' + str(words_grouped))
    run_commands(words_grouped)

def open_file(file_name):
    text = open(file_name, 'r').read()
    return text

def get_sentences(text):
    sentences = text.split('please') # each sentence is expected to begin with "please"
    return sentences

def get_words_grouped_by_sentence(sentences):
    word_groups = [] # instead of "= sentences", which would pass by reference
    for sentence in sentences:
        words = list(sentence.strip().split()) # no params for split so it uses any whitespace character
        word_groups.append(words)
    return word_groups

def run_commands(words_grouped):
    global last_spelled_word
    global last_variable
    global if_continue_state
    for sentence in words_grouped:
        # printplz('  DEBUG OUTPUT: ' + 'sentence = ' + str(sentence))
        words_count = len(sentence)
        for i, word in enumerate(sentence): # need to track number of words left in sentence while read each word
            if if_continue_state == False:
                # reset variable for next sentence
                if_continue_state = True
                # stop looking at next words and go to next sentence
                break
            elif if_continue_state == True:
                words_left = words_count - i
                sentence_data = sentence_info(word, words_left)
                if note_state == False:
                    last_spelled_word = check_spell(sentence_data)
                    if print_state == False:
                        last_variable = check_variable(sentence_data)
                        check_math(sentence_data)
                        check_assign(sentence_data) # put after variable and math
                        check_import(sentence_data)
                        check_use(sentence_data)
                        if_continue_state = check_if(sentence_data)
                    check_print(sentence_data) # put after assign to avoid recognition of keyword within print
                if print_state == False:
                    check_note(sentence_data)

"""
example:
Please print this string of words
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
            print_string += ' ' + word
        elif words_left == 1:
            print_string += ' ' + word
            print_string = print_string.strip() # .strip() removes leading and trailing spaces
            print(print_string)
            # reset variables
            print_state = False
            print_string = ''

"""
example:
Please one plus two
"""
def check_math(sentence_data):
    global math_state
    global math_string
    global math_result
    word = sentence_data.word
    words_left = sentence_data.words_left
    word_uses_math_keyword = (word in math_words_numbers or word in math_words_operators)
    if math_state == False and word_uses_math_keyword:
        math_state = True
        math_string = word
    elif math_state == True:
        if words_left > 1 and word_uses_math_keyword:
            math_string += ' ' + word
        elif words_left > 1 and not word_uses_math_keyword:
            math_string = math_string.strip()
            math_result = eval_math(translate_math(math_string))
            printplz('  DEBUG MATH: ' + str(math_result))
            # reset variables
            math_state = False
            math_string = ''
        elif words_left == 1:
            if word_uses_math_keyword:
                math_string += ' ' + word
            math_string = math_string.strip()
            math_result = eval_math(translate_math(math_string))
            printplz('  DEBUG MATH: ' + str(math_result))
            # temp = math_result
            # reset variables
            math_state = False
            math_string = ''
            math_result = ''
            # return temp

def translate_math(expression_string):
    global math_words_numbers
    output_string = ''
    expression = expression_string.split()
    for word in expression:
        if word in math_words_numbers:
            output_string += str(math_words_numbers[word])
        elif word in math_words_operators:
            output_string += str(math_words_operators[word])
    return output_string

def eval_math(expression):
    return eval(expression,{"__builtins__":None},{}) # use ,{"__builtins__":None},{} to make eval function safer

def is_math_expression(expression_string):
    return all((word in math_words_numbers or word in math_words_operators) for word in expression_string.split(' '))

"""
example:
Please spell with the first letters of Neptune unicorn moose panda Yoda
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
        spell_string += ' ' + word
        if words_left == 1:
            spell_string = spell_with_first_letters(spell_string)
            printplz('  DEBUG SPELL: ' + spell_string)
            temp = spell_string
            # reset variables
            spell_state = False
            spell_string = ''
            spell_phrase_index = 0
            return temp
    return ''

def spell_with_first_letters(sentence):
    local_sent = sentence.replace('spell with the first letters of ', '')
    words = local_sent.split()
    spelt_word = ''.join(list(word[0] for word in words))
    return spelt_word

"""
example:
Please import alternate
Please import test from library
Please import numpy as nectarine pony
"""
def check_import(sentence_data):
    global import_state
    global import_string
    global import_dictionary
    global as_state
    global as_string
    global spell_state
    global last_spelled_word
    global from_state
    global from_string
    word = sentence_data.word
    words_left = sentence_data.words_left
    if import_state == False and word == 'import':
        import_state = True
    elif import_state == True:
        if words_left > 1 and word != 'as' and word != 'from':
            if as_state == False and from_state == False:
                import_string += ' ' + word
            elif as_state == True:
                as_string += ' ' + word
            elif from_state == True:
                from_string += ' ' + word
        elif words_left > 1 and word == 'as' and as_state == False:
            as_state = True
        elif words_left > 1 and word == 'from' and from_state == False:
            from_state = True
        elif words_left == 1:
            dictionary_key = import_string
            if as_state == False and from_state == False:
                import_string += ' ' + word
                dictionary_key = import_string
            elif as_state == True:
                as_string += ' ' + word
                if last_spelled_word == '':
                    dictionary_key = as_string
                else:
                    dictionary_key = last_spelled_word
            elif from_state == True:
                from_string += ' ' + word
                #from_string = spell_with_first_letters(from_string)
                dictionary_key = import_string
            import_string = import_string.strip()
            dictionary_key = dictionary_key.strip()
            from_string = from_string.strip()
            printplz('  DEBUG IMPORT: import_string = ' + import_string)
            printplz('  DEBUG IMPORT: dictionary_key = ' + dictionary_key)
            if from_state == True:
                # importing from folder
                printplz('  DEBUG IMPORT: from_string = ' + from_string)
                # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
                spec = importlib.util.spec_from_file_location(import_string, from_string + '/' + import_string + '.py')
                module = importlib.util.module_from_spec(spec) # get module
                spec.loader.exec_module(module) # enables use of functions and variables from the module
            elif from_state == False:
                module = import_module(import_string)
            import_dictionary[dictionary_key] = module
            printplz('  DEBUG IMPORT: ' + str(import_dictionary))
            # reset variables
            import_state = False
            import_string = ''
            as_state = False
            as_string = ''
            spell_state = False
            from_state = False
            from_string = ''

"""
example:
Please use test_function of test
Please use test_function from test
"""
def check_use(sentence_data):
    global use_state
    global use_string
    global from_state
    global from_string
    word = sentence_data.word
    words_left = sentence_data.words_left
    if use_state == False and word == 'use':
        use_state = True
    elif use_state == True:
        if words_left > 1 and (word != 'of' and word != 'from') and from_state == False:
            use_string += ' ' + word
            # printplz('use_string ' + use_string)
        elif words_left > 1 and (word == 'of' or word == 'from'):
            from_state = True
            # printplz('from_state = True')
        elif words_left > 1 and from_state == True:
            from_string += ' ' + word
            from_string = from_string.strip()
            # printplz('from_string = ' + from_string)
        elif words_left == 1:
            if from_state == True:
                from_string += ' ' + word
                from_string = from_string.strip()
                # printplz('from_string = ' + from_string)
            use_string = use_string.strip()
            printplz('  DEBUG USE: ' + use_string)
            # printplz('from_string = ' + from_string)
            function_imported = getattr(import_dictionary[from_string], use_string)
            try:
                function_imported() # try to use function_imported as a function
            except:
                printplz(function_imported) # in case function_imported is just an output value
            # reset variables
            use_state = False
            use_string = ''
            from_state = False
            from_string = ''

"""
example:
Please create variable apple
Please variable banana
"""
def check_variable(sentence_data):
    global variable_state
    global variable_dictionary
    global variable_name
    word = sentence_data.word
    words_left = sentence_data.words_left
    if variable_state == False and word == 'variable':
        variable_state = True
    elif variable_state == True:
        if words_left > 1:
            variable_name += ' ' + word
        elif words_left == 1:
            variable_name += ' ' + word
            variable_name = variable_name.strip()
            if variable_name not in variable_dictionary:
                variable_dictionary[variable_name] = ''
                printplz('  DEBUG CREATE NEW VAR: ' + variable_name)
            printplz('  DEBUG variable_name: ' + variable_name)
            printplz('  DEBUG variable_dictionary: ' + str(variable_dictionary))
            temp = variable_name
            # reset variables
            variable_state = False
            variable_name = ''
            return temp

"""
example:
Please assign one to variable apple
Please assign three hundred to variable banana
Please assign some words to variable coconut
"""
def check_assign(sentence_data):
    global assign_state
    global assign_to_state
    global assign_string
    global assign_to_string
    global variable_name
    global variable_dictionary
    global math_state
    global math_string
    global math_result
    global last_variable
    word = sentence_data.word
    words_left = sentence_data.words_left
    if assign_state == False and word == 'assign':
        assign_state = True
    elif assign_state == True:
        if words_left > 1 and word != 'to' and assign_to_state == False:
            assign_string += ' ' + word
            assign_string = assign_string.strip()
        elif words_left > 1 and word == 'to':
            assign_to_state = True
        elif words_left > 1 and assign_to_state == True:
            assign_to_string += ' ' + word
            # let check_variable() get variable name
        elif words_left == 1:
            # printplz('  DEBUG math_state = ' + str(math_state))
            # printplz('  DEBUG math_result ' + str(math_result))
            # printplz('  DEBUG assign_string ' + str(assign_string))
            # printplz('  DEBUG assign_string in math_words_numbers ' + str(assign_string in math_words_numbers))
            # printplz('  DEBUG all words in assign_string are math: check: ' + is_math_expression(assign_string))
            if math_state == False and math_result != '' and is_math_expression(assign_string):
                assign_string = math_result
            # printplz('  DEBUG variable_state ' + str(variable_state))
            if variable_state == False:
                assign_to_string = last_variable
                # printplz('  DEBUG last_variable = ' + last_variable)
            printplz('  DEBUG assign_string: ' + str(assign_string))
            variable_dictionary[assign_to_string] = assign_string
            printplz('  DEBUG assign_to_string: ' + assign_to_string)
            printplz('  DEBUG variable_dictionary: ' + str(variable_dictionary))
            # reset variables
            assign_state = False
            assign_to_state = False
            assign_string = ''

"""
example:
Please if one equals one then print it works
Please if one equals two then print it should not print this
"""
def check_if(sentence_data):
    global if_state
    global if_continue_state
    global math_result
    word = sentence_data.word
    words_left = sentence_data.words_left
    # printplz('  DEBUG words_left ---> ' + str(words_left))
    if if_state == False:
        if word == 'if':
            if_state = True
            printplz('  DEBUG IF')
        if_continue_state = True # reset variable to eval new if statement
        return if_continue_state
    elif if_state == True:
        if word == 'then':
            printplz('  DEBUG detect math within if statement: ' + str(math_result))
            printplz('  DEBUG THEN')
            if_continue_state = math_result
            if_state = False # reset variable
            return if_continue_state
        else:
            if_continue_state = True
            return if_continue_state

"""
example:
Please note this is a comment
"""
def check_note(sentence_data):
    global note_state
    word = sentence_data.word
    words_left = sentence_data.words_left
    if note_state == False and word == 'note':
        note_state = True
    elif note_state == True and words_left == 1:
        note_state = False # reset variable

"""
enable/disable debug print outputs
"""
def printplz(string):
    global hide_debug_printouts
    if hide_debug_printouts == False:
        print(string)
    elif hide_debug_printouts == True and '  DEBUG' != string[0:7]:
        print(string)


# initialize global variables:
hide_debug_printouts = False # True
print_state = False
print_string = ''
math_state = False
math_string = ''
math_result = ''
math_words_numbers = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,
                      'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,
                      'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19,
                      'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90,
                      'hundred':'00','thousand':'000','million':'000000','billion':'000000000','trillion':'000000000',
                      '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
math_words_operators = {'plus':'+','minus':'-','times':'*','divide':'/','equals':'=='}
spell_state = False
spell_string = ''
spell_phrase_index = 0
spell_checkphrase = ['spell','with','the','first','letters','of']
import_state = False
import_string = ''
import_dictionary = {}
as_state = False
as_string = ''
use_state = False
use_string = ''
from_state = False
from_string = ''
note_state = False
variable_state = False
variable_dictionary = {}
variable_name = ''
assign_state = False
assign_string = ''
assign_to_state = False
assign_to_string = ''
last_spelled_word = ''
last_variable = ''
if_state = False
if_continue_state = True
class sentence_info():
    word = ''
    words_left = 0
    def __init__(self, word, words_left):
        self.word = word
        self.words_left = words_left


printplz('\nPLEASE WORK...\n')
# run this interpreter:
interpret()
printplz('\n...THANK YOU!\n')