|Regex|Description
|--|--|
|(?=subexp)|positive look-ahead
(?!subexp)|negative look-ahead
(?<=subexp)|positive look-behind
(?<!subexp)|negative look-behind

          (?<=foo)bar    positive look-behind
Will match foobar but only capture bar. It will not barometer, bar, baron, etc. (https://regex101.com/r/SFLS8w/1)
          
          foo(?=bar)    positive look-ahead
Will match foobar but not football, bamfoo or foo. (https://regex101.com/r/GK2cD0/1)   

**More Examples**

1.  Find all lines that dont start with set of works

     Find lines not starting with WatermarkId or Executing
   
         ^(?!WatermarkID|Executing).*             negative look-ahead
         
1.  Find all lines that dont contain set of words

     Find lines not starting with WatermarkId or Executing
   
         ^((?!WatermarkID|Executing).)*           negative look-ahead     
         
1. Find all lines that dont contain the word DataflowName anywhere in the line
         
         ^(?!.*DataflowName).*                    negative look-ahead
         
1. Find all lines that have foo but not preceded by bam or succeeded by bar

        (?<!bam )foo(?!bar)                       negative look-behind & negative look-ahead
        
   Test it out: https://regex101.com/r/cmmtVi/1

1. 
