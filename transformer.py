# transform() function is where you should start reading to understand this code.
# transform() has to be called at the bottom of this file for things to work.

from sys import *
import re
from importlib import import_module
import importlib.util



# functions:

def transform():
    file_name = argv[1] # so you can use this Terminal command: python transformer.py text.txt
    text = get_text(file_name)
    text = text.lower() # lowercase
    text = remove_multi_spaces(text)
    sentences = get_sentences(text)
    clear_code_file(code_file_name)
    compile_code(sentences)
    run_code()

def get_text(file_name):
    text = open(file_name, 'r').read() # for example: file_name = "text.txt"
    return text

def remove_multi_spaces(text):
    # just doing ' '.join(text.split()) would not enable use of terse mode (which uses '\n')
    newtext = ''
    for line in text.split('\n'):
        line = ' '.join(line.split())
        newtext += line + '\n'
    return newtext.strip() # remove trailing line(s)

def get_sentences(text):
    # normally, each sentence is expected to begin with "please "
    split_by_word = 'please '
    # but you can turn on "terse mode" to use newline characters per line of code if your interface enables it
    terse_mode_on = check_terse_mode(text)
    if terse_mode_on:
        split_by_word = '\n'
    # split into sentences by "please " or by "\n"
    sentences = text.split(split_by_word)[1:] # assume index [0] is always empty or invalid before the first "please " or "\n"
    return sentences

def check_terse_mode(text):
    """
    example:
    please no need to say please
    print this works
    print no need to say please before each line
    """
    terse_mode_on = False
    checkphrases = ['please no need to say please',
                    'please use enter mode',
                    'please use short mode']
    if any(text.startswith(checkphrase) for checkphrase in checkphrases):
        terse_mode_on = True
    return terse_mode_on

def clear_code_file(filename):
    open(filename, 'w').close()

def compile_code(sentences):
    global nested_blocks_ignore
    i = 0
    for sentence in sentences: # use i to access sentence indices for go-to locations
        sentence = modify_sentence(sentence)
        with open(code_file_name, 'a') as f:
            f.write(sentence+'\n')

def modify_sentence(sentence):
    # note that order matters for replacing things in the sentence
    
    recognized = False
    
    if sentence == '': # blank/new line
        return sentence
    
    sentence = check_spell(sentence)
    
    [sentence, is_note] = check_note(sentence)
    if is_note:
        # don't bother checking the rest
        return sentence
    
    [sentence, is_print] = check_print(sentence)
    if is_print:
        # don't bother checking the rest
        return sentence
    
    [sentence, is_import] = check_import(sentence)
    if is_import:
        # don't bother checking the rest
        return sentence
    
    [sentence, is_variable] = check_variable(sentence)
    if is_variable:
        recognized = True
    
    [sentence, is_math] = check_math(sentence)
    if is_math:
        recognized = True
    
    [sentence, is_list] = check_list(sentence) # this relies on math replacing integers
    if is_list:
        recognized = True
    
    [sentence, is_use] = check_use(sentence)
    if is_use:
        recognized = True
    
    [sentence, is_assign] = check_assign(sentence)
    if is_assign:
        recognized = True
    
    [sentence, is_if] = check_if(sentence)
    if is_if:
        recognized = True
    
    [sentence, is_for] = check_for(sentence)
    if is_for:
        recognized = True
    
    [sentence, is_function] = check_function(sentence)
    if is_function:
        recognized = True
    
    # treat with suspicion if nothing was recognized in the sentence
    if not recognized:
        raise Exception('DID NOT RECOGNIZE COMMAND: ' + sentence)
    else:
        return sentence

def run_code():
    code_file_name_without_py_extension = code_file_name[:-3]
    importlib.import_module(code_file_name_without_py_extension)

"""
example:
please spell with the first letters of Neptune unicorn moose panda Yoda
"""
def check_spell(sentence):
    # find matches in sentence:
    for phrase_start in spell_checkphrases:
        for phrase_stop in spell_finish_words:
            checkphrase = '.*' + phrase_start + ' (.+)' + phrase_stop
            matches = re.match(checkphrase, sentence)
            if matches:
                words_to_spell_with = matches.group(1) # this is substring found inside '(.+)'
                spelt_word = spell_with_first_letters(checkphrase, words_to_spell_with)
                print_debug('SPELL: spelt_word=' + spelt_word)
                phrase_to_replace = phrase_start + ' ' + words_to_spell_with
                sentence = sentence.replace(phrase_to_replace, spelt_word + ' ').strip()
    return sentence

