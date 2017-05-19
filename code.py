def fibonacci(number):
	if number <2:
		return number
	
	apple = fibonacci(number -1)
	banana = fibonacci(number -2)
	coconut = apple + banana
	return coconut

input = [ 0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 ]
for number in input:
	output = fibonacci(number)
	print(str(output))

