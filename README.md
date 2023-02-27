<h1 align="center">ETL Pipeline with Airflow, Python, PostgreSQL and Docker</h1>

<p align="center">
  <a href="#about">About</a> •
  <a href="#scenario">Scenario</a> •
  <a href="#base-concepts">Base Concepts</a> •
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#set-up">Set-up</a> •
  <a href="#installation">Installation</a> •
  <a href="#airflow-interface">Airflow Interface</a> •
  <a href="#pipeline-task-by-task">Pipeline Task by Task</a> •
  <a href="#shut-down-and-restart-airflow">Shut Down and Restart Airflow</a> 
</p>

## About

This is a small project showcasing how to build an ETL workload using Airflow, Python and PostgreSQL with Docker being used for deployment.

A file is pulled from local storage(easily replaceable with an AWS S3 bucket if need be), transformed using Python and loaded into a PostgreSQL database. 

The project is built in Python and it has 2 main parts:
  1. The Airflow DAG file, [**dagRun.py**](https://github.com/DEMaestro1/AirflowOrchPython/blob/main/dags/dagRun.py), which orchestrates the data pipeline tasks.
  2. The python data transformation/processing script which uses Pandas, located in [**pythonProcess.py**](https://github.com/DEMaestro1/AirflowOrchPython/blob/main/tasks/pythonProcess.py)

## Scenario

The poverty data which can be found on https://data.worldbank.org/topic/poverty, contains poverty data for each county, for every year there has been a survey in said countries.

We are only looking for countries with a specific poverty level in the year of 2019. A quite simple scenario, more advanced transformations can be used for various other purposes.

## Base concepts

 - [Data Engineering](https://realpython.com/python-data-engineer/)
 - [ETL (Extract, Transform, Load)](https://en.wikipedia.org/wiki/Extract,_transform,_load)
 - [Pipeline](https://en.wikipedia.org/wiki/Pipeline_(computing))
 - [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html) ([wikipedia page](https://en.wikipedia.org/wiki/Apache_Airflow))
 - [Airflow DAG](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#dags)
 - [PostgreSQL](https://www.postgresql.org/)

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## Set-up

Download / pull the repo to your desired location.

You can change the user and passwords in docker-compose file if need be, just make sure to change the configuration.conf file that is being used. Usually instead of user and pass being stored in such a way, projects use AWS Secrets or Azure Key Vault.

## Installation

Start the installation with:

    docker-compose up -d

This command will pull and create Docker images and containers for Airflow as well as another PostgreSQL container to store poverty data.
This is done according to the instructions in the [docker-compose.yml](https://github.com/DEMaestro1/AirflowOrchPython/blob/main/docker-compose.yaml) file:

After everything has been installed, you can check the status of your containers (if they are healthy) with:

    docker ps

**Note**: it might take up to 30 seconds for the containers to have the **healthy** flag after starting.

## Airflow Interface

You can now access the Airflow web interface by going to http://localhost:8080/. If you have not changed them in the docker-compose.yml file, the default user is **airflow** and password is **airflow**:

The defaults can be changed inside the docker-compose file.

After signing in, the Airflow home page is the DAGs list page. Here you will see all your DAGs and the Airflow example DAGs, sorted alphabetically. 

Any DAG python script saved in the directory [**dags/**](https://github.com/DEMaestro1/AirflowOrchPython/tree/main/dags), will show up on the DAGs page.

## Pipeline Task by Task

#### Task `processData`

The csv contains unnecessary data for this case, so it needs to be  filtered out. We are using a PythonOperator in this case.

This runs the cleanFilterData function inside the pythonProcess.py file under the tasks folder which selects a subset of the data that is required and filters it based on some condition.

The data is then written to the files folder as a parquet, ready to be loaded into a database.

#### Task `loadDB`

A BashOperator is used to call loadData function inside the pythonProcess.py file. This is just used to showcase an alternative Operator that can be used instead if a certain use case requires it.

The processed data is loaded into PostgreSQL instance running inside the container postgres-db, please be aware that a separate container named only postgres is being used by airflow and thus was not used for storing the processed data.

However if need be data can be stored on the same container but it is generally considered good practice to have it another container.

#### Task `validateDBData`

The function validateData is called from the pythonProcess.py file.

It is used to validate the data, this is a simple check to see if the data has been successfully loaded, there are plenty of checks that can be done as required.

You can find a list of common data validation checks as well as information about why its important to have in your projects, [**here**](https://www.tibco.com/reference-center/what-is-data-validation).

## Shut Down and Restart Airflow

For any changes made in the configuration files to be applied, you will have to rebuild the Airflow images with the command:

    docker-compose build

Recreate all the containers with:

    docker-compose up -d

## License
You can check out the full license [here](https://github.com/DEMaestro1/AirflowOrchPython/blob/main/LICENSE)

This project is licensed under the terms of the **GPL** license.
