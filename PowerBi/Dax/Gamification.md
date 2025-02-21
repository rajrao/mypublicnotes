```
Gamificiation Icon = 
var has_one_value = HASONEVALUE('Events'[User])
return if (has_one_value,
    var event_count = Count('Events'[Id])
    var category = SELECTEDVALUE('Event Type'[Type])
    var tbl_categories = Filter('Gamification Levels','Gamification Levels'[Category] = category)
    var tbl_events = Filter(tbl_categories,[_events] < event_count)
    return SELECTCOLUMNS(TOPN(1,tbl_events,[_events],DESC),[Icon]) & SELECTCOLUMNS(TOPN(1,tbl_events,[_events],DESC),[Multiplier])
)
```

![image](https://github.com/user-attachments/assets/8e869368-06fd-4474-a078-9fda0ae2b890)

Gamification levels is created in PowerQuery using a table with Unicode values  
![image](https://github.com/user-attachments/assets/815bce1c-7654-49a0-a1a6-cd4261a14c34)

Following power query is used to convert to Unicode:  
```
= Table.AddColumn(#"Replaced Value", "Custom", each Character.FromNumber(Expression.Evaluate([Icons])))
```

![image](https://github.com/user-attachments/assets/21b40bfa-b21b-4bbe-875b-e578e8b90b4b)

