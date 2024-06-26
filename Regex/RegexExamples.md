Most examples are for NotePad++.

Notepad++ regex syntax: https://www.boost.org/doc/libs/1_55_0/libs/regex/doc/html/boost_regex/syntax/perl_syntax.html

Advanced syntax: https://www.boost.org/doc/libs/1_55_0/libs/regex/doc/html/boost_regex/format/boost_format_syntax.html

Reference: https://docs.microsoft.com/en-us/dotnet/standard/base-types/regular-expressions

1. Non-capturing group
   If you dont want to capture some part of the regex
   
        (?:regex)
   
   eg: CN=xxxxxx
   
   if you dont want to capture CN=
   
        (?:CN=)(?<name>.*)
   
   Name will have just xxxxxxx

   This is a better regex and $1 will have just the name.
   
       ^(?:CN=)(.*?),(.*)$

1. Find and remove new lines and comma separate them
   
   Demonstrates grouped capture. $1, represents first group, $2, 2nd group and $0 the full match.
    
    Search:
    
        (.*)(\r\n)
  
    Replace:
    
        $1,
        
1. Find and remove new lines and quote and comma separate them:
     
     Search:
        
        (.*)(\r\n)
      
     Replace:
     
         "$1", 

1. Find and remove new lines and comma separate using named groups instead of 

     Search:
   
        (?<data>(.*))(?<nl>(\r\n))
   
     Replace:
   
         '$+{data}',
        
1.  Lazy vs Greedy Capture

    Regex will normally capture greedily. With the following input text
    
        abcd,efghi,klmno,

    The following regex:

        .*,

    will match the entire input text (abcd,efghi,klmno,)

    If instead what you wanted is each group of text with the comma separately, you would need to make Regex behave lazily (i.e, stop at the first instance of the ,). To do this you use the ? to do a lazy match.

        .*?,

    The above regex will match "abcd," "efghi," and "klmno," separately.

    Now if you wanted to capture just the text before the comma, you can use the lazy operator plus the non-capturing group.

    Search for all character before a "," and dont capture the comma:
  
    Greedy capture (regex?)

    Non capture group (?:regex)
   
        (.*?)(?:,)
         
1. Find all lines that contain the word dataflowname in the line

         (DataflowName.*=.*"(?<wfn>(.*))")

1. Find lines like: abcd run duration 34 minute(s) 36 second(s) and convert it to "abcd 34 36" (tab separated) 

         (?<e>(.*)) run duration((?<m>(.*)) minute\(s\) )?(?<s>(.*)) second\(s\)
         
         $+{e}\t$+{m}\t$+{s}
         
1. Find and replace with Capitals!

         Find all words that start with an **as** and end with a , and convert them to caps:
         
         as (\w+),
         
         as "\U($1)\E",
         
   The \U($1)\E converts the capture group to caps!!!         
         
