|Regex|Description
|--|--|
|(?=subexp)|look-ahead
(?!subexp)|negative look-ahead
(?<=subexp)|look-behind
(?<!subexp)|negative look-behind

1.  Find all lines that dont start with set of works

     Find lines not starting with WatermarkId or Executing
   
         ^(?!WatermarkID|Executing).*
         
1.  Find all lines that dont contain set of words

     Find lines not starting with WatermarkId or Executing
   
         ^((?!WatermarkID|Executing).)*       
         
1. Find all lines that dont contain the word DataflowName anywhere in the line
         
         ^(?!.*DataflowName).*
         
1. Find all lines that have foo but not preceded by bam or succeeded by bar

        (?<!bam )foo(?!bar)
        
   Test it out: https://regex101.com/r/cmmtVi/1

1. 
