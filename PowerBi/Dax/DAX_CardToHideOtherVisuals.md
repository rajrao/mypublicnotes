When you need to hide a visual (eg: table) and show it only when a record is selected

```
Card Title = if (not HASONEVALUE(Location[Location]),"Select a location","")
```

```
Card Background = IF (HASONEVALUE( Location[Location]),"#FFFFFF00","White")
```

1. Create a card and add the "Card Title" as its field.
2. Set its background to "Card Background"
3. Place the card over the visual you need hidden.


In this example, the table is hidden until a location is selected.
![image](https://user-images.githubusercontent.com/1643325/197056915-addf1ba2-0b54-40c5-bf82-2d8f96819310.png)

When a map point is selected:
![image](https://user-images.githubusercontent.com/1643325/197057001-eac1fe93-09a0-4025-b948-8d1ef861270c.png)
