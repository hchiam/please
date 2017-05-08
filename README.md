<img src="https://github.com/hchiam/please/blob/master/library/please_icon.jpeg" height="250" title="Please scroll down to read more">

# "Please" - An Experimental Programming Language

**Simply put:** Program by talking to your computer using common English words. 

**More technically:** You can easily write code in Please using speech recognition software (like Mac Dictation) out-of-the-box, without having to train the software to recognize esoteric jargon and special keywords for symbols. 

<br>

# Example Code in Please:

First transcribe this code:

```
Please print this string of words
```

When you run that code, it prints out:

```
this string of words
```

<br>

# Try It:

## A) In Your Browser (Mini Version):

No speech recognition software? No Python? Just type code in your browser: https://trinket.io/python3/18deba3c24 (go to the text.txt tab to write code in Please).

## B) On Your Computer (Full Version):

1. Download this project from GitHub. https://github.com/hchiam/please/archive/master.zip --> master branch.

2. Open the folder using Terminal or Command-line.

3. Then input the following command and hit enter:

```
python interpreter.py text.txt
```

The *interpreter* will interpret and run the *text* file as "source code" written in Please.

Requires Python 3: https://www.python.org/downloads

<br>

# Why?

What if you could easily write code just by talking with speech recognition software? What if code could be *more* like English sentences? How might you combine these two things (easy-to-parse and easy-to-say code)?

Please is an attempt at that.

Here are 3 ground rules to make commands easier to say, but also easier for speech recognition software and Please's code interpreter to understand:

1. **Just say words that use your ABCs and spaces between**. No special non-letter characters like "?". Why? Speed and recognition. Saying "question mark" just to type out "?" is slow and could be faulty if the speech recognition software thinks you literally want the words "question mark". Please also doesn't differentiate (non-)capital letters because it's a speech-based language (vs. a "written language").
2. **Avoid specialized words or names**. Why? So you don't have to specifically train your speech recognition software to recognize uncommon words like "numpy" (mine thought I said "numb pie"). Workaround/trade-off: you have to spell it out, maybe using the first letters of more common words, like "**N**eptune **u**nicorn **m**oose **p**anda **Y**oda" to spell out "numpy". Afterwards, you can reassign "numpy" to a shorter label that uses more common words, like "numb pie" or "pneumatic".
3. **"Say please"**. Each new sentence starts with "please" and roughly marks out a new command or line in the code. Some devices or interfaces don't let you enter the newline character.

I don't intend to replace Python. In fact, python import capability is built right into Please. See [import examples](#import-to-add-functionality) below.

<br>

# More Example Code:

Currently you can: [print](#print) strings and variable values, create [variables](#create-variables), assign [values/lists to variables](#assign-values-lists-to-variables), do [basic math](#math), use (nested) [if-then-(end-if) statements](#if-statements) and [one-liner if-then statements](#if-statements), use (nested) [for loops](#for-loops), write [comments](#comments-notes), [spell out words](#spell-out-a-special-word), do [imports](#import-to-add-functionality), use [imported functions](#use-an-import-modules-function), use [your own defined functions](#use-your-own-functions), access [list indices](#access-list-index), ... 

## Print:

```
Please print this string of words
```
--> This prints out: `this string of words`

```
Please assign one to variable apple
Please print variable apple
```
--> This prints out: `1`

## Create Variables:

By design, Please encourages you to use words instead of letters and short forms -- you're saying it out loud.

```
Please create variable apple
```

or

```
Please variable banana
```

## Assign Values/Lists to Variables:

```
Please assign one to variable apple
Please assign three hundred to variable banana
Please assign some words to variable coconut
```
--> This generates: `apple = 1`, `banana = 300`, `coconut = 'some words'`

Note: variables automatically get created if you didn't already create them.

```
Please assign list from eight to twelve to durian
```
--> This generates: `durian = [8, 9, 10, 11, 12]`

```
Please assign list of one and two and tree bark to variable crazy list
```
--> This generates: `crazy list = [1, 2, 'tree bark']`

## Spell Out a Special Word:

```
Please spell with the first letters of Neptune unicorn moose panda Yoda
```
--> This evaluates to: `numpy` (NumPy is a Python library you can import: https://en.wikipedia.org/wiki/NumPy) (Also see [import examples](#import-to-add-functionality))

Note: capital letters are treated the same as lowercase letters. Please is case-insensitive.

## Math:

```
Please one plus two
```
--> This evaluates to: `3`

```
Please one plus one equals two
```
--> This evaluates to: `True`

```
Please assign one plus two to variable result
Please print variable result
```
--> This prints out: `3`

## If Statements:

```
Please if true then print this is a one line if statement
```
---> This prints out: `this is a one line if statement`

```
Please if one equals one then
    Please print this should print
Please end if
```
--> This prints out: `this should print`

```
Please if one equals two then
    Please print it should not print this
Please end if
```
--> (This doesn't print anything because the if-statement evaluates to False.)

Note: Please ignores whitespace and newline characters because the spoken word doesn't explicitly mark out paragraphs either. So you could type this too:

```
Please if one equals two then please print it should not print this please end if
```

You can use library/format.py to automatically format your Please code.

## For Loops:

```
Please assign list from negative one to three to variable circle
Please for each index in circle
    Please print variable index
Please end for
```
--> This prints out: `-1`, `0`, `1`, `2`, `3`

## Comments/Notes:

```
Please note this is a comment
```
--> (The interpreter ignores this sentence.)

## Import to Add Functionality:

```
Please import alternate
```
--> This imports: alternate.py (from the local folder)

```
Please import test from library
```
--> This imports: /library/test.py

```
Please import spelled with the first letters of Neptune unicorn moose panda Yoda
```
--> This performs: `import numpy`. (You can spell out "numpy" since it's not an everyday word, and your speech recognition software might not already be trained to recognize it.)

```
Please import spelled with the first letters of Neptune unicorn moose panda Yoda as noodle
```
--> This performs: `import numpy as noodle`. (So no need to spell it out each time you use it.)

```
Please import spelled with the first letters of Neptune unicorn moose panda Yoda as numb pie
```
--> This performs: `import numpy as numb pie`. (You can also just rename it to whatever your speech recognition software thinks you're saying.)

## Use an Import Module's Function:

```
Please import test from library
Please use test_function of test
Please use test_function from test
```
--> This performs twice: `test.test_function()`

--> This prints twice: `Yay the import test_function() of test.py from the "library" folder works!`

## Use Your Own Functions:

```
Please define function test with item
    Please print variable item
Please end function
Please assign it works to other
Please use function test on variable other
```
--> This prints: `it works`

## Access List Index:

```
Please assign list of one and two and tree bark to variable crazy list
Please for each item in crazy list
    Please print index variable item of crazy list
Please end for
```
--> This prints: `1`, `2`, `'tree bark'`

<br>

# Inspirations for Please:

https://github.com/hchiam/programmingByVoice

https://github.com/AnotherTest/-English

https://www.youtube.com/playlist?list=PLBOh8f9FoHHiKx3ZCPxOZWUtZswrj2zI0

<br>

# Ideas for Development:

(See the Issues list. Click the "Issues" tab above or go to https://github.com/hchiam/please/issues)