def spell_with_first_letters(checkphrase, sentence):
    local_sent = sentence.replace(checkphrase, '')
    words = local_sent.split()
    spelt_word = ''.join(list(word[0] for word in words))
    return spelt_word

"""
example:
please note this is a comment
"""
def check_note(sentence):
    word = 'note' + ' '
    word_len = len(word)
    if sentence.startswith(word):
        sentence = '\t'*num_indents + '# ' + sentence[word_len:]
        return [sentence, True]
    else:
        return [sentence, False]

"""
example:
please print this string of words
"""
def check_print(sentence):
    word = 'print' + ' '
    word_len = len(word)
    if sentence.startswith(word):
        string = sentence[word_len:]
        string = replace_index_of_variable_in_print(string) # do this before replace variable to check more restrictive match first
        string = '"' + replace_variables_in_print(string) + '"' # enables replacing string '...variable <...> ...' with '...' + str(<..>) + '...'
        string = remove_empty_start_end(string)
        sentence = '\t'*num_indents + 'print(' + string + ')'
        return [sentence, True]
    else:
        return [sentence, False]

def replace_index_of_variable_in_print(string):
    # add spaces to make it easier to cover all cases (only, start, mid, end) in single search regexes
    string = ' ' + string + ' '
    indexes_found = re.findall(' index (.+) of (.+) ', string)
    for index_found in indexes_found:
        index_string = index_found[0]
        index_value = str(index_string)
        if index_string in math_words_numbers:
            index_value = str(math_words_numbers[index_string] - 1) # start index at one
        elif is_digit(index_string):
            index_value = str(int(index_string) - 1) # start index at one
        elif index_string.startswith('variable '):
            index_value = index_value.replace('variable ', '')
        variable_name = index_found[1]
        variable_name_replacer = index_found[1].replace(' ','_') # variable names can't have spaces
        replace_over = 'index ' + index_string + ' of ' + variable_name
        replace_with = ' ' + '" + ' + variable_name_replacer + '[' + index_value + ']' + ' + "'
        string = string.replace(replace_over, replace_with)
    return string

def replace_variables_in_print(string): # TODO: enable replace multi-word variable names (would require tracking a list of variable names)
    # add spaces to make it easier to cover all cases (only, start, mid, end) in single search regexes
    string = ' ' + string + ' '
    if 'variable ' in string:
        variables_found = re.findall('variable (.+?) ', string) # get ALL non-overlapping matches
        for variable_found in variables_found:
            replace_over = ' variable ' + variable_found
            replace_with = ' ' + '" + str(' + variable_found + ') + "'
            # note: add an initial space to replace_with so that words between variables get spaces between them
            string = string.replace(replace_over, replace_with)
    return string.strip()

def remove_empty_start_end(string):
    false_start = '"" + '
    false_end = ' + ""'
    string = string.replace(false_start, '').replace(false_end, '')
    return string

"""
example:
please import alternate
please import test from library
please import numpy as nectarine pony
"""
def check_import(sentence):
    # order matters; start with most restrictive first
    
    if not sentence.startswith('import '):
        return [sentence, False]
    
    matches_as_from = re.match('import (.+) as (.+) from (.+)', sentence)
    if matches_as_from:
        import_name = matches_as_from.group(1)
        import_as   = matches_as_from.group(2).replace(' ','_') # import names can't have spaces
        import_from = matches_as_from.group(3)
        sentence = '\t'*num_indents + 'from ' + import_from + ' import ' + import_name + ' as ' + import_as
        return [sentence, True]
    
    matches_as = re.match('import (.+) as (.+)', sentence)
    if matches_as:
        import_name = matches_as.group(1)
        import_as   = matches_as.group(2).replace(' ','_') # import names can't have spaces
        sentence = '\t'*num_indents + 'import ' + import_name + ' as ' + import_as
        return [sentence, True]
    
    matches_from = re.match('import (.+) from (.+)', sentence)
    if matches_from:
        import_name = matches_from.group(1)
        import_from = matches_from.group(2)
        sentence = '\t'*num_indents + 'from ' + import_from + ' import ' + import_name
        return [sentence, True]
    
    matches_name = re.match('import (.+)', sentence)
    if matches_name:
        import_name = matches_name.group(1)
        sentence = '\t'*num_indents + 'import ' + import_name
        return [sentence, True]
    
    # just in case
    return [sentence, False]

