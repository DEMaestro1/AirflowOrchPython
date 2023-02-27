import json
import pandas as pd
import os
import datetime
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from tasks.pythonProcess import cleanFilterData, validateData
# Defining parameters to be passed to Operators - Functions
rawFileLocation = '/opt/airflow/files/PovertyData.csv'
sinkLocation = '/opt/airflow/files'
fileName = 'PovertyData.csv'
s3Bucket = 'readOnlyBucket'


# DAG arguments
defaultArgs = {
    'owner': 'New_O',
    'start_date': datetime.datetime(2023, 1, 1),
    'retries': 0,
    'retry_delay': datetime.timedelta(seconds=30),
    'catchup': False
}

# DAG definition
with DAG('load_csv_data',
         schedule_interval ='@daily',
         default_args = defaultArgs,
         catchup = False) as dag:
    
    # Calling function to clean data by using a PythonOperator
    processData = PythonOperator(
        task_id = 'processData',
        python_callable = cleanFilterData,
        op_kwargs = {'rawLocation': rawFileLocation, 
                    'stageLocation': sinkLocation}
    )
    
    # Calling function to load data by using a BashOperator as an alternative
    loadDB = BashOperator(
        task_id = 'loadDB',
        bash_command = f"""cd /opt/airflow/dags/tasks; python -c'import pythonProcess;pythonProcess.loadData("{sinkLocation}")'"""
    )

   # Data Validation
    validateDBData = PythonOperator(
        task_id = 'validateDBData',
        python_callable = validateData,
        op_kwargs = {'stageLocation': sinkLocation}
    )
    # set tasks relations (the order the tasks are executed)
    processData >> loadDB >> validateDBData
