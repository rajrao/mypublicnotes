from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator
from airflow.providers.amazon.aws.sensors.athena import AthenaSensor

from datetime import datetime, timedelta
import os

DAG_ID = os.path.basename(__file__).replace(".py", "")
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 1)
}
  
with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    schedule_interval="@once",
    start_date=datetime(2023, 4, 1),
    catchup=False
) as dag:
    t1 = BashOperator(task_id="task1", bash_command="echo task 1")

    read_table1 = AthenaOperator(
        task_id='read_table1',
        query='SELECT current_timestamp',
        database='athena_db_name',
        output_location='s3://aws-athena-query-results-location/'
        )
    
    await_query1 = AthenaSensor(
        task_id='await_query1',
        query_execution_id=read_table1.output,
        mode="poke"  #hold up a worker while it checks
        )
    
    read_table2 = AthenaOperator(
        task_id='read_table2',
        query='SELECT col_name from table_name',
        database='athena_db_name',
        output_location='s3://aws-athena-query-results-location/'
        )
    
    await_query2 = AthenaSensor(
        task_id='await_query2',
        query_execution_id=read_table2.output,
        mode="reschedule" #dont hold up a worker
        )
    
    

    t2 = BashOperator(task_id="task2", bash_command="echo task 2")
    
    t1 >> read_table1 >> await_query1 >> t2
    t1 >> read_table2 >> await_query2 >> t2





