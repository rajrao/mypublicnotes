If you have a table (here called account) with columns id, parentid, where parentid points at the id column in the same table, then here is how you can get the ultimate-parent (aka top-level parent)

**Modified solution using ChatGPT help** (prompt: I have an account table with ID and ParentId. ParentId references Id.
Can you write a query that returns the ultimate parent for all accounts in account table)

This is the best solution! Cant believe I used to use a window function to do this!
```sql
WITH RECURSIVE cte(id,parentid,ultimate_parent_id, level) AS (
  SELECT id, parentid, id as ultimate_parent_id, 1 as level
  FROM account
  where parentid is null
  UNION ALL
  SELECT a.id, a.parentid, cte.ultimate_parent_id, level + 1 as level
  FROM account a
  JOIN cte ON cte.id = a.parentid
)
SELECT * FROM cte
```

**Modified Cleaner Solution**
```sql
with recursive hieararchy_cte(orig_id,id,parentid,level) as
(
    select a.id orig_id,a.id, a.parentid, 1 as level
    from account a
    union all
    -- note the use of current_child.id, this carries the child-id forward, so that row-number will work
    -- only needed if you need the ultimate parent
    select current_child.orig_id,parent.id, parent.parentid, level+1 as level
	from
    account parent
    join hieararchy_cte current_child on parent.id = current_child.parentid
    where level < 20    -- prevent infinite recursion
)
-- select * from hieararchy_cte; -- uncomment this line if you want to see the complete hierarchy from child to parent
,CTE_UltimateParent as
(
    select cte.*, row_number() over ( partition by cte.orig_id order by cte.level desc) RN
    from hieararchy_cte cte
    where parentid is not null
)
select cte.orig_id, child.name as name, cte.parentid, parent.name, cte.level, cte.rn
from
    CTE_UltimateParent cte
    left join account parent on parent.id = cte.parentid
    left join account child on child.id = cte.orig_id
where RN = 1
order by level desc
;
```


**My Original Solution**
```sql
with recursive hieararchy_cte(id,parentid,level) as
(
    select a.id,a.parentid, 1 as level
    from account a
    union all
    -- note the use of current_child.id, this carries the child-id forward, so that row-number will work
    select current_child.id, parent.parentid, level+1 as level
    from account parent
    join hieararchy_cte current_child on parent.id = current_child.parentid
    where level < 20    -- prevent infinite recursion
    and parent.parentid is not null -- dont want to look at ultimate parent, as its parent will be null
)
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
