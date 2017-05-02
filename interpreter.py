# interpret() function is where you should start reading to understand this code.
# interpret() has to be called at the bottom of this file for things to work.

from sys import *
import re
from importlib import import_module
import importlib.util



# functions:

def interpret():
    file_name = argv[1] # so you can use this Terminal command: python interpreter.py text.txt
    text = get_text(file_name)
    text = text.lower() # lowercase
    text = remove_multi_spaces(text)
    sentences = get_sentences(text)
    run_commands(sentences)

def get_text(file_name):
    text = open(file_name, 'r').read() # for example: file_name = "text.txt"
    return text

def remove_multi_spaces(text):
    return ' '.join(text.split())

def get_sentences(text):
    # each sentence is expected to begin with "please "
    sentences = text.split('please ')[1:] # assume index [0] is always empty or invalid before the first "please "
    return sentences

def run_commands(sentences):
    global keep_going
    for sentence in sentences:
        sentence = sentence.strip()
        # note: order matters, like order of replacing words or ignoring rest of sentence:
        # note > if > spell > print > variable > math, assign, import, use
        is_note = check_note(sentence)
        if is_note:
            continue # ignore this sentence
        keep_going = check_if(sentence) # whether to not ignore lines after an if-statement
        if keep_going:
            sentence = check_spell(sentence)
            is_print = check_print(sentence)
            if is_print:
                continue # do not try to interpret the rest of the sentence, just go straight to next sentence
            check_variable(sentence)
            check_assign(sentence)
            sentence = check_math(sentence) # math after assign: avoid creating variables named None
            check_import(sentence)
            check_use(sentence)

def get_words(sentence):
    words = sentence.strip().split() # .split() with no params splits at any whitespace character
    return words

"""
example:
Please note this is a comment
"""
def check_note(sentence):
    words = get_words(sentence)
    if words[0] == 'note':
        return True
    else:
        return False

"""
example:
Please print this string of words
"""
def check_print(sentence):
    words = get_words(sentence)
    if words[0] == 'print':
        print(' '.join(words[1:]))
        return True
    else:
        return False

"""
example:
Please spell with the first letters of Neptune unicorn moose panda Yoda
"""
def check_spell(sentence):
    global spell_checkphrases
    global spell_finish_words
    count = 0
    partial_checks = []
    # find matches in sentence:
    for phrase_start in spell_checkphrases:
        for phrase_stop in spell_finish_words:
            checkphrase = '.*' + phrase_start + ' ' + '(.+)' + phrase_stop
            matches = re.match(checkphrase, sentence)
            if matches:
                words_to_spell_with = matches.group(1) # this is substring found inside '(.+)'
                spelt_word = spell_with_first_letters(checkphrase, words_to_spell_with)
                print('  DEBUG SPELL: spelt_word=' + spelt_word)
                # print(sentence)
                phrase_to_replace = phrase_start + ' ' + words_to_spell_with
                sentence = sentence.replace(phrase_to_replace, spelt_word + ' ')
                # print(sentence)
    # alternate idea:
        # get indices and then find words between
        # [indices.start() for indices in re.finditer('test', 'test test test test')]
    return sentence

def spell_with_first_letters(checkphrase, sentence):
    local_sent = sentence.replace(checkphrase, '')
    words = local_sent.split()
    spelt_word = ''.join(list(word[0] for word in words))
    return spelt_word

"""
example:
Please create variable apple
Please variable banana
"""
def check_variable(sentence):
    global variable_dictionary
    checkphrase = '.*' + 'variable ' + '(.+)'
    matches = re.match(checkphrase, sentence)
    if matches:
        variable_name = matches.group(1) # this is substring found inside '(.+)'
        if variable_name not in variable_dictionary:
            variable_dictionary[variable_name] = None
        print('  DEBUG variable_dictionary: ' + str(variable_dictionary))

