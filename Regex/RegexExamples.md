Most examples are for NotePad++.

Notepad++ regex syntax: https://www.boost.org/doc/libs/1_55_0/libs/regex/doc/html/boost_regex/syntax/perl_syntax.html
Advanced syntax: https://www.boost.org/doc/libs/1_55_0/libs/regex/doc/html/boost_regex/format/boost_format_syntax.html

1. Find and remove new lines and comma separate them
   
   Demonstrates grouped capture. $1, represents first group, $2, 2nd group and $0 the full match.
    
    Search:
    
        (.\*)(\r\n)
  
    Replace:
    
        $1,
        
1. Find and remove new lines and comma separate using named groups instead of 

   Search:
   
        (?<data>(.*))(?<nl>(\r\n))
   
   Replace:
   
        '$+{data}',
        
1.  