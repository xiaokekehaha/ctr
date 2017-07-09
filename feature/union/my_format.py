import sys

def string_f(decimal):#format
	return str(round(decimal, 5))

def string_cf(num1, num2):#calculate, format
	decimal = num1 / float(num2)
	return str(round(decimal, 5))