"""
example:
Please one plus two
"""
def check_math(sentence):
    words = get_words(sentence)
    math_expression = ''
    replace_expression = ''
    # need to find math expressions word-by-word (since sometimes embedded in sentences like if...then)
    for i in range(len(words)):
        word = words[i]
        if word in math_words_numbers:
            # sentence = sentence.replace(word, str(math_words_numbers[word]))
            math_expression += str(math_words_numbers[word])
            replace_expression += ' ' + word
        elif word.isdigit():
            math_expression += str(word)
            replace_expression += ' ' + word
        elif word in math_words_operators:
            # sentence = sentence.replace(word, math_words_operators[word])
            math_expression += math_words_operators[word]
            replace_expression += ' ' + word
        elif word in variable_dictionary:
            # sentence = sentence.replace(word, str(variable_dictionary[word]))
            math_expression += str(variable_dictionary[word])
            replace_expression += ' ' + word
        else: # non-math word detected; time to evaluate expression so far
            try:
                math_result = eval_math(math_expression)
                print('  DEBUG MATH: ' + math_expression + ' -> ' + str(math_result) + ' \t replace_expression = ' + replace_expression)
                # if the math works, then replace the section of the sentence
                replace_expression = replace_expression.strip() # to make sure replaces properly
                sentence = sentence.replace(replace_expression, str(math_result))
            except:
                pass
            # reset variables
            math_expression = ''
            replace_expression = ''
        # separate if-statement for end of sentence; time to evaluate (may (not) have been a math word)
        if i == len(words)-1:
            try:
                math_result = eval_math(math_expression)
                print('  DEBUG MATH: ' + math_expression + ' -> ' + str(math_result) + ' \t replace_expression = ' + replace_expression)
                # if the math works, then replace the section of the sentence
                replace_expression = replace_expression.strip() # to make sure replaces properly
                sentence = sentence.replace(replace_expression, str(math_result))
            except:
                pass
            # reset variables
            math_expression = ''
            replace_expression = ''
    return sentence

def eval_math(expression):
    return eval(expression,{"__builtins__":None},{}) # use ,{"__builtins__":None},{} to make eval function safer

"""
example:
Please assign one to variable apple
Please assign three hundred to variable banana
Please assign some words to variable coconut
"""
def check_assign(sentence):
    checkphrase = '.*' + 'assign ' + '(.+)' + ' to variable ' + '(.+)'
    matches = re.match(checkphrase, sentence)
    if matches:
        variable_value = matches.group(1)
        variable_name = matches.group(2)
        try:
            variable_value = eval_math(check_math(variable_value))
        except:
            pass
        variable_dictionary[variable_name] = variable_value
        # print(' variable_value = ' + str(variable_value) + ' \t variable_name = ' + variable_name)
        print('  DEBUG variable_dictionary: ' + str(variable_dictionary))

"""
example:
Please import alternate
Please import test from library
Please import numpy as nectarine pony
"""
def check_import(sentence):
    global import_dictionary
    module = None
    checkphrase = '.*import (.+)(( as (.+))|( from (.+)))'
    matches = re.match(checkphrase, sentence)
    if matches:
        import_name = matches.group(1)
        import_as = matches.group(4)
        import_from = matches.group(6)
        print('  DEBUG IMPORT:\n\timport_name = ' + str(import_name) + '\n\timport_from = ' + str(import_from) + '\n\timport_as = ' + str(import_as))
        if import_as: # can nickname import module
            print('  DEBUG IMPORT ... AS ...')
            module = import_module(import_name)
        if import_from: # can import from folder
            print('  DEBUG IMPORT ... FROM ...')
            spec = importlib.util.spec_from_file_location(import_name, import_from + '/' + import_name + '.py')
            module = importlib.util.module_from_spec(spec)
            # enables use of functions and variables from the module (does the actual import):
            spec.loader.exec_module(module)
        print(str(module))
        # add to list of imports
        if import_as:
            import_dictionary[import_as] = module
        else:
            import_dictionary[import_name] = module
        print('  DEBUG IMPORT: IMPORT_DICTIONARY, size = ' + str(len(import_dictionary)) + '\n\t = ' + str(import_dictionary))
    else:
        checkphrase = '.*import (.+)'
        matches = re.match(checkphrase, sentence)
        if matches:
            print('  DEBUG IMPORT NAME ...')
            import_name = matches.group(1).strip() # remove final spaces because of regex
            try: # try with .py ending
                spec = importlib.util.spec_from_file_location(import_name, import_name + '.py')
                module = importlib.util.module_from_spec(spec)
                # enables use of functions and variables from the module (does the actual import):
                spec.loader.exec_module(module)
            except:
                try: # try withOUT .py ending
                    spec = importlib.util.spec_from_file_location(import_name, import_name)
                    module = importlib.util.module_from_spec(spec)
                    # enables use of functions and variables from the module (does the actual import):
                    spec.loader.exec_module(module)
                except:
                    pass
            print(str(module))
            # add to list of imports
            import_dictionary[import_name] = module
            print('  DEBUG IMPORT: IMPORT_DICTIONARY, size = ' + str(len(import_dictionary)) + '\n\t = ' + str(import_dictionary))

