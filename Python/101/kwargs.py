#https://replit.com/@rajrao2/kwargs-test

def testKwargs(*args, **kwargs):
  """
  * collects all the positional arguments in a tuple.
  ** collects all the keyword arguments in a dictionary
  """
  print(args)
  print(kwargs)

print("Test of positional and named arguments")
testKwargs(1, 2, 3, 4, 5, 6, a=7, b=8, c=9)

list=[1, 2, 3, 4]
dict={'a': 10, 'b':20}
"""
* unpacks a list or tuple into position arguments.
** unpacks a dictionary into keyword arguments.
"""
print("Test of unpacking of lists and dictionaries")
testKwargs(*list, **dict)

print("Test of unpacking of tuples and dictionaries")
testKwargs(*(11,22), **{"hello":"world"})
