Here is a recreation of the CaseMilestone query from Sales Force objects (meant to be run on a database replica of the SalesForce data (eg: a data lake))

```sql
select 
		c.casenumber "Case number", 
		c."type" "Type",
		round((gettimeinmillis(c.closeddate) - gettimeinmillis(c.createddate))/(1000.0*60*60)) as Age, 
       	c.createddate "Date/Time Opened", 
       	c.closeddate "Date/Time Closed",
	       case
	              when ch.field = 'created' then 'New'
	              when ch.field = 'closed' then 'Closed'
	              when ch.field = 'Status' then ch.newvalue
	       end as "Case History Status",
       chocase.name as "Created by ",  
       cho.name "Case History Last Modified by ", 
       ch.createddate as "Case History Last Modified Date", 
       round(
              (
                     abs(
                           gettimeinmillis(lag(ch.createddate, 1, c.createddate) over (partition by ch.caseid order by ch.createddate desc, ch.id desc))
                           - gettimeinmillis(ch.createddate)
                     )
              )/(1000.0 * 60 * 60)
       ,4 
) as Duration
, a.name "Account Name"
from case c 
join casehistory ch on c.id = ch.caseid 
left join user cho on ch.createdbyid = cho.id 
left join user chocase on c.createdbyid = chocase.id
left join account a on a.id = c.accountid
where ch.field in ('Status', 'created', 'closed');
```