"""
example:
Please use test_function of test
Please use test_function from test
"""
def check_use(sentence):
    global import_dictionary
    checkphrase = '.*use (.+)( from | of )(.+)'
    matches = re.match(checkphrase, sentence)
    if matches:
        use_string = matches.group(1)
        from_string = matches.group(3)
        print('  DEBUG USE: ' + use_string + ' from ' + from_string)
        function_imported = getattr(import_dictionary[from_string], use_string)
        try:
            function_imported() # try to use function_imported as a function
        except:
            print(function_imported) # in case function_imported is just an output value

"""
example:
please if one equals one then
please print it works
please end if
please if one equals two then
please print it should not print this
please end if
"""
def check_if(sentence): # TO-DO: track number of if-statements and end-ifs (nesting)
    global keep_going
    # force 'if' to be first word; DO NOT start regex with '.*'
    checkphrase = 'if (.+) then'
    matches = re.match(checkphrase, sentence)
    if matches and keep_going:
        math_expression = check_math(matches.group(1))
        if_string = eval_math(math_expression) # if_string = eval_math(check_math(check_variable(check_spell(matches.group(1)))))
        print('  DEBUG if (' + str(if_string) + ') then')
        if if_string == True:
            keep_going = True
            return True
        else:
            print('  DEBUG -> FALSE -> end if')
            return False
    else:
        checkphrase = '.*end if'
        matches = re.match(checkphrase, sentence)
        if matches:
            keep_going = True
            return True
        else:
            return keep_going



# initialize global variables:

hide_debug_printouts = False # True = hide debug prints print()
keep_going = True # whether to not ignore lines after an if-statement
variable_dictionary = {} # Python dictionaries are just hashtables (avg time complexity O(1))
import_dictionary = {}
math_words_numbers = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,
                      'ten':10,'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,
                      'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19,
                      'twenty':20,'thirty':30,'forty':40,'fifty':50,'sixty':60,'seventy':70,'eighty':80,'ninety':90,
                      'hundred':'00','thousand':'000','million':'000000','billion':'000000000','trillion':'000000000',
                      '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
math_words_operators = {'plus':'+','minus':'-','times':'*','divide':'/','divided':'/','equals':'==','equal':'==','modulus':'%','modulo':'%'}
spell_checkphrases = ['spell with first letters of',
                      'spell with first letter of',
                      'spell with the first letters of',
                      'spell with the first letter of',
                      'spelled with the first letters of',
                      'spelled with the first letter of',
                      'spell using the first letters of',
                      'spell using the first letter of',
                      'spelled using the first letters of',
                      'spelled using the first letter of',
                      'spelt with the first letters of',
                      'spelt with the first letter of',
                      'spelt using the first letters of',
                      'spelt using the first letter of',
                     ]
spell_finish_words = ['to', 'as', 'from', 'then', '$'] # $ for end of line for regex



# (this if statement lets code after it only run if you're running this file directly)
if __name__ == '__main__':
    print('\nPLEASE WORK...\n')
    # run this interpreter:
    interpret()
    print('\n...THANK YOU!\n')
    