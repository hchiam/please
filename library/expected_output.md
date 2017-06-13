This file shows expected output for test input code.

# Input Code

Replace the contents of text.txt with the following code:

```
please no need to say please
note this is just sample code
print this string of words
create variable apple
variable banana
assign apple the value one
print variable apple
assign variable banana the value three hundred
assign to coconut the value of some words
assign dragon fruit the value list starting from eight ending at twelve
assign crazy list the value list of one and two and tree bark
assign result the value one plus two
print variable result
if true then print this is a one line if statement
if one equals one then
    print this should print
end if
print there should be nothing between this line
if one equals two then
    print it should not print this
end if
if one equals two then  print it should not print this  end if
print and this line
assign circle the value list starting from negative one ending at three
for each index in circle
    print variable index
end for
note this is a comment
define function test with item
    print variable item
end function
assign other the value it works
use function test on variable other
import alternate
import test from library
use test function of test
use test function from test
assign crazy list the value list of one and two and tree bark
assign sequence the value list starting from zero ending at two
for each item in sequence
    print index variable item of crazy list
end for
import spelled with the first letters of Neptune unicorn moose panda Yoda as numb pie
assign array the value list starting from two ending at four
print array is variable array
print use array of numb pie on variable array
assign output the value of using array of numb pie on variable array
print output of array of numb pie is variable output


define function fibonacci with number
    if variable number equals zero then return zero
    if variable number equals one then return one
    assign answer one the value of using function fibonacci on variable number minus one
    assign answer two the value of using function fibonacci on variable number minus two
    return variable answer one plus variable answer two
end function
assign output the value of use function fibonacci with zero
print step 1: output = variable output
assign output the value of use function fibonacci with one
print step 2: output = variable output
assign output the value of use function fibonacci with two
print step 3: output = variable output
assign output the value of use function fibonacci with three
print step 4: output = variable output
```

# Outputs

Use Terminal/Commandline/Bash: `python transformer.py text.txt`

<br>

The Terminal should print this out:

```

PLEASE WORK...

this string of words
1
3
this is a 1 line if statement
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
array is [2, 3, 4]
use array of numb pie on [2, 3, 4]
output of array of numb pie is [2 3 4]
step 1: output = 0
step 2: output = 1
step 3: output = 1
step 4: output = 2

...THANK YOU!

```