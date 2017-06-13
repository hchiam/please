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
        sentence = sentence.strip() # remove '\n' and leading/trailing spaces
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
    
    [sentence, is_list] = check_list(sentence) # this can rely on math replacing integers
    if is_list:
        recognized = True
    
    [sentence, is_dictionary] = check_dictionary(sentence)
    if is_dictionary:
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
    
    [sentence, is_class] = check_class(sentence)
    if is_class:
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
            checkphrase = phrase_start + ' (.+)' + phrase_stop
            matches = re.search(checkphrase, sentence)
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
    matches_print = re.match('print (.+)', sentence)
    if matches_print:
        string = matches_print.group(1)
        string = replace_index_of_variable_in_print(string) # do this before replace variable to check more restrictive match first
        string = '"' + replace_variables_in_print(string) + '"' # enables replacing string '...variable <...> ...' with '...' + str(<..>) + '...'
        string = remove_empty_start_end(string)
        sentence = '\t'*num_indents + 'print(' + string + ')'
        return [sentence, True]
    elif sentence == 'print':
        sentence = 'print()'
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
            index_value = str(math_words_numbers[index_string]) # start index at zero (so don't add +1 here)
        elif is_digit(index_string):
            index_value = str(int(index_string)) # start index at zero (so don't add +1 here)
        elif index_string.startswith('variable '):
            index_value = index_value.replace('variable ', '')
        variable_name = index_found[1]
        update_variable_names_list(variable_name)
        variable_name_replacer = index_found[1].replace(' ','_') # variable names can't have spaces
        replace_over = 'index ' + index_string + ' of ' + variable_name
        replace_with = ' ' + '" + ' + variable_name_replacer + '[' + index_value + ']' + ' + "'
        string = string.replace(replace_over, replace_with)
    return string

def replace_variables_in_print(string):
    # add spaces to make it easier to cover all cases (only, start, mid, end) in single search regexes
    string = ' ' + string + ' '
    if 'variable ' in string:
        for variable_name in variable_names:
            variable_name_spaced = variable_name.replace('_',' ')
            if variable_name_spaced in string:
                replace_over = ' variable ' + variable_name_spaced
                replace_with = ' ' + '" + str(' + variable_name + ') + "'
                # note: add an initial space to replace_with so that words between variables get spaces between them
                string = string.replace(replace_over, replace_with)
        variables_found = re.findall('variable (.+?) ', string) # .findall() = get ALL non-overlapping matches
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
    has_variable = 'variable ' in sentence
    if not has_variable:
        return [sentence, False]
    else:
        # order matters; start with most restrictive first
        
        matches_variable_index = re.search(' index (.+) of variable (.+)', sentence)
        if matches_variable_index:
            variable_name = matches_variable_index.group(2).replace(' ','_') # variable names can't have spaces
            update_variable_names_list(variable_name)
            variable_index = matches_variable_index.group(1)
            replace_over = ' index ' + variable_index + ' of variable ' + variable_name
            replace_with = variable_name + '[' + variable_index + ']'
            sentence = sentence.replace(replace_over, replace_with)
            return [sentence, True]
        
        matches_variable_only = re.match('create variable (.+)', sentence)
        if matches_variable_only:
            variable_name = matches_variable_only.group(1).replace(' ','_') # variable names can't have spaces
            update_variable_names_list(variable_name)
            sentence = '\t'*num_indents + variable_name + ' = None'
            return [sentence, True]
        
        matches_variable_only = re.match('variable (.+)', sentence)
        if matches_variable_only:
            variable_name = matches_variable_only.group(1).replace(' ','_') # variable names can't have spaces (use underscores to avoid name collisions)
            update_variable_names_list(variable_name)
            sentence = '\t'*num_indents + variable_name + ' = None'
            return [sentence, True]
        
        matches_variable_only = re.search('variable (.+)', sentence)
        if matches_variable_only:
            variable_name = matches_variable_only.group(1).replace(' ','_') # variable names can't have spaces
            update_variable_names_list(variable_name)
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
    # need to find math expressions word-by-word (since typically embedded in sentences like assign...to...)
    for i, word in enumerate(words):
        if word in math_words_numbers:
            sentence = sentence.replace(word, str(math_words_numbers[word]))
            recognized = True
        elif word in math_words_boolean:
            sentence = sentence.replace(word, str(math_words_boolean[word]))
            recognized = True
        elif word in math_words_operators:
            replace_over = word
            if word == 'negative': # "- 1" --> "-1" for check_list(sentence) to work
                replace_over = 'negative '
            sentence = sentence.replace(replace_over, math_words_operators[word])
            # no str() because already string, just need to add to expression
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
please assign dragon fruit the value of list starting from eight ending at twelve
please assign variable crazy list the value list of one and two and tree bark
"""
def check_list(sentence):
    # check if ordered list of items from int to int
    matches_list_ordered = re.search(' list starting from (.+) ending at (.+)', sentence)
    if matches_list_ordered:
        list_start = matches_list_ordered.group(1)
        list_stop = matches_list_ordered.group(2)
        ordered_list_items = list(range(int(list_start), int(list_stop) + 1)) # + 1 so that the number spoken actually appears in the list
        ordered_list_items = create_list_string(ordered_list_items)
        replace_over = matches_list_ordered.group()
        replace_with = ' ' + ordered_list_items
        sentence = sentence.replace(replace_over, replace_with)
        return [sentence, True]
    
    # check if unordered list of items separated by ' and '
    matches_list_unordered = re.search(' list of (.+)', sentence)
    if matches_list_unordered:
        string_of_list_items = matches_list_unordered.group(1)
        unordered_list_items = string_of_list_items.split(' and ') # items separated by ' and '
        unordered_list_items = create_list_string(unordered_list_items)
        replace_over = matches_list_unordered.group()
        replace_with = ' ' + unordered_list_items
        sentence = sentence.replace(replace_over, replace_with)
        return [sentence, True]
    
    # just in case
    return [sentence, False]

"""
example:
please assign my dictionary the value dictionary key one value apple
please assign my dictionary the value dictionary key one value apple key two value banana
"""
def check_dictionary(sentence):
    
    matches_dictionary = re.search(' (dictionary( key .+ value .+)+)', sentence)
    if matches_dictionary:
        pairs = matches_dictionary.group(2).split(' key ') # returns ['', '<keyval> value <value>', ...]
        pairs = list(filter(None,pairs)) # filter(None,...) is shorthand for filter(lambda x:x, ...)
        replace_with = []
        for pair in pairs:
            key = pair.split(' value ')[0]
            val = pair.split(' value ')[1]
            replace_with.append('\'' + key + '\'' + ':' + '\'' + val + '\'')
        replace_with = '{ ' + ', '.join(replace_with) + ' }'
        replace_over = matches_dictionary.group(1)
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
please assign other the value it works
please use function test on variable other
"""
def check_use(sentence): # TODO: make into one regex
    
    # order matters; start with most restrictive first
    
    matches_from_and_input = re.match('assign (.+) (use|using) (.+) (from|of) (.+) (on|with) (.+)', sentence)
    if matches_from_and_input:
        function_output = matches_from_and_input.group(1).replace('variable ', '')
        function_name = matches_from_and_input.group(3).replace('function ', '').replace(' ','_')
        function_from = matches_from_and_input.group(5).replace(' ','_')
        function_input = matches_from_and_input.group(7).replace('variable ', '')
        replace_over = matches_from_and_input.group()
        # check assignment
        function_output = re.match('(to )?(.+) the value (of )?', function_output)
        if function_output:
            function_output = function_output.group(2).replace(' ','_') + ' = '
        replace_with = '\t'*num_indents + function_output + function_from + '.' + function_name + '(' + function_input + ')'
        sentence = sentence.replace(replace_over, replace_with)
        recognized = True
        return [sentence, recognized]
    
    matches_from_and_input = re.match('assign (.+) (use|using) (.+) (from|of) (.+)', sentence)
    if matches_from_and_input:
        function_output = matches_from_and_input.group(1).replace('variable ', '')
        function_name = matches_from_and_input.group(3).replace('function ', '').replace(' ','_')
        function_from = matches_from_and_input.group(5).replace(' ','_')
        replace_over = matches_from_and_input.group()
        # check assignment
        function_output = re.match('(to )?(.+) the value (of )?', function_output)
        if function_output:
            function_output = function_output.group(2).replace(' ','_') + ' = '
        replace_with = '\t'*num_indents + function_output + function_from + '.' + function_name + '()'
        sentence = sentence.replace(replace_over, replace_with)
        recognized = True
        return [sentence, recognized]
    
    matches_from_and_input = re.match('assign (.+) (use|using) (.+) (on|with) (.+)', sentence)
    if matches_from_and_input:
        function_output = matches_from_and_input.group(1).replace('variable ', '')
        function_name = matches_from_and_input.group(3).replace('function ', '').replace(' ','_')
        function_input = matches_from_and_input.group(5).replace('variable ', '')
        replace_over = matches_from_and_input.group()
        # check assignment
        function_output = re.match('(to )?(.+) the value (of )?', function_output)
        if function_output:
            function_output = function_output.group(2).replace(' ','_') + ' = '
        replace_with = '\t'*num_indents + function_output + function_name + '(' + function_input + ')'
        sentence = sentence.replace(replace_over, replace_with)
        recognized = True
        return [sentence, recognized]
    
    matches_from_and_input = re.search('(use|using) (.+) (from|of) (.+) (on|with) (.+)', sentence)
    if matches_from_and_input:
        function_name = matches_from_and_input.group(2).replace('function ', '').replace(' ','_')
        function_from = matches_from_and_input.group(4).replace(' ','_')
        function_input = matches_from_and_input.group(6).replace('variable ', '')
        replace_over = matches_from_and_input.group()
        replace_with = '\t'*num_indents + function_from + '.' + function_name + '(' + function_input + ')'
        sentence = sentence.replace(replace_over, replace_with)
        recognized = True
        return [sentence, recognized]
    
    matches_from = re.search('(use|using) (.+) (from|of) (.+)', sentence)
    if matches_from:
        function_name = matches_from.group(2).replace('function ', '').replace(' ','_')
        function_from = matches_from.group(4).replace(' ','_')
        replace_over = matches_from.group()
        replace_with = '\t'*num_indents + function_from + '.' + function_name + '()'
        sentence = sentence.replace(replace_over, replace_with)
        recognized = True
        return [sentence, recognized]
    
    matches_input = re.search('(use|using) (.+) (on|with) (.+)', sentence)
    if matches_input:
        function_name = matches_input.group(2).replace('function ', '').replace(' ','_')
        function_input = matches_input.group(4).replace('variable ', '')
        replace_over = matches_input.group()
        replace_with = '\t'*num_indents + function_name + '(' + function_input + ')'
        sentence = sentence.replace(replace_over, replace_with)
        recognized = True
        return [sentence, True]
    
    matches_name = re.search('(use|using) (.+)', sentence)
    if matches_name:
        function_name = matches_name.group(2).replace('function ', '').replace(' ','_')
        replace_over = matches_name.group()
        replace_with = '\t'*num_indents + function_name + '()'
        sentence = sentence.replace(replace_over, replace_with)
        recognized = True
        return [sentence, recognized]
    
    # just in case
    return [sentence, False]

