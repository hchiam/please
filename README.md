# "Please" - a programming language

Please is an experimental programming language that can read (i.e. parse) text generated by speech recognition software like Mac Dictation, so you can code by talking.

# Example code in "Please":

    Please print this string of words

When you run that code, it prints out:

    this string of words

# Why?

What if code could be easy to read like Python code? What if you could easily write code just by talking with speech recognition software? How might you combine these two things (easy-to-read and easy-to-say code)?

Please is an attempt at that.

To make utterances short but also easily understood by speech recognition software:

* **No non-letter characters**. Why? Speed and recognition. Saying "question mark" just to type out "?" is slow and could be faulty if the speech recognition software thinks you literally want the words "question mark".
* **No specialized words or jargon**. Why? So you don't have to specifically train the software to recognize uncommon words like "numpy" (mine thought I said "numb pie"). Workaround/trade-off: you have to spell it out, maybe using the first letters of more common words, like 'Neptune unicorn moose panda Yoda' --> 'numpy'.
* **Just letters and the space character**. (The keyword "spacebar" is recognized by Mac Dictation.)
* **"Be polite"**. Each new sentence starts with "please" and roughly marks out a new command/line in the code.

# Use:

Download this project, open the folder in Terminal/Commandline, and type:

    python interpreter.py text.txt

# Ideas for Development:

* ~~Try to be able to enter words that are likely to not be trained into Mac Dictation by default (like the word 'numpy'). How? Maybe use some kind of spelling convention, like using the first letters of the words 'Neptune unicorn moose panda Yoda' --> 'numpy'.~~

* Try to map number strings to digits.

* Try to import existing python libraries like numpy.

* Try variables. Maybe something like 'variable apple' and 'variable apple equals one'.

* Try embedded expressions. Maybe use "thanks" as a closing bracket of sorts?

* Try trinket that loads most recent python code from github.

# Inspirations for "Please":

https://github.com/hchiam/programmingByVoice

https://github.com/AnotherTest/-English

https://www.youtube.com/playlist?list=PLBOh8f9FoHHiKx3ZCPxOZWUtZswrj2zI0
