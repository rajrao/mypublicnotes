from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.operators.python import PythonOperator, ShortCircuitOperator
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
    event_info = {"event": {"exec_name": "just_a_test"}}
  
    test_py_operator_returning_value = PythonOperator(
            task_id=f"aTestPyOperator",
            op_kwargs=event_info,
            python_callable=lambda **kwargs: f"rexec_id_{kwargs['event']['exec_name']}_12345",
            )

    sensor = S3KeySensor(
        task_id='check_s3_for_file_in_s3',
        bucket_name='hvbidev-dl-l1',
        bucket_key="{{ ti.xcom_pull(task_ids='aTestPyOperator') }}/",
        timeout=18*60*60,
        poke_interval=120,
        mode="reschedule"
    )
    
    t2 = BashOperator(task_id="task2", bash_command="echo task 2")
    
    t1 >> test_py_operator_returning_value >> sensor >> t2


