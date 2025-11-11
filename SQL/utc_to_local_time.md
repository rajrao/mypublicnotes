Convert timestamp provided in UTC to local time.
Also extracts the hour in local time zone.

Tested in Denodo. Works with day light savings times

```sql
WITH examples AS (
  SELECT 'America/New_York' AS tz, TO_TIMESTAMPTZ('yyyy-MM-dd HH:mm:ss','2025-11-01 18:00:00', 'utc') AS dt_utc UNION ALL
  SELECT 'America/New_York' AS tz, TO_TIMESTAMPTZ('yyyy-MM-dd HH:mm:ss','2025-11-11 18:00:00', 'utc') AS dt_utc UNION ALL
  SELECT 'America/Denver' AS tz, TO_TIMESTAMPTZ('yyyy-MM-dd HH:mm:ss','2025-11-01 18:00:00', 'utc') AS dt_utc UNION ALL
  SELECT 'America/Denver' AS tz, TO_TIMESTAMPTZ('yyyy-MM-dd HH:mm:ss','2025-11-11 18:00:00', 'utc') AS dt_utc UNION ALL
  SELECT 'America/Los_Angeles' AS tz, TO_TIMESTAMPTZ('yyyy-MM-dd HH:mm:ss','2025-11-01 18:00:00', 'utc') AS dt_utc UNION ALL
  SELECT 'America/Los_Angeles' AS tz, TO_TIMESTAMPTZ('yyyy-MM-dd HH:mm:ss','2025-11-11 18:00:00', 'utc') AS dt_utc
)
SELECT
  tz,
  dt_utc,
  CONVERT_TIMEZONE(tz, dt_utc) local_time,
  EXTRACT(HOUR FROM CONVERT_TIMEZONE(tz, dt_utc)) AS hour_local_time
FROM examples
order by tz, dt_utc;
```
