<img src="https://github.com/hchiam/please/blob/master/library/please_icon.jpeg" height="250" title="Please scroll down to read more">

# "Please" - An Experimental Programming Language

**Simply put:** Program by talking to your computer using common English words. 

**More technically:** You can easily write code in Please using speech recognition software (like Dragon NaturallySpeaking, Mac Dictation, or Google Voice Typing) out-of-the-box, without having to train the software to recognize esoteric jargon and special keywords for symbols. As of release [v0.2.0](https://github.com/hchiam/please/releases): transformer.py compiles Please into Python code and runs that. 

Presentation at [Round 13](https://www.meetup.com/Toronto-Hack-and-Tell/events/239650451/?_cookie-check=p9kqjtLjZT2eIqkU) of Toronto Hack && Tell: https://goo.gl/mcdLYH

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

No speech recognition software? No Python? Just type code in your browser: https://goo.gl/zk1LFu (go to the text.txt tab to write code in Please).

## B) On Your Computer (Full Version):

1. Download this project from GitHub. https://github.com/hchiam/please/archive/master.zip --> master branch. Or get a different version at https://github.com/hchiam/please/releases

2. Open the folder using Terminal or Command-line.

3. Then input the following command and hit enter:

```
python transformer.py text.txt
```

The *transformer* will turn the *text* file (Please "source code") into Python code, and then run that. 

Requires Python 3: https://www.python.org/downloads

This project was built with Python 3.6.0

<br>

# Why?

Less carpal tunnel syndrome? More accessible programming for people with a mobility impairment? Code while you exercise?

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
please assign apple the value one
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
please assign apple the value one
please assign variable banana the value three hundred
please assign to coconut the value of some words
```
--> This generates: `apple = 1`, `banana = 300`, `coconut = 'some words'`

Note: variables automatically get created if you didn't already create them.

```
please assign dragon fruit the value list starting from eight ending at twelve
```
--> This generates: `dragon fruit = [ 8 , 9 , 10 , 11 , 12 ]`

```
please assign crazy list the value list of one and two and tree bark
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
please assign result the value one plus two
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
please if one equals two then  print it should not print this  end if
```

You can use library/format.py to automatically format your Please code.

## For Loops:

```
assign circle the value list starting from negative one ending at three
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
please assign other the value it works
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
assign crazy list the value list of one and two and tree bark
assign sequence the value list starting from zero ending at two
for each item in sequence
    print index variable item of crazy list
end for
```
--> This prints: `1`, `2`, `'tree bark'`

## Example Using numpy.array

Requires numpy already installed to work:

```
please import spelled with the first letters of Neptune unicorn moose panda Yoda as numb pie

assign array the value list starting from two ending at four
please print array is variable array

please print use array of numb pie on variable array
please assign output the value of using array of numb pie on variable array

please print output of array of numb pie is variable output
```
--> This imports `numpy`, creates `array = [ 2 , 3 , 4 ]`, and runs `output = numb_pie.array(array)`

--> This also prints `array is [2, 3, 4]`, `use array of numb pie on [2, 3, 4]`, and `output of array of numb pie is [2 3 4]`

## Example Fibonacci

```
Please define function Fibonacci with number
Please if number under two then return number
Please assign apple the value of using function Fibonacci on number -1
Please assign banana the value of using function Fibonacci on number -2
Please assign coconut the value of variable apple plus variable banana
Please return variable coconut
Please done function
Please assign input the value list starting from 0 ending at 8
Please for each Number in input
Please assign output the value of using function Fibonacci on number
Please print variable output
Please done for
```
--> This compiles to:

```
def fibonacci(number):
	if number < 2:
		return number
	
	apple = fibonacci(number -1)
	banana = fibonacci(number -2)
	coconut = apple + banana
	return coconut

input = [ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 ]
for number in input:
	output = fibonacci(number)
	print(str(output))
```

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

https://www.youtube.com/playlist?list=PLBOh8f9FoHHiKx3ZCPxOZWUtZswrj2zI0 (especially for [v0.1.0](https://github.com/hchiam/please/releases))

# You may also like: 

https://github.com/hchiam/code-tutor

https://github.com/hchiam/language-user-interface

https://github.com/hchiam/how

<br>

# Ideas for Development:

(See the Issues list. Click the "Issues" tab above or go to https://github.com/hchiam/please/issues)
