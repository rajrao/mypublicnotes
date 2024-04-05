-- this query finds missing dates, where the expectation is that there should be dates for all days in a table

WITH cte_dates AS (
	SELECT activitydate,
		count(1) num_records
	FROM source_table
	where activitydate >= cast('2023-04-01' as date)
	group by activitydate
	order by activitydate
),
cte_missing_dates as (
	select activitydate,
		lag(activitydate, 1) over (order by activitydate) prev_date,
		(
			date_diff('day',lag(activitydate, 1) over (order by activitydate),activitydate) - 1
		) num_days_missing,
		num_records
	from cte_dates
)
select * from cte_missing_dates where num_days_missing >= 1;
	
