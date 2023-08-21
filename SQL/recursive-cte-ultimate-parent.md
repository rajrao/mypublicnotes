If you have a table (here called account) with columns id, parentid, where parentid points at the id column in the same table, then here is how you can get the ultimate-parent (aka top-level parent)

```sql
with recursive parent_account_cte(id,name,parentid,level) as
(
	select a.id, a."name", a.parentid, 1 as level
	from account a
union all
	select parent.id, parent."name", parent.parentid, level + 1 as level
from
		parent_account_cte ca
	join account parent on parent.id = ca.parentid
	where level < 20	-- prevent infinite recursion
),
--cte to find ultimate parent
CTE_UltimateParent as 
(
	select cte.*, row_number() over ( partition by cte.id order by cte.level desc) RN
	from parent_account_cte cte
)
select distinct
	cte.id, cte.name, coalesce(cte.parentid, cte.id) parentid, 	coalesce(parent.name,cte.name) parent_name,	cte.level
from CTE_UltimateParent cte
left join account parent on cte.parentid = parent.id
where RN = 1
-- and coalesce(cte.parentid, cte.id) = 'parent-id-for-searching'
order by level desc
```
