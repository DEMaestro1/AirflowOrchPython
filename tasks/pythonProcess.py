import configparser
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

#parsing configuration file in same directory for postgres details, other DBs can be used if needed
parser = configparser.ConfigParser()
p = Path(__file__).with_name('configuration.conf')
parser.read(p.absolute())
username = parser.get('postgres_config', 'postgres_username')
password = parser.get('postgres_config', 'postgres_password')
host = parser.get('postgres_config', 'postgres_hostname')
port = parser.get('postgres_config', 'postgres_port')
dbName = parser.get('postgres_config', 'postgres_db')
sqlDb = 'postgresql'

# create a dataframe using the data in the csv
def cleanFilterData(rawLocation, stageLocation):
    df = pd.read_csv(rawLocation,
                    skiprows = 4,
                    header='infer')
    
    #selecting the subset of a dataframe
    subDf = df[['Country Name', 'Country Code', '2019']]
    
    #Filtering data for the required rows/countries
    filteredDf = subDf[subDf['2019'] > 0.9]
    
    #writing to a parquet
    filteredDf.to_parquet(stageLocation+'/processedData.parquet', index=False)
    
#loading data into Postgres, using sqlalchemy for ease of use but usual preference is psycopg2 or a combination of the two
def loadData(stageLocation):
    pDf = pd.read_parquet(stageLocation+'/processedData.parquet')               
    engine = create_engine(f'{sqlDb}://{username}:{password}@{host}:{port}/{dbName}')
    pDf.to_sql('poverty_demographics',
                engine,
                if_exists='replace',
                index=False)

#Simple count check to validate if data was successfully pushed to poverty_demographics table, for validation you can also use tools like dbt and Great Expectations
def validateData(stageLocation):
    engine = create_engine(f'{sqlDb}://{username}:{password}@{host}:{port}/{dbName}')
    df = pd.read_sql('Select * from poverty_demographics', engine)
    if df.empty:
        raise ValueError('File not parsed completely/correctly')

