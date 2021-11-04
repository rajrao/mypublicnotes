Most examples are for NotePad++.

Notepad++ regex syntax: https://www.boost.org/doc/libs/1_55_0/libs/regex/doc/html/boost_regex/syntax/perl_syntax.html

Advanced syntax: https://www.boost.org/doc/libs/1_55_0/libs/regex/doc/html/boost_regex/format/boost_format_syntax.html

Reference: https://docs.microsoft.com/en-us/dotnet/standard/base-types/regular-expressions

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
        
1.  Greedy Capture

     Search for all character before a "," and dont capture the comma:
  
     Greedy capture (regex?)
     Non capture group (?:regex)
   
         (.*?)(?:,)

1.  Find all lines that dont start with set of works

     Find lines not starting with WatermarkId or Executing
   
         ^(?!WatermarkID|Executing).*
         
1.  Find all lines that dont contain set of words

     Find lines not starting with WatermarkId or Executing
   
         ^((?!WatermarkID|Executing).)*       
         
1. Find all lines that dont contain the word DataflowName anywhere in the line
         
         ^(?!.*DataflowName).*
         
1. Find all lines that contain the word dataflowname in the line

         (DataflowName.*=.*"(?<wfn>(.*))")

1. Find lines like: abcd run duration 34 minute(s) 36 second(s) and convert it to "abcd 34 36" (tab separated) 

         (?<e>(.*)) run duration((?<m>(.*)) minute\(s\) )?(?<s>(.*)) second\(s\)
         
         $+{e}\t$+{m}\t$+{s}
         
1. 
