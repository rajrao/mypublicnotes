**1. Capture the CN name**

input ```CN=happy_group,OU=Security Groups,DC=my,DC=xyz,DC=com```

Regex ```^.*CN=(.*?),.*```

replace ```$1```

Output: ```happy_group```

**2. Capture key value pairs from a URL/Path** https://regex101.com/r/h7a2e3/1

input ```./part=a/date=2012-01-01/test.parquet```  
regex ```[\/\\]([^\/\\\?]+)=([^\\\/\\n\?]+)```  
output:
```
/part=a
part
a
/date=2012-01-01
date
2012-01-01
```
