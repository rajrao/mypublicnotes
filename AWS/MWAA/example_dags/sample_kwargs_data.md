Below is what is available within kwargs/context passed to a python operator:

```python
{'conf': <airflow.configuration.AirflowConfigParser object at 0x7f0641e890f0>,
 'conn': None,
 'custom_data': {'data_interval_end': '2024-02-12T21:23:42.357838+00:00',
                 'data_interval_start': '2024-02-12T21:23:42.357838+00:00',
                 'ds': '2024-02-12',
                 'ds_nodash': '20240212',
                 'macros.datetime.utcnow()': '2024-02-12 21:23:52.217716',
                 'prev_data_interval_end_success': 'None',
                 'prev_data_interval_start_success': 'None',
                 'prev_start_date_success': 'None',
                 'run_id': 'manual__2024-02-12T21:23:42.357838+00:00',
                 'ts': '2024-02-12T21:23:42.357838+00:00',
                 'ts_nodash': '20240212T212342',
                 'ts_nodash_with_tz': '20240212T212342.357838+0000'},
 'dag': <DAG: my_task>,
 'dag_run': <DagRun my_task @ 2024-02-12 21:23:42.357838+00:00: manual__2024-02-12T21:23:42.357838+00:00, state:running, queued_at: 2024-02-12 21:23:42.432318+00:00. externally triggered: True>,
 'data_interval_end': DateTime(2024, 2, 12, 21, 23, 42, 357838, tzinfo=Timezone('UTC')),
 'data_interval_start': DateTime(2024, 2, 12, 21, 23, 42, 357838, tzinfo=Timezone('UTC')),
 'ds': '2024-02-12',
 'ds_nodash': '20240212',
 'execution_date': <Proxy at 0x7f0632963b80 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'execution_date', DateTime(2024, 2, 12, 21, 23, 42, 357838, tzinfo=Timezone('UTC')))>,
 'expanded_ti_count': None,
 'inlets': [],
 'logical_date': DateTime(2024, 2, 12, 21, 23, 42, 357838, tzinfo=Timezone('UTC')),
 'macros': <module 'airflow.macros' from '/usr/local/airflow/.local/lib/python3.10/site-packages/airflow/macros/__init__.py'>,
 'next_ds': <Proxy at 0x7f06328eb2c0 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'next_ds', '2024-02-12')>,
 'next_ds_nodash': <Proxy at 0x7f063292b580 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'next_ds_nodash', '20240212')>,
 'next_execution_date': <Proxy at 0x7f063292bc00 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'next_execution_date', DateTime(2024, 2, 12, 21, 23, 42, 357838, tzinfo=Timezone('UTC')))>,
 'outlets': [],
 'params': {},
 'prev_data_interval_end_success': None,
 'prev_data_interval_start_success': None,
 'prev_ds': <Proxy at 0x7f063292af00 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'prev_ds', '2024-02-12')>,
 'prev_ds_nodash': <Proxy at 0x7f063291be80 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'prev_ds_nodash', '20240212')>,
 'prev_execution_date': <Proxy at 0x7f0632781900 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'prev_execution_date', DateTime(2024, 2, 12, 21, 23, 42, 357838, tzinfo=Timezone('UTC')))>,
 'prev_execution_date_success': <Proxy at 0x7f0632781600 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'prev_execution_date_success', None)>,
 'prev_start_date_success': None,
 'run_id': 'manual__2024-02-12T21:23:42.357838+00:00',
 'task': <Task(PythonOperator): python_operator>,
 'task_instance': <TaskInstance: my_task.python_operator manual__2024-02-12T21:23:42.357838+00:00 [running]>,
 'task_instance_key_str': 'my_task__python_operator__20240212',
 'templates_dict': None,
 'test_mode': False,
 'ti': <TaskInstance: my_task.python_operator manual__2024-02-12T21:23:42.357838+00:00 [running]>,
 'tomorrow_ds': <Proxy at 0x7f0632781e80 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'tomorrow_ds', '2024-02-13')>,
 'tomorrow_ds_nodash': <Proxy at 0x7f0632781540 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'tomorrow_ds_nodash', '20240213')>,
 'triggering_dataset_events': <Proxy at 0x7f0632921f40 with factory <function TaskInstance.get_template_context.<locals>.get_triggering_events at 0x7f06328fa680>>,
 'ts': '2024-02-12T21:23:42.357838+00:00',
 'ts_nodash': '20240212T212342',
 'ts_nodash_with_tz': '20240212T212342.357838+0000',
 'var': {'json': None, 'value': None},
 'yesterday_ds': <Proxy at 0x7f0632781c00 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'yesterday_ds', '2024-02-11')>,
 'yesterday_ds_nodash': <Proxy at 0x7f0632781b80 with factory functools.partial(<function lazy_mapping_from_context.<locals>._deprecated_proxy_factory at 0x7f06328fbd00>, 'yesterday_ds_nodash', '20240211')>}

```


Code
```python
"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""
import pprint
from datetime import datetime, timedelta
from textwrap import dedent
import logging

from airflow import DAG

from airflow.operators.python import PythonOperator

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


def python_test_operator(**kwargs):
    _logger.info("--------------------------")
    _logger.info(pprint.pformat(kwargs["custom_data"]))
    _logger.info("--------------------------")
    ds = "{{ ds }}"
    _logger.info("This does not work: ", ds)
    _logger.info("This works: ds: ", kwargs['ds'])
    _logger.info("This works: ds_nodash: ", kwargs['ds_nodash'])
    _logger.info("----------kwargs content----------------")
    _logger.info(pprint.pformat(kwargs))

    _logger.info(f"type of ds: {type(kwargs['ds'])}")

    _logger.info(f"dr.start_date: {type(kwargs['dag_run'].start_date)} "
                 f"{kwargs['dag_run'].start_date}")
    _logger.info(f"ti.start_date: {type(kwargs['task_instance'].start_date)} "
                 f"{kwargs['task_instance'].start_date}")


with DAG(
    'tutorial_af_2_2_2',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
    _op_kwargs = {"custom_data": {
        "data_interval_start": "{{ data_interval_start }}",
        "data_interval_end": "{{ data_interval_end }}",
        "ds": "{{ ds }}",
        "ds_nodash": "{{ ds_nodash }}",
        "ts": "{{ ts }}",
        "ts_nodash_with_tz": "{{ ts_nodash_with_tz }}",
        "ts_nodash": "{{ ts_nodash }}",
        "prev_data_interval_start_success": "{{ prev_data_interval_start_success }}",
        "prev_data_interval_end_success": "{{ prev_data_interval_end_success }}",
        "prev_start_date_success": "{{ prev_start_date_success }}",
        "run_id": "{{ run_id }}",
        "macros.datetime.utcnow()": "{{ macros.datetime.utcnow() }}",
    }}

    t4_python_op = PythonOperator(
            task_id=f"python_operator",
            python_callable=python_test_operator,
            op_kwargs=_op_kwargs,
        )

    t1 >> t4_python_op

```
