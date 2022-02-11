abcdefg:hello world:sldhsldhl  ==> hello world
```
with cte(text) as
( 
	select 'abcdefg:hello world:sldhsldhl'
	union select ''
	union select '::'
	union select 'abcdefg:hello world'  --this will return null! add case statement if you want to extract hello world for this. (see second example)
	union select 'abcdefg:hello world:'
)
select 
substring(text,
	len(substring(text,0,INSTR(text, ':')))+1, --start
	--below looks for next location of delim and counts num characters to extract
	len(substring(text,0,INSTR(text, ':')))+1 + 
	instr(
			substring(text,len(substring(text,0,INSTR(text, ':')))+1) --text starting from previous delim to end
		,':') --look for next delim
)
,text
from cte
order by 1
```
```
with cte(text) as
( 
	select 'abcdefg:hello world:sldhsldhl'
	union select ''
	union select '::'
	union select 'abcdefg:hello world'
	union select 'abcdefg:hello world:'
)
select 
substring(text,
	len(substring(text,0,INSTR(text, ':')))+1, --start
	--below looks for next location of delim and counts num characters to extract
	len(substring(text,0,INSTR(text, ':')))+1 + 
	case when instr(
			substring(text,len(substring(text,0,INSTR(text, ':')))+1) --text starting from previous delim to end
		,':') = -1 then len(text) else instr(
			substring(text,len(substring(text,0,INSTR(text, ':')))+1) --text starting from previous delim to end
		,':') end --look for next delim = 
)
,text
from cte
order by 1
```
