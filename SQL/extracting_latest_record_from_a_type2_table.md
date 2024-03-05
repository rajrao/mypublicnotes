


```sql
-- example from: https://docs.aws.amazon.com/marketplace/latest/userguide/data-feed-full-examples.html
with products_with_uni_temporal_data as (
      select
       *
      from
      (
        select
         *,
         ROW_NUMBER() OVER (PARTITION BY product_id, valid_from 
             ORDER BY from_iso8601_timestamp(update_date) desc) 
             as row_num
        from
         productfeed_v1
      )
      where
        -- A product_id can appear multiple times with the same 
        -- valid_from date but with a different update_date column,
        -- making it effectively bi-temporal. By only taking the most
        -- recent tuple, we are converting to a uni-temporal model.
        row_num = 1
    ),

    -- Gets the latest revision of a product
    -- A product can have multiple revisions where some of the 
    -- columns, like the title, can change.
    -- For the purpose of the disbursement report, we want 
    -- to get the latest revision of a product
    products_with_latest_version as (
     select
      *
     from
     (
      select
       *,
       ROW_NUMBER() OVER (PARTITION BY product_id 
           ORDER BY from_iso8601_timestamp(valid_from) desc) 
           as row_num_latest_version
      from
       products_with_uni_temporal_data
     )
     where
      row_num_latest_version = 1
   )
select * from products_with_latest_version
```
