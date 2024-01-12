Airflow SLAs at the task level are cummulative. The best way to think of the SLA is that it uses the "execution_date" on the task as its T-0. The execution_date on the task is the **"Data interval start"** on the dag. From "Data Pipelines with Apache Airflow", SLAs are described as:
```    
SLAs function somewhat counter-intuitive. While you might expect it to function as a maximum runtime for the given task,
it functions as the maximum time difference between the scheduled start of the DAG run and completion of the task.
```

On the "List SLA Misses" page, the "Logical Date" is the start time for the dag. The "Timestamp" column represents when the SLA was captured. SLAs are captured as they occur, but the "sla_miss_callback" is only called at the end of the task completion.

SLAs are captured on both scheduled and manually run DAGs. But this may end up acting in a way that you dont expect. As the SLA is calculated based on "Data interval start", a manually run DAG will use the "Data Interval Start" based on the last time the schedule should have run. In this case, the SLA may be breached, if your SLAs were setup with very tight tolerances.
But SLAs are not triggered on manually run **Tasks**.

1. Pt_1.2 will fail as it has a SLA of 20 and it runs for 25 seconds
2. PT_1.1 will not fail SLA as it has an sla of 20, but runs for only 10 seconds
3. PT_2 will fail SLA, as even though it runs only for 20 seconds, its sla of 25 will be breached, because pt_1.2 takes 25 seconds to run and Pt_2 runs only after that.
4. PT_3.1 will pass SLA as it has an SLA of 65 and it should complete after (25+25+15=60) seconds.
5. PT_3.2 will fail SLA (sometimes) as it has an SLA of 60 and although it should complete in 60 seconds, it may not always do so
6. PT_3.4 is similar to PT_3.2 but will always pass, as it will complete at T+15 and its SLA is 60 seconds.
7. PT_3.5 has a short SLA but long duration. Although the task taskes 45 seconds to complete, the SLA is captured almost immediately after the SLA has expired.

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/e417effe-47a0-4a97-9861-51571dbcbf66)

**SLA misses captured for the above DAG:**
![image](https://github.com/rajrao/mypublicnotes/assets/1643325/806e22b9-170c-47b2-951d-e5638959c767)

**Final Thoughts**

Given all the info above, use SLA to capture and notify when a DAG/Task has run for an abnormally long time. So if a task runs typically for 15 minutes, dont have an SLA of 20 minutes, instead use an SLA of 30 minutes or even 45 minutes. This way, a manually run DAG will not cause SLA misses.

**More Info:**

[Airflow SLAS](https://airflow.apache.org/docs/apache-airflow/2.6.3/core-concepts/tasks.html#slas)

SLAs not working? Check [check_slas configuration](https://airflow.apache.org/docs/apache-airflow/2.6.3/configurations-ref.html#check-slas)



**Code**
```python
import time
from datetime import datetime, timedelta, date
import logging
import os

from airflow import models
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


_logger = logging.getLogger(__name__)
# _logger.addHandler(logging.NullHandler())
_logger.setLevel(logging.INFO)

WORKFLOW_DAG_ID = os.path.basename(__file__).replace(".py", "")

def task_acting_like_its_doing_work(**kwargs):
    _logger.info(f"task_acting_like_its_doing_work for {kwargs['sleep_duration']} seconds...")
    time.sleep(kwargs['sleep_duration'])
    _logger.info("task_acting_like_its_doing_work is complete")


# Default settings applied to all tasks
default_args = {
    "owner": "rrao",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": "raj.rao@hitachivantara.com",
    "email_on_retry": False,
    "sla": timedelta(minutes=30),
}

# SLA does not seem to work with schedule=None
with models.DAG(
    dag_id=WORKFLOW_DAG_ID,
    start_date=datetime(2024, 1, 1),
    max_active_runs=1,
    schedule="*/15 * * * *", 
    default_args=default_args,
    catchup=False,
) as dag:
    task_start = DummyOperator(task_id="start")
    
    # the following 2 tasks run in parallel.
    # only py_task_2 will fail SLA every time.
    py_task_1 = PythonOperator(task_id="pt_1.1_sla_20_duration_10", 
        python_callable=task_acting_like_its_doing_work,
        op_kwargs={'sleep_duration':10},
        sla=timedelta(seconds=20),
        )
    py_task_2 = PythonOperator(task_id="pt_1.2_sla_20_duration_25", 
        python_callable=task_acting_like_its_doing_work,
        op_kwargs={'sleep_duration':25},
        sla=timedelta(seconds=20),
        )
    
    # this next task runs after the above 2.
    # as elapsed time would be 25 seconds + 20 for this task
    # this one will also fail SLA every time
    py_task_3 = PythonOperator(task_id="pt_2_sla_25_duration_20", 
        python_callable=task_acting_like_its_doing_work,
        op_kwargs={'sleep_duration':20},
        sla=timedelta(seconds=25),
        )
    
    # the next 2 tasks run in parallel
    # task 4 should pass SLA (45 + 15) < 65
    # task 5 might not pass SLA (45 + 15) <= 60. Because depending on time of run
    # the SLA may or not breach
    py_task_4 = PythonOperator(task_id="pt_3.1_sla_65_duration_15", 
        python_callable=task_acting_like_its_doing_work,
        op_kwargs={'sleep_duration':15},
        sla=timedelta(seconds=65),
        )

    py_task_5 = PythonOperator(task_id="pt_3.2_sla_60_duration_15", 
        python_callable=task_acting_like_its_doing_work,
        op_kwargs={'sleep_duration':15},
        sla=timedelta(seconds=60),
        )
    
    # this one is exactly like py_task5 which might fail SLA, but this one wont,
    # as it runs right after start node.
    py_task_6 = PythonOperator(task_id="pt_3.4_standalone_sla_60_duration_15", 
        python_callable=task_acting_like_its_doing_work,
        op_kwargs={'sleep_duration':15},
        sla=timedelta(seconds=60),
        )
    
    py_task_7 = PythonOperator(task_id="pt_3.5_standalone_sla_5_duration_45", 
        python_callable=task_acting_like_its_doing_work,
        op_kwargs={'sleep_duration':45},
        sla=timedelta(seconds=5),
        )
    
    task_end = DummyOperator(task_id="end")

    task_start >> [py_task_1,py_task_2] >> py_task_3 >> [py_task_4,py_task_5] >> task_end
    task_start >> [py_task_6,py_task_7] >> task_end
```

