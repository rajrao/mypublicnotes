**1. Capture the CN name**

input ```CN=happy_group,OU=Security Groups,DC=my,DC=xyz,DC=com```

Regex ```^.*CN=(.*?),.*```

replace ```$1```

Output: ```happy_group```
