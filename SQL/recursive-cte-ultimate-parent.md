If you have a table (here called account) with columns id, parentid, where parentid points at the id column in the same table, then here is how you can get the ultimate-parent (aka top-level parent)

```sql
with recursive hieararchy_cte(id,parentid,level) as
(
    select a.id,a.parentid, 1 as level
    from account a
    union all
    select current_child.id, parent.parentid, level+1 as level
    from account parent
    join hieararchy_cte current_child on parent.id = current_child.parentid
    where level < 20    -- prevent infinite recursion
    and parent.parentid is not null -- dont want to look at ultimate parent, as its parent will be null
)
-- select * from parent_account_cte;
,CTE_UltimateParent as
(
    select cte.*, row_number() over ( partition by cte.id order by cte.level desc) RN
    from hieararchy_cte cte
)
select cte.id, child.name as name, cte.parentid, parent.name, cte.level, cte.rn
from
    CTE_UltimateParent cte
    left join account parent on parent.id = cte.parentid
    left join account child on child.id = cte.id
where RN = 1
order by level desc
;
```
