This file shows expected output for test input code.

# Input Code

Put this code into text.txt:

```
Please print this string of words
Please create variable apple
Please variable banana
Please assign one to variable apple
Please print variable apple
Please assign three hundred to variable banana
Please assign some words to variable coconut
Please assign list from eight to twelve to durian
Please assign list of one and two and tree bark to variable crazy list
Please assign one plus two to variable result
Please print variable result
Please if true then print this is a one line if statement
Please if one equals one then
    Please print this should print
Please end if
please print there should be nothing between this line
Please if one equals two then
    Please print it should not print this
Please end if
Please if one equals two then please print it should not print this please end if
please print and this line
Please assign list from negative one to three to variable circle
Please for each index in circle
    Please print variable index
Please end for
Please note this is a comment
Please define function test with item
    Please print variable item
Please end function
Please assign it works to other
Please use function test on variable other
Please import alternate
Please import test from library
Please use test_function of test
Please use test_function from test
Please assign list of one and two and tree bark to variable crazy list
Please for each item in crazy list
    Please print index variable item of crazy list
Please end for
please import spelled with the first letters of Neptune unicorn moose panda Yoda as numb pie
please assign list from two to four to array
please print array is variable array
please print use array of numb pie on variable array
please assign use array of numb pie on variable array to output
please print output of array of numb pie is variable output
```

# Outputs

Use Terminal/Commandline/Bash: `python interpreter.py text.txt`

The variable dictionary should look like this:

```
{'test':<…>, 'apple':1, 'banana':300, 'coconut':'some words', 'durian':[8,9,10,11,12], 'crazy list':[1,2,'tree bark'], 'result':3,'circle':[-1,0,1,2,3], 'other':'it works', 'array':[2,3,4], 'output':[2,3,4]}
```

The import dictionary should look like this:

```
{'alternate':<…>,'test':<…>,'numbpie':<…>}
```

The Terminal should print this out:

```
this string of words
1
3
this is a one line if statement
this should print
there should be nothing between this line
and this line
-1
0
1
2
3
it works
Yay the import test_function() of test.py from the "library" folder works!
Yay the import test_function() of test.py from the "library" folder works!
1
2
tree bark
array is [2,3,4]
use array of numb pie on [2,3,4]
output of array of numb pie is [2,3,4]
```