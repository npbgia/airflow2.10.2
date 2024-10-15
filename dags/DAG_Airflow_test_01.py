from datetime import date,datetime, timedelta
import datetime

from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.empty import EmptyOperator
from airflow.decorators import task_group

args = {
    'owner': 'de@airflow',
    'start_date': datetime.datetime(2023,1,30),
    'provide_context': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

dag = DAG(
        dag_id='DAG_Airflow__Ni_Hao_Ma',        
        catchup=False,
        #concurrency=4,
        schedule_interval='35 0 * * *',
        default_args=args,
        tags=["airflow","tren_tay_airflow2.10.2"]
        )


today = date.today()

init_task = DummyOperator(task_id='init_task', retries=3, dag=dag)
dummy_task_01 = DummyOperator(task_id='dummy_task_01', retries=3, dag=dag)
dummy_task_02 = DummyOperator(task_id='dummy_task_02', retries=3, dag=dag)


task_ni_hao_ma = BashOperator(task_id='ni_hao_ma',
                            bash_command="echo 'Ni Hao Ma?' Airflow 2.10.2 {_date}".format(_date=today),
                            dag=dag
                            )

task_wo_hen_hao = BashOperator(task_id='wo_hen_hao',
                            bash_command="echo 'Wo Hen Hao!' Airflow 2.10.2 {_date}".format(_date=today),
                            dag=dag
                            )

# Start task group definition
@task_group(group_id='task_group_01', dag=dag)
def tg1():
    dummy_task_03 = DummyOperator(task_id='dummy_task_03', retries=3, dag=dag)
    dummy_task_04 = DummyOperator(task_id='dummy_task_04', retries=3, dag=dag)
    dummy_task_05 = DummyOperator(task_id='dummy_task_05', retries=3, dag=dag)

    [dummy_task_03,dummy_task_04] >> dummy_task_05

init_task >> task_ni_hao_ma >> task_wo_hen_hao >> [dummy_task_01,dummy_task_02] >> tg1()