"""
example:
please create variable apple
please variable banana
please print you assigned variable apple to apple
"""
def check_variable(sentence):
    has_variable = re.match('.*variable (.+).*', sentence)
    if not has_variable:
        return [sentence, False]
    else:
        # order matters; start with most restrictive first
        
        matches_variable_index = re.match('.* index (.+) of variable (.+).*', sentence)
        if matches_variable_index:
            variable_name = matches_variable_index.group(2).replace(' ','_') # variable names can't have spaces
            variable_index = matches_variable_index.group(1)
            replace_over = ' index ' + variable_index + ' of variable ' + variable_name
            replace_with = variable_name + '[' + variable_index + ']'
            sentence = sentence.replace(replace_over, replace_with)
            return [sentence, True]
        
        matches_variable_only = re.match('create variable (.+)', sentence)
        if matches_variable_only:
            variable_name = matches_variable_only.group(1).replace(' ','_') # variable names can't have spaces
            sentence = '\t'*num_indents + variable_name + ' = None'
            return [sentence, True]
        
        matches_variable_only = re.match('variable (.+)', sentence)
        if matches_variable_only:
            variable_name = matches_variable_only.group(1).replace(' ','_') # variable names can't have spaces (use underscores to avoid name collisions)
            sentence = '\t'*num_indents + variable_name + ' = None'
            return [sentence, True]
        
        matches_variable_only = re.match('.* variable (.+).*', sentence)
        if matches_variable_only:
            variable_name = matches_variable_only.group(1).replace(' ','_') # variable names can't have spaces
            replace_over = ' variable ' + variable_name
            replace_with = ' ' + variable_name
            sentence = sentence.replace(replace_over, replace_with)
            return [sentence, True]
        
        # just in case
        return [sentence, False]

"""
example:
please one plus two
"""
def check_math(sentence):
    recognized = False
    words = sentence.split()
    math_expression = ''
    replace_expression = ''
    escape_signals = ['print','variable','assign','if','then','to','of','from','import','for','as','end','each','in','list','use','function','return']
    # need to find math expressions word-by-word (since typically embedded in sentences like assign...to...)
    for i, word in enumerate(words):
        if word in math_words_numbers:
            math_expression += str(math_words_numbers[word])
            replace_expression += ' ' + word
            recognized = True
        elif is_digit(word):
            math_expression += str(word)
            replace_expression += ' ' + word
            recognized = True
        elif word in math_words_boolean:
            math_expression += str(math_words_boolean[word])
            replace_expression += ' ' + word
            recognized = True
        elif word in math_words_operators:
            math_expression += math_words_operators[word] # no str() because already string, just need to add to expression
            replace_expression += ' ' + word
            recognized = True
        elif word in escape_signals:
            replace_expression = replace_expression.strip() # use strip() to make sure replaces properly
            sentence = sentence.replace(replace_expression, math_expression)
            math_expression = '' # reset for next sequence
            replace_expression = '' # reset for next sequence
            recognized = True
        # also account for end of sentence as escape signal
        if i == len(words)-1:
            replace_expression = replace_expression # do NOT use strip() so final math word just gets appended to variable name
            sentence = sentence.replace(replace_expression, math_expression)
            math_expression = '' # reset for next sequence
            replace_expression = '' # reset for next sequence
            recognized = True
    return [sentence, recognized]

def is_digit(string):
    # built-in isdigit() doesn't work with negative numbers
    try:
        int(string)
        return True
    except:
        return False

"""
example:
please assign list from eight to twelve to durian
please assign list of one and two and tree bark to variable crazy list
"""
def check_list(sentence):
    # check if ordered list of items from int to int
    matches_list_ordered = re.match('.* list from (.+) to (.+)( to )+?.*', sentence) # ( to )+? to account for assignment wrapping it
    if matches_list_ordered:
        list_start = matches_list_ordered.group(1)
        list_stop = matches_list_ordered.group(2)
        ordered_list_items = list(range(int(list_start), int(list_stop) + 1)) # + 1 so that the number spoken actually appears in the list
        ordered_list_items = create_list_string(ordered_list_items)
        replace_over = ' list from ' + list_start + ' to ' + list_stop
        replace_with = ' ' + ordered_list_items
        sentence = sentence.replace(replace_over, replace_with)
        return [sentence, True]
    
    # check if unordered list of items separated by ' and '
    matches_list_unordered = re.match('.* list of (.+)( to )+?.*', sentence) # ( to )+? to account for assignment wrapping it
    if matches_list_unordered:
        string_of_list_items = matches_list_unordered.group(1)
        unordered_list_items = string_of_list_items.split(' and ') # items separated by ' and '
        unordered_list_items = create_list_string(unordered_list_items)
        replace_over = ' list of ' + string_of_list_items
        replace_with = ' ' + unordered_list_items
        sentence = sentence.replace(replace_over, replace_with)
        return [sentence, True]
    
    # just in case
    return [sentence, False]

def create_list_string(list_items):
    # note: spaces between '[ ', ' ]', and ' , ' because need to identify list items as numbers/strings
    list_string = '[ '
    for item in list_items:
        if is_digit(item):
            list_string += str(item)
        elif item in math_words_numbers:
            list_string += str(math_words_numbers[item])
        elif item in math_words_boolean:
            list_string += str(math_words_boolean[item])
        elif ' ' in str(item) and all((is_digit(word) or word in math_words_numbers or word in math_words_operators or word in math_words_boolean) for word in item.split()):
            # need this condition to account for things like negative numbers in (un)ordered lists
            
            # if composed of multiple words that are all math words
            for word in item.split():
                if is_digit(word):
                    list_string += str(word)
                elif word in math_words_numbers:
                    list_string += str(math_words_numbers[word])
                elif word in math_words_boolean:
                    list_string += str(math_words_boolean[word])
                elif word in math_words_operators: # use this because could contain minus/plus/etc.
                    list_string += str(math_words_operators[word])
        else:
            list_string += '\'' + str(item) + '\''
        list_string += ' , '
    list_string = list_string[:-3] # remove last comma and space
    list_string += ' ]'
    return list_string

"""
example 1:
please use test_function of test
please use test_function from test
"""
"""
example 2:
please define function test with item
    please print variable item
please end function
please assign it works to other
please use function test on variable other
"""
def check_use(sentence):
    if not sentence.startswith('use '):
        return [sentence, False]
    
    # order matters; start with most restrictive first
    
    matches_from_and_input = re.match('.*use (function )?(.+)( (from|of) (.+))+?( (on|with) (.+))+?', sentence)
    if matches_from_and_input:
        function_name = matches_from_and_input.group(2).replace(' ','_')
        function_from = matches_from_and_input.group(5).replace(' ','_')
        function_input = matches_from_and_input.group(8).replace(' ','_')
        sentence = '\t'*num_indents + function_from + '.' + function_name + '(' + function_input + ')'
        recognized = True
        return [sentence, recognized]
    
    matches_from = re.match('.*use (function )?(.+) (from|of) (.+)', sentence)
    if matches_from:
        function_name = matches_from.group(2).replace(' ','_')
        function_from = matches_from.group(4).replace(' ','_')
        sentence = '\t'*num_indents + function_from + '.' + function_name + '()'
        recognized = True
        return [sentence, recognized]
    
    matches_input = re.match('.*use (function )?(.+) (on|with) (.+)', sentence)
    if matches_input:
        function_name = matches_input.group(2).replace(' ','_')
        function_input = matches_input.group(4)
        sentence = '\t'*num_indents + function_name + '(' + function_input + ')'
        recognized = True
        return [sentence, True]
    
    matches_name = re.match('.*use (function )?(.+)', sentence)
    if matches_name:
        function_name = matches_name.group(2).replace(' ','_')
        sentence = '\t'*num_indents + function_name + '()'
        recognized = True
        return [sentence, recognized]
    
    # just in case
    return [sentence, False]

"""
example:
please assign one to variable apple
please assign three hundred to variable banana
please assign some words to variable coconut
"""
def check_assign(sentence):
    matches_assign = re.match('.*assign (.+) to (variable )?(.+)', sentence)
    if not matches_assign:
        return [sentence, False]
    else:
        variable_name = matches_assign.group(3).replace(' ','_') # variable names can't have spaces
        variable_value = matches_assign.group(1)
        first_word_is_string = check_if_just_string(variable_value)
        # if the first word is not math, then just make the whole variable value a string (otherwise leave as is)
        if first_word_is_string:
            variable_value = '\'' + variable_value + '\'' # need to put quotation marks around strings being assigned
        sentence = '\t'*num_indents + variable_name + ' = ' + variable_value
        return [sentence, True]

def check_if_just_string(variable_value):
    # get first word
    first_word = variable_value.split(' ',1)[0]
    # do various checks
    not_variable = first_word != 'variable'
    not_number = first_word not in math_words_numbers
    not_boolean = first_word not in math_words_boolean
    not_math_punctuation = first_word not in math_punctuation
    first_few_characters_are_math = is_digit(first_word[0]) or is_digit(first_word[:2])
    # put those checks together
    first_word_is_string = not_variable and not_number and not_boolean and not first_few_characters_are_math and not_math_punctuation
    return first_word_is_string

"""
example:
please if true then print this is a one line if statement
please if one equals one then
    please print it works
please end if
please if one equals two then
    please print it should not print this
please end if
"""
def check_if(sentence):
    global num_indents
    
    if sentence == 'end if':
        num_indents -= 1
        sentence = '\t'*num_indents
        return [sentence, True]
    
    # escape early if does not start with 'if '
    if not sentence.startswith('if '):
        return [sentence, False]
    
    # note: force 'if ' to be first word; DO NOT start regex with '.*'
    matches_multiliner = re.match('if (.+) then$', sentence) # $ for end of sentence
    matches_oneliner = re.match('if (.+) then (.+)', sentence) # space after 'then' WITHOUT $ because sentence continues
    
    if matches_multiliner:
        condition = matches_multiliner.group(1)
        sentence = '\t'*num_indents + 'if ' + condition + ':'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    if matches_oneliner:
        condition = matches_oneliner.group(1)
        then = modify_sentence(matches_oneliner.group(2))
        sentence = '\t'*num_indents + 'if ' + condition + ':' + '\n' + '\t'*(num_indents+1) + then + '\n' + '\t'*num_indents
        return [sentence, True]
    
    # just in case
    return [sentence, False]

"""
example:
please assign list from negative one to three to variable circle
please for each index in circle
    please print variable index
please end for
"""
def check_for(sentence):
    global num_indents
    
    matches_for = re.match('for each (.+) in (.+)', sentence)
    if matches_for:
        for_what = matches_for.group(1)
        for_in = matches_for.group(2).replace(' ','_') # variable names can't have spaces
        sentence = '\t'*num_indents + 'for ' + for_what + ' in ' + for_in + ':'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    if sentence == 'end for':
        num_indents -= 1
        sentence = '\t'*num_indents
        return [sentence, True]
    
    # just in case
    return [sentence, False]

"""
example:
please define function test with item
    please print variable item
please end function
please assign it works to other
please use function test on variable other
"""
def check_function(sentence):
    global num_indents
    
    matches_define_function_with_input = re.match('define function (.+) (with|using) (inputs |input )?(.+)$', sentence)
    if matches_define_function_with_input:
        function_name = matches_define_function_with_input.group(1)
        input_names = ','.join(matches_define_function_with_input.group(4).split(' and '))
        sentence = '\t'*num_indents + 'def ' + function_name + '(' + input_names + '):'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    matches_define_function = re.match('define function (.+)$', sentence)
    if matches_define_function:
        function_name = matches_define_function.group(1)
        sentence = '\t'*num_indents + 'def ' + function_name + '():'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    if sentence == 'end function':
        num_indents -= 1
        sentence = '\t'*num_indents
        return [sentence, True]
    
    matches_return = re.match('return (variable )?(.+)', sentence)
    if matches_return:
        output_value = check_math(matches_return.group(2)) # will either output the literal value "...", or the value of "variable ..."
        sentence = '\t'*num_indents + 'return ' + output_value
        num_indents -= 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    # just in case
    return [sentence, False]

def print_debug(string):
    if hide_debug_printouts == False:
        print('  DEBUG ' + string)



# initialize global variables:

num_indents = 0
code_file_name = 'code.py'
# recognize words for numbers, math operations, spelling checkphases, etc.
math_words_numbers = {'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,
                      'six':6,'seven':7,'eight':8,'nine':9,'ten':10,
                      'eleven':11,'twelve':12,'thirteen':13,'fourteen':14,'fifteen':15,
                      'sixteen':16,'seventeen':17,'eighteen':18,'nineteen':19,
                      'twenty':20,'thirty':30,'forty':40,'fifty':50,
                      'sixty':60,'seventy':70,'eighty':80,'ninety':90,
                      'hundred':'00','thousand':'000','million':'000000',
                      'billion':'000000000','trillion':'000000000',
                      '0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
math_words_boolean = {'true':True,'false':False}
math_words_operators = {'plus':'+','positive':'+','minus':'-','negative':'-',
                        'times':'*','divide':'/','divided':'/',
                        'equals':'==','equal':'==','over':'>','above':'>','under':'<','below':'<',
                        'not':'!',
                        'modulus':'%','modulo':'%'} # add more functions later as needed
math_punctuation = '()[]{},.:-+=/*><!%'
spell_checkphrases = ['spell with first letters of',
                      'spell with first letter of',
                      'spelled with first letters of',
                      'spelled with first letter of',
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

# True = hide debug prints:
# False = show debug prints:
hide_debug_printouts = True



# (this if statement lets code after it only run if you're running this file directly)
if __name__ == '__main__':
    print('\nPLEASE WORK...\n')
    # run this interpreter:
    transform()
    print('\n...THANK YOU!\n')