<img src="https://github.com/hchiam/please/blob/master/library/please_icon.jpeg" height="250" title="Please scroll down to read more">

# "Please" - An Experimental Programming Language

**Simply put:** Program by talking to your computer using common English words. 

**More technically:** You can easily write code in Please using speech recognition software (like Mac Dictation) out-of-the-box, without having to train the software to recognize esoteric jargon and special keywords for symbols. As of release v0.2.0: transformer.py compiles Please into Python code and runs that. 

<br>

# Example Code in Please:

First transcribe this code:

```
please print this string of words
```

When you run that code, it prints out:

```
this string of words
```

<br>

# Try It:

## A) In Your Browser (Mini Version):

No speech recognition software? No Python? Just type code in your browser: https://trinket.io/python3/5cdaee1b04 (go to the text.txt tab to write code in Please).

## B) On Your Computer (Full Version):

1. Download this project from GitHub. https://github.com/hchiam/please/archive/master.zip --> master branch. Or get a different version at https://github.com/hchiam/please/releases

2. Open the folder using Terminal or Command-line.

3. Then input the following command and hit enter:

```
python transformer.py text.txt
```

The *transformer* will take the *text* file "source code" written in Please, translate it into Python code, and then run that Python code.

Requires Python 3: https://www.python.org/downloads

This project was built with Python 3.6.0

<br>

# Why?

What if you could easily write code just by talking with speech recognition software? What if code could be *more* like English sentences? How might you combine these two things (easy-to-parse and easy-to-say code)?

Please is an attempt at that.

Here are 3 ground rules to make commands easier to say, but also easier for speech recognition software and Please's code transformer to understand:

1. **Just say words that use your ABCs and spaces between**. No special non-letter characters like "?". Why? Speed and recognition. Saying "question mark" just to type out "?" is slow and could be faulty if the speech recognition software thinks you literally want the words "question mark". Please also doesn't differentiate (non-)capital letters because it's a speech-based language (vs. a "written language").
2. **Avoid specialized words or names**. Why? So you don't have to specifically train your speech recognition software to recognize uncommon words like "numpy" (mine thought I said "numb pie"). Workaround/trade-off: you have to spell it out, maybe using the first letters of more common words, like "**N**eptune **u**nicorn **m**oose **p**anda **Y**oda" to spell out "numpy". Afterwards, you can reassign "numpy" to a shorter label that uses more common words, like "numb pie" or "pneumatic".
3. **"Say please"**. Start each new sentence with "please" to mark out a new command or line in the code. (*But* you don't have to: on devices or interfaces that let you enter the newline character, just start your code with "please no need to say please". See [terse mode](#terse-mode).)

I don't intend to replace Python. In fact, python import capability is built right into Please. See [import examples](#import-to-add-functionality) below.

<br>

# More Example Code:

Currently you can: [print out](#print) strings and variable values, create [variables](#create-variables), assign [values/lists to variables](#assign-valueslists-to-variables), [spell out uncommon words](#spell-out-a-special-word), do [basic math](#math), use nested [if statements](#if-statements), use nested [for loops](#for-loops), write [comments](#commentsnotes), [import](#import-to-add-functionality) Python modules, use [imports](#use-an-import-modules-function), use [your own defined functions](#make-and-use-your-own-functions), access [list indices](#access-list-index), use [terse mode](#terse-mode)... 

## Print:

```
please print this string of words
```
--> This prints out: `this string of words`

```
please assign one to variable apple
please print variable apple
```
--> This prints out: `1`

## Create Variables:

By design, Please encourages you to use words instead of letters and short forms -- you're saying it out loud.

```
please create variable apple
```

or

```
please variable banana
```

## Assign Values/Lists to Variables:

```
please assign one to variable apple
please assign three hundred to variable banana
please assign some words to variable coconut
```
--> This generates: `apple = 1`, `banana = 300`, `coconut = 'some words'`

Note: variables automatically get created if you didn't already create them.

```
please assign list from eight to twelve to durian
```
--> This generates: `durian = [ 8 , 9 , 10 , 11 , 12 ]`

```
please assign list of one and two and tree bark to variable crazy list
```
--> This generates: `crazy_list = [ 1 , 2 , 'tree bark' ]`

## Spell Out a Special Word:

```
please spell with the first letters of Neptune unicorn moose panda Yoda
```
--> This evaluates to: `numpy` (NumPy is a Python library you can import: https://en.wikipedia.org/wiki/NumPy) (Also see [import examples](#import-to-add-functionality))

Note: capital letters are treated the same as lowercase letters. Please is case-insensitive.

## Math:

```
please one plus two
```
--> This evaluates to: `3`

```
please one plus one equals two
```
--> This evaluates to: `True`

```
please assign one plus two to variable result
please print variable result
```
--> This prints out: `3`

## If Statements:

```
please if true then print this is a one line if statement
```
---> This prints out: `this is a 1 line if statement`

```
please if one equals one then
    please print this should print
please end if
```
--> This prints out: `this should print`

```
please if one equals two then
    please print it should not print this
please end if
```
--> (This doesn't print anything because the if-statement evaluates to False.)

Note: Please ignores whitespace and newline characters because the spoken word doesn't explicitly mark out paragraphs either. So you could type this too:

```
please if one equals two then please print it should not print this please end if
```

You can use library/format.py to automatically format your Please code.

## For Loops:

```
please assign list from negative one to three to variable circle
please for each index in circle
    please print variable index
please end for
```
--> This prints out: `-1`, `0`, `1`, `2`, `3`

## Comments/Notes:

```
please note this is a comment
```
--> (The transformer ignores this sentence.)

## Make and Use Your Own Functions:

```
please define function test with item
    please print variable item
please end function
please assign it works to other
please use function test on variable other
```
--> This prints: `it works`

## Import to Add Functionality:

```
please import alternate
```
--> This imports: alternate.py (from the local folder)

```
please import test from library
```
--> This performs: `from library import test`
--> This imports: /library/test.py

```
please import spelled with the first letters of Neptune unicorn moose panda Yoda
```
--> This performs: `import numpy`. (You can spell out "numpy" since it's not an everyday word, and your speech recognition software might not already be trained to recognize it.)

```
please import spelled with the first letters of Neptune unicorn moose panda Yoda as noodle
```
--> This performs: `import numpy as noodle`. (So no need to spell it out each time you use it.)

```
please import spelled with the first letters of Neptune unicorn moose panda Yoda as numb pie
```
--> This performs: `import numpy as numb_pie`. (You can also just rename it to whatever your speech recognition software thinks you're saying.)

## Use an Import Module's Function:

```
please import test from library
please use test function of test
please use test function from test
```
--> This performs twice: `test.test_function()`

--> This prints twice: `Yay the import test_function() of test.py from the "library" folder works!`

## Access List Index:

```
please no need to say please
assign list of one and two and tree bark to variable crazy list
assign list from zero to two to sequence
for each item in sequence
    print index variable item of crazy list
end for
```
--> This prints: `1`, `2`, `'tree bark'`

## Example Using numpy.array

Requires numpy already installed to work:

```
please import spelled with the first letters of Neptune unicorn moose panda Yoda as numb pie

please assign list from two to four to array
please print array is variable array

please print use array of numb pie on variable array
please assign use array of numb pie on variable array to output

please print output of array of numb pie is variable output
```
--> This imports `numpy`, creates `array = [ 2 , 3 , 4 ]`, and runs `output = numb_pie.array(array)`

--> This also prints `array is [2, 3, 4]`, `use array of numb pie on [2, 3, 4]`, and `output of array of numb pie is [2 3 4]`

## Terse Mode

```
please no need to say please
print this works
print no need to say please before each line
```
--> This prints out: `this works` and `no need to say please before each line`

<br>

# Inspirations for Please:

https://github.com/hchiam/programmingByVoice

https://github.com/AnotherTest/-English

https://www.youtube.com/playlist?list=PLBOh8f9FoHHiKx3ZCPxOZWUtZswrj2zI0

<br>

# Ideas for Development:

(See the Issues list. Click the "Issues" tab above or go to https://github.com/hchiam/please/issues)