"""
example:
please assign to variable apple the value of one
please assign to banana the value three hundred
please assign coconut the value of some words
please assign dragon fruit the value four

NOTE DEPRECATED/OBSOLTE:
please assign one to apple
"""
def check_assign(sentence):
    matches_assign2 = re.match('assign (to )?(variable )?(.+) (the )+?value (of )?(.+)', sentence)
    if matches_assign2:
        variable_name = matches_assign2.group(3).replace(' ','_') # variable names can't have spaces
        update_variable_names_list(variable_name)
        variable_value = matches_assign2.group(6)
        first_word_is_string = check_if_just_string(variable_value)
        
        # if the first word is not math, then just make the whole variable value a string (otherwise leave as is)
        if first_word_is_string and not variable_value.startswith('variable ') and not variable_value.startswith('list '):
            variable_value = '\'' + variable_value + '\'' # need to put quotation marks around strings being assigned
        elif variable_value.startswith('variable '):
            variable_value = variable_value.replace('variable ', '')
        elif is_digit(variable_value.replace(' ','')): # TODO need better way to detect that it's not a string
            variable_value = variable_value.replace(' ','') # so "3 00" becomes "300"
        sentence = '\t'*num_indents + variable_name + ' = ' + variable_value
        return [sentence, True]
    
    # just in case
    return [sentence, False]

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

def update_variable_names_list(variable_name):
    if variable_name not in variable_names:
        variable_names.append(variable_name)

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
    
    if sentence.startswith('end if') or sentence.startswith('done if'):
        num_indents -= 1
        sentence = '\t'*num_indents
        return [sentence, True]
    
    # escape early if does not start with 'if '
    if not sentence.startswith('if '):
        return [sentence, False]
    
    # note: force 'if ' to be first word; DO NOT start regex with '.*'
    matches_multiliner = re.match('if (.+) then ?$', sentence) # $ for end of sentence
    matches_oneliner = re.match('if (.+) then (.+)', sentence) # space after 'then' WITHOUT $ because sentence continues
    
    if matches_multiliner:
        condition = matches_multiliner.group(1).replace('variable ', '')
        sentence = '\t'*num_indents + 'if ' + condition + ':'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    if matches_oneliner:
        condition = matches_oneliner.group(1).replace('variable ', '')
        then = check_print(matches_oneliner.group(2))[0] # because check_print() only activates if 'print ' starts the string
        sentence = '\t'*num_indents + 'if ' + condition + ':' + '\n' + '\t'*(num_indents+1) + then + '\n' + '\t'*num_indents
        return [sentence, True]
    
    # just in case
    return [sentence, False]

