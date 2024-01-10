import os
from datetime import timedelta
import logging
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from pprint import pprint
import inspect

DAG_ID = os.path.basename(__file__).replace(".py", "")
WORKFLOW_SCHEDULE_INTERVAL = None

DEFAULT_ARGS = {
    "owner": "garystafford",
    "depends_on_past": False,
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
}
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

def print_airflow_cfg():
    with open(f"{os.getenv('AIRFLOW_HOME')}/airflow.cfg", "r") as airflow_cfg:
        file_contents = airflow_cfg.read()
        _logger.info(f"\n{file_contents}")


def print_env_vars():
    keys = str(os.environ.keys()).replace("', '", "'|'").split("|")
    keys.sort()
    for key in keys:
        _logger.info(key)


def print_conf_from_context_vars_callable(**kwargs):
    conf = kwargs['conf']
    _logger.info(json.dumps(conf,indent=3))
    #pprint(vars(conf))


def print_conf_from_context_dir_callable(**kwargs):
    conf = kwargs['conf']
    for attr in dir(conf):
        _logger.info(f"{attr}: {getattr(conf, attr)}")


def print_conf_from_context_inspect_callable(**kwargs):
    conf = kwargs['conf']
    props = inspect.getmembers(conf, lambda a: not (inspect.isroutine(a)))
    for prop in props:
        _logger.info(prop)


with DAG(
    dag_id=DAG_ID,
    schedule_interval=WORKFLOW_SCHEDULE_INTERVAL,
    default_args=DEFAULT_ARGS,
    description="Print diagnostic data to logs",
    dagrun_timeout=timedelta(hours=2),
    start_date=days_ago(1),
    catchup=False,
    tags=["utilities", "python", "bash"],
) as dag:
    get_airflow_cfg_operator = PythonOperator(
        task_id="get_airflow_cfg_task", python_callable=print_airflow_cfg
    )
    get_env_vars_operator = PythonOperator(
        task_id="get_env_vars_task", python_callable=print_env_vars
    )
    """
    [2023-06-15, 17:00:56 UTC] {{subprocess.py:74}} INFO - Running command: \
        ['bash', '-c', 'python3 --version']
    [2023-06-15, 17:00:56 UTC] {{subprocess.py:85}} INFO - Output:
    [2023-06-15, 17:00:56 UTC] {{subprocess.py:89}} INFO - Python 3.7.16
    [2023-06-15, 17:00:56 UTC] {{subprocess.py:93}} INFO - Command exited with return code 0
    """
    list_python_packages_operator = BashOperator(
       task_id="list_python_packages", bash_command="python3 -m pip list"
    # list_python_packages_operator = BashOperator(
    #     task_id="list_python_packages", bash_command="python3 --version"
    )
    print_conf_from_context_vars_operator = PythonOperator(
        task_id="print_conf_from_context_vars",
        python_callable=print_conf_from_context_vars_callable,
        provide_context=True
        )
    print_conf_from_context_dir_operator = PythonOperator(
        task_id="print_conf_from_context_dir",
        python_callable=print_conf_from_context_dir_callable,
        provide_context=True
        )
    print_conf_from_context_inspect__operator = PythonOperator(
        task_id="print_conf_from_context_inspect",
        python_callable=print_conf_from_context_inspect_callable,
        provide_context=True
        )
