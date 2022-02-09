Shows 2 ways to do it:


```
with cte (url) as
(
	select 'https://www.google.com/'
	union
	select 'https://www.google.com'
	union
	select 'https://images.google.com'
	union
	select 'https://www.google.com/xxxxx/iyewhnh/xd'
	union
	select 'https://www.google.com/xxxxx/iyewhnh/xd'
	union
	select 'http://www.google.com/'
)
select
	substring(url from INSTR(url, '//') + 3 for case when instr(substring(url, INSTR(url, '//') + 2), '/') =-1 then 1000 else instr(substring(url, INSTR(url, '//') + 2), '/') end ),
	substring(url, 
		INSTR(url, '//') + 2,  -- start after the protocol bit http:// or https://
		case 
			when instr(substring(url, INSTR(url, '//') + 2), '/') =-1 then 1000 else --after the first set of slashes look for next /. if not found, get till end
			instr(substring(url, INSTR(url, '//') + 2), '/') + INSTR(url, '//') + 2  --the first single slash was found, so get text between first set of slashes //xxxx/
		end)
from
	cte
order by 1
```