"""
example:
please assign variable circle the value of list from negative one to three
please for each index in circle
    please print variable index
please end for
"""
def check_for(sentence):
    global num_indents
    
    matches_for = re.match('for (.+) in (.+)', sentence)
    if matches_for:
        for_what = matches_for.group(1).replace('each ', '')
        for_in = matches_for.group(2).replace(' ','_') # variable names can't have spaces
        sentence = '\t'*num_indents + 'for ' + for_what + ' in ' + for_in + ':'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    if sentence.startswith('end for') or sentence.startswith('done for'):
        num_indents -= 1
        sentence = '\t'*num_indents
        return [sentence, True]
    
    # just in case
    return [sentence, False]

def check_class(sentence):
    global num_indents
    
    matches_define_class = re.match('(define |create )(a )?class (named )?(.+)', sentence)
    if matches_define_class:
        class_name = matches_define_class.group(4).replace(' ','_') # class names can't have spaces
        sentence = '\t'*num_indents + 'class ' + class_name + ':'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    matches_end_class = re.match('end class', sentence)
    matches_end_class2 = re.match('done class', sentence)
    if matches_end_class or matches_end_class2:
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
please assign to other the value it works
please use function test on variable other
"""
def check_function(sentence):
    global num_indents
    
    matches_define_function_with_input = re.match('define function (.+) (with|using) (inputs |input )?(.+)$', sentence)
    if matches_define_function_with_input:
        function_name = matches_define_function_with_input.group(1).replace(' ','_') # function names can't have spaces
        input_names = ','.join(matches_define_function_with_input.group(4).split(' and '))
        sentence = '\t'*num_indents + 'def ' + function_name + '(' + input_names + '):'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    matches_define_function = re.match('define function (.+)$', sentence)
    if matches_define_function:
        function_name = matches_define_function.group(1).replace(' ','_') # function names can't have spaces
        sentence = '\t'*num_indents + 'def ' + function_name + '():'
        num_indents += 1 # affect indents for later lines, not current line
        return [sentence, True]
    
    matches_end_function = re.match('end function', sentence)
    matches_end_function2 = re.match('done function', sentence)
    if matches_end_function or matches_end_function2:
        num_indents -= 1
        sentence = '\t'*num_indents
        return [sentence, True]
    
    matches_return = re.match('return (.+)', sentence)
    if matches_return:
        output_value = matches_return.group(1) # will either output the literal value "...", or the value of "variable ..."
        if output_value.startswith('variable '):
            # print(variable_names) # TODO: some variables it has should not have been created
            output_value = replace_variables_in_return(output_value)
            # for variable_name in variable_names:
            #     if 'variable ' + variable_name.replace('_',' ') in output_value:
            #         output_value = output_value.replace('variable ' + variable_name.replace('_',' '), variable_name)
            # output_value = output_value.replace('variable ', '') #.replace(' ','_')
        output_value = check_math(output_value)[0] # will either output the literal value "...", or the value of "variable ..."
        sentence = '\t'*num_indents + 'return ' + str(output_value)
        return [sentence, True]
    
    # just in case
    return [sentence, False]

def replace_variables_in_return(string):
    # add spaces to make it easier to cover all cases (only, start, mid, end) in single search regexes
    string = ' ' + string + ' '
    if 'variable ' in string:
        for variable_name in variable_names:
            variable_name_spaced = variable_name.replace('_',' ')
            if variable_name_spaced in string:
                replace_over = ' variable ' + variable_name_spaced
                replace_with = variable_name
                # note: add an initial space to replace_with so that words between variables get spaces between them
                string = string.replace(replace_over, replace_with)
        variables_found = re.findall('variable ([\w ]+) ', string) # .findall() = get ALL non-overlapping matches
        for variable_found in variables_found:
            replace_over = 'variable ' + variable_found
            replace_with = variable_found.replace(' ', '_')
            # note: add an initial space to replace_with so that words between variables get spaces between them
            string = string.replace(replace_over, replace_with)
    return string.strip()

def print_debug(string):
    if hide_debug_printouts == False:
        print('  DEBUG ' + string)



# initialize global variables:

num_indents = 0
code_file_name = 'code.py'
# track variable names
variable_names = []
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