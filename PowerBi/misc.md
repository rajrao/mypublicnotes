Example VS Release Tasks: https://github.com/maikvandergaag/msft-extensions/tree/master/azuredevops/powerbiactions


**Sizes of PBIX files when using duplicating tables** vs referencing tables (there is no difference). But each additional table takes up more space.

|Size|Name/Type|
|---:|---|
| 11,889|Blank.pbix
| 95,774|SingleCalendarNoViz.pbix
| 98,132|SingleCalendarWViz.pbix
|387,136|MultipleCalendarWViz.pbix
|387,395|MultipleCalendarsAsReferencesWViz.pbix


**Visualize PBI Refresh**

https://dax.tips/2021/02/15/visualise-your-power-bi-refresh/

**Best Practices**
https://github.com/TabularEditor/BestPracticeRules


**Make a PowerBI Matrix look like a table**

* Row Headers (these are key to making it look like a table)
  * Stepped Layout: off 
  * +/- icons: off

* Other formatting to make it look nice:
	- Style: Default
	- Grid
      - Vertical Grid: On		  
      - Horizontal Grid: On
