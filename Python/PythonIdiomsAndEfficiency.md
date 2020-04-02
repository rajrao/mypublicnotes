From: [Python Idioms and Efficiency 1/28/07](https://www.memonic.com/user/pneff/folder/python/id/1bufp)
-------------------------------------------------------------------------------------------------
[bayes.colorado.edu](http://bayes.colorado.edu/PythonIdioms.html "http://bayes.colorado.edu/PythonIdioms.html")

Python Idioms and Efficiency 1/28/07
====================================

Written by [Rob Knight](mailto:rob@spot.colorado.edu) for the Cogent project
----------------------------------------------------------------------------

Table of Contents
-----------------

### [What idioms should I use to make my code easier to read?](http://bayes.colorado.edu/PythonIdioms.html#idioms_readable)

### [What techniques should I use to make my code run faster?](http://bayes.colorado.edu/PythonIdioms.html#idioms_efficient)

### [Back to the coding guidelines](http://bayes.colorado.edu/PythonGuidelines.html)

What idioms should I use to make my code easier to read?
--------------------------------------------------------

**Read "The Python Cookbook", especially the first few chapters.** It's a great source of well-written Python code examples.

**Build strings as a list and use `''.join` at the end.** `join` is a string method called on the separator, not the list. Calling it from the empty string concatenates the pieces with no separator, which is a Python quirk and rather surprising at first. **This is important: string building with + is quadratic time instead of linear! If you learn one idiom, learn this one.**

**Wrong:** for s in strings: result += s
**Right:** result = ''.join(strings)

**Always use an object's capabilities instead of its type.** Python is a dynamically typed language: you should basically never care whether an object is a particular type as long as it supports a particular interface. This can give you impressive polymorphism for free. For example, my code for checking whether a string is valid on an alphabet looks like this:

for char in string:
    if char not in alphabet:
        raise ValueError, "Char %s not in alphabet %a" % (char, alphabet)

It doesn't matter whether `alphabet` is a string, a dict, a list, or an object that I define as long as it supports the __contains__ special method.

**Use `in` wherever possible** (you can override `__contains__` to support `if x in y` syntax and `__iter__` to support `for x in y` syntax in your own classes). This keeps your statements general and polymorphic.

**Better:** for key in d: print key     #also works for arbitrary sequence
**Worse:**  for key in d.keys(): print key #limited to objects with keys()
**Better:** if key not in d: d[key] = []
**Worse:**  if not dict.has_key(key): d[key] = []

Note: you still need to use `d.keys()` if you want to mutate the dictionary. `for key in d: del d[key]` will raise `RuntimeError: dictionary changed size during iteration`. Use `for key in d.keys(): del d[key]` instead.

**Use coercion if an object must be a particular type.** If `x` must be a string for your code to work, why not call `str(x)` instead of trying something like `isinstance(str, x)`? You can wrap it in a `try/except` if you want to catch the errors, and will probably end up with a solution that's much more general than if you had tried to anticipate every possibility.

**Use `if not x` instead of `if x == 0`** or `if x == ""` or `if x == None` or `if x == False`; **likewise, `if x` instead of `if x != 0`**, `if x != None`, etc. Exception: for numbers, 0 is a false value, so you may need to distinguish between 0 and the other things that return `False`. Beware of comparing a floating point value that is supposed to be zero with `int(0)` or `float(0.0)`: rounding error can cause infuriating bugs.

**Use string methods rather than the string module.** For example, use s.startswith('abc') rather than startswith(s, 'abc'). This lets you use other objects that just support a small part of the string interface (e.g. ones you write yourself): the string module functions generally expect real strings. There are a few cases where you need to `import string`: for example, `maketrans` is still only available through the string module. However, in general, seeing that import statement is a warning sign.

**Use `for line in infile`, not `for line in infile.readlines()`.** `readlines` and `xreadlines` are deprecated in Python 2.3 anyway in favor of the new iterator protocol. The `for line in infile` version allows `infile` to be anything that acts like a sequence of lines, such as a list, which can greatly aid testing. Actually, just use `**for line in lines**`: you should basically never care whether the lines come from a file, a list of strings, some other iterator, the keys of a dict, or whatever.

**To reverse-sort a list, use:**

    list.sort()
    list.reverse()

It's much easier to read and, incidentally, faster than the tricky 1-line alternatives. Remember that in-place methods like `sort()` and `reverse()` do not return a value. This can be surprising, because if you do something like `sorted_list = orig_list.sort()` then `sorted_list` is `None` and `orig_list` is now in sorted order. Note that if you just want to iterate over the reversed list, you can (in Python 2.5, at least) use `for i in reversed(sorted(orig_list))`.

**Use 'while 1:' for infinite loops, or to always execute the loop body at least once.** This is just a Python idiom, but it's what other people will expect to see once they're used to the language. For example:

    while 1:
        curr_line = reader.next()
        if not curr_line:
            break
        curr_line.process()

**Catch errors rather than avoiding them to avoid cluttering your code with special cases.** This idiom is called EAFP ('easier to ask forgiveness than permission'), as opposed to LBYL ('look before you leap'). This often makes the code more readable. For example:

**Worse:**

    #check whether int conversion will raise an error
    if not isinstance(s, str) or not s.isdigit:
        return None
    elif len(s) > 10:    #too many digits for int conversion
        return None
    else:
        return int(str)

**Better:**

    try:
        return int(str)
    except (TypeError, ValueError, OverflowError): #int conversion failed
        return None

(Note that in this case, the second version is much better, since it correctly handles leading + and -, and also values between 2 and 10 billion (for 32-bit machines). Don't clutter your code by anticipating all the possible failures: just try it and use appropriate exception handling.)

**Catch only the appropriate errors.** It is incredibly risky to use `catch` without specifying which errors you want to intercept, since it will get everything. If you are expecting a particular kind of error, such as a `ZeroDivisionError` or a `ValueError`, don't catch everything else as well on the assumption that those are the only ones that could come up. You might be out of memory instead, or you might have passed in an object that doesn't have the right attribute or hasn't implemented the operation. Masking these unexpected errors makes debugging very difficult, especially if you print misleading error messages.

**Swap values without using temporary variables.** Instead, use implicit tuple unpacking. You can write `a, b = b, a` to swap a and b. In fact, you can do this with as many items as you like: `a, b, c, d = d, b, c, a` to map `a` to `d`, etc.

**Use zip to get a list's (or any sequence's) items with their indices:**

        indices = xrange(maxint)    #only need this once; mine is in Utils.py
            for d, index in zip(data, indices):
            #do something with d and index here

(Note that Python 2.3 provides enumerate(data), which provides lazy evaluation of the sequence and makes this idiom largely unnecessary. It can still be useful when you want to include an index along with several other lists, however, e.g. zip(list_1, list_2, indices). May fail on some 64-bit systems.)

If you do not need the indices, just do:

    for i in items:
        something(i)

...rather than:

    for index in range(len(items)):
        something(items[index])

    (which is more typing, uglier, and slower.)

What techniques should I use to make my code run faster?
--------------------------------------------------------

**Always profile before you optimize for speed.** You should always optimize for readability first: it's easier to tune readable code than to read 'optimized' code, especially if the optimizations are not effective. Before using any technique that makes the code less readable, you should check that it's actually a bottleneck in your application by running your application with the built-in `profile.py` script. If your program spends 10% of its time running a particular method, even if you increase its speed tenfold you've only shaved 9% off the total running time.

**Always use a good algorithm when it is available.** The exception to the above rule is when there are known large differences in the time complexity of alternative algorithms. Reducing running time from quadratic to linear, or from exponential to polynomial, is always worth doing unless you are sure that the data sets will always be tiny (less than a couple of dozen items).

**Use the simplest option that could possibly work.** Don't use a regular expression if you just want to see if a string starts with a particular substring: use `.startswith` instead. Don't use `.index` if you just want to see if a string contains a particular letter: use `in` instead. Don't use `StringIO` if you could just use a list of strings. In general, keeping it simple cuts down on bugs and makes your code more readable. Even a complicated combination of `.index` calls will be much faster than a regular expression, and probably easier to decipher if you're just matching rather than capturing the result.

**Build strings as a list and use `''.join` at the end.** Yes, you already saw this one above under "Python Idioms", but it's such an important one that I thought I'd mention it again. `join` is a string method called on the separator, not the list. Calling it from the empty string concatenates the pieces with no separator, which is a Python quirk and rather surprising at first. **This is important: string building with + is quadratic time instead of linear!**

**Wrong:**

    for s in strings: result += s

**Right:**
    
    result = ''.join(strings)

**Use tests for object identity when appropriate:** `if x is not None` rather than `if x != None`. It is much more efficient to test objects for identity than equality, because identity only checks their address in memory (two objects are identical if they are the same object in the same physical location) and not their actual data.

**Use dictionaries (or sets) for searching, not lists.** To find items in common between two lists, make the first into a dictionary and then look for items in the second in it. Searching a list for an item is linear-time, while searching a dict or set for an item is constant time. This can often let you reduce search time from quadratic to linear.

**Use the built-in `sort` wherever possible.** `sort` can take a custom comparison function as a parameter, but this makes it very slow because the function has to be called at least O(n log n) times in the inner loop. To save time, turn the list of items into a list of tuples, where the first element of each tuple has the precalculated value of the function for each item (e.g. extracting a field), and the last element is the item itself.

This idiom is called DSU for 'decorate-sort-undecorate.' In the 'decorate' step, make a list of tuples containing `(transformed_value, second_key, ... , original value)`. In the 'sort' step, use the built-in `sort` on the tuples. In the 'undecorate' step, retrieve the original list in the sorted order by extracting the last item from each tuple. For example:

    aux_list = [i.Count, i.Name, ... i) for i in items]
    aux_list.sort()    #sorts by Count, then Name, ... , then by item itself
    sorted_list = [i[-1] for i in items] #extracts last item

For more recent versions of Python, DSU is often unnecessary. [This page](http://wiki.python.org/moin/HowTo/Sorting) has a good discussion of different sorting techniques in Python.

**Use `map` and/or `filter` to apply functions to lists.** `map` applies a function to each item in a list (technically, sequence) and returns a list of the results. `filter` applies a function to each item in a sequence, and returns a list containing only those items for which the function evaluated `True` (using the `__nonzero__` built-in method). These functions can make code much shorter. They also make it much faster, since the loop takes place entirely in the C API and never has to bind loop variables to Python objects.

**Worse:**

    strings = []
    for d in data:
        strings.append(str(d))

**Better:**

    strings = map(str, data)

**Use list comprehensions where there are conditions attached, or where the functions are methods or take more than one parameter.** These are cases where `map` and `filter` do badly, since you have to make up a new one-argument function that does the operation you want. This makes them much slower, since more work is done in the Python layer. List comprehensions are often surprisingly readable.

**Worse:**

    result = []
    for d in data:
        if d.Count > 4:
            result.append[3*d.Count]

**Better:**

    result = [3*d.Count for d in data if d.Count > 4]

If you find yourself making the same list comprehension repeatedly, make utility functions and use `map` and/or `filter`:

    def triple(x):
        """Returns 3 * x.Count: raises AttributeError if .Count missing."""
        return 3 * x.Count

    def check_count(x):
        """Returns 1 if x.Count exists and is greater than 3, 0 otherwise."""
        try:
            return x.Count > 3
        except:
            return 0

    result = map(triple, filter(check_count, data))

**Use function factories to create utility functions.** Often, especially if you're using `map` and `filter` a lot, you need utility functions that convert other functions or methods to taking a single parameter. In particular, you often want to bind some data to the function once, and then apply it repeatedly to different objects. In the above example, we needed a function that multiplied a particular field of an object by 3, but what we really want is a factory that's able to return for any field name and amount a multiplier function in that family:

    def multiply_by_field(fieldname, multiplier):
        """Returns function that multiplies field "fieldname" by multiplier."""
        def multiplier(x):
            return getattr(x, fieldname) * multiplier
        return multiplier

    triple = multiply_by_field('Count', 3)
    quadruple = multiply_by_field('Count', 4)
    halve_sum = multiply_by_field('Sum', 0.5)

This is a very powerful and general technique for producing functions that might do something like search a specified field for a list of words, or perform several actions on different fields of a particular object, etc. It's a pain to write a lot of little functions that do very similar things, but if they're produced by a function factory it's easy.

**Use the operator module and `reduce` to get sums, products, etc.** `reduce` takes a function and a sequence. First it applies the function to the first two items, then it takes the result and applies the function to the result and the next item, takes that result and applies the function to it and the next item, and so on until the end of the list. This makes it very easy to accumulate items along a list (or, in fact, any sequence). Note that Python 2.3 has a built-in sum() function (for numbers only), making this less necessary than it used to be.

**Worse:**
    
    sum = 0
    for d in data:
        sum += d
    product = 1
    for d in data:
        product *= d

**Better:**
from operator import add, mul
sum = reduce(add, data)
product = reduce(mul, data)

**Use `zip` and `dict` to map fields to names.** `zip` turns a pair of sequences into a list of tuples containing the first, second, etc. values from each sequence. For example, `zip('abc', [1,2,3]) == [('a',1),('b',2),('c',3)]`. You can use this to save a lot of typing when you have fields in a known order that you want to map to names:

**Bad:**

    fields = '|'.split(line)
    gi = fields[0]
    accession = fields[1]
    description = fields[2]
    #etc.
    lookup = {}
    lookup['GI'] = gi
    lookup['Accession'] = accession
    lookup['Description'] = description
    #etc.

**Good:**

    fieldnames = ['GI', 'Accession', 'Description'] #etc.
    fields = '|'.split(line)
    lookup = dict(zip(fieldnames, fields))

**Ideal:**

    def FieldWrapper(fieldnames, delimiter, constructor=dict):
    """Returns function that splits a line and wraps it into an object.

    Field names are passed in as keyword args, so constructor must be
    expecting them as such.
    """
    def FieldsToObject(line):
        fields = [field.strip() for field in line.split(delimiter)]
        result = constructor(**dict(zip(fieldnames, fields)))
    return FieldsToObject

    FastaFactory = FieldWrapper(['GI','Accession','Description'], '|', Fasta)
    TaxonFactory = FieldWrapper(['TaxonID', 'ParentID', ...], '|', Taxon)
    CodonFreqFactory = FieldWrapper(['UUU', 'UUC', 'UUA',...], ' ', CodonFreq)
    #etc for similar data, including any database tables you care to wrap
