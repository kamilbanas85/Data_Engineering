#%% CONNECT TO SQL Server DATABASE
import pyodbc
import sqlalchemy as sa
import urllib


##########################################
##########################################
##########################################
##########################################
### standard - with pyodbc.connect

##############################
### connect to DB

server = 'dashboard-dbserver01.database.windows.net'
database = 'baza01'
username = 'kamilbanas85'
password = 'pasword'
driver= '{ODBC Driver 17 for SQL Server}'


### 'trusted-azure' - inisde web-app with identiy:
with pyodbc.connect('Driver='+driver +
                     ';Server='+server + 
                     ";PORT=1443;Database="+ database +
                     ";Authentication=ActiveDirectoryMsi") as conn:

### 'trusted':
with pyodbc.connect('Driver='+driver +
                    ';Server='+server + 
                    ";PORT=1443;Database="+ database +
                    ";Trusted_Connection=yes") as conn:
                
### 'password'
with pyodbc.connect('DRIVER='+driver+
                    ';SERVER=tcp:'+server+
                    ';PORT=1433;DATABASE='+database+
                    ';UID='+username+
                    ';PWD='+ password) as conn:
 
### AZURE - mfa - interactive - window o login shows:
### 
### !!! You need to install adalsql.dll first. Remember to choose ENU\x86\adalsql.msi.
### !!! https://www.microsoft.com/en-us/download/confirmation.aspx?id=48742
### 

Authentication='ActiveDirectoryInteractive'

with pyodbc.connect('DRIVER='+driver+
                    ';SERVER=tcp:'+server+
                    ';PORT=1433;DATABASE='+database+
                    ';UID='+username+
                    ';AUTHENTICATION='+Authentication) as conn:
  
### AZURE - mfa - to prevent showing window to login:

Authentication='ActiveDirectoryPassword'

with pyodbc.connect('DRIVER='+driver+
                    ';SERVER=tcp:'+server+
                    ';PORT=1433;DATABASE='+database+
                    ';UID='+username+
                    ';PWD='+ password+
                    ';AUTHENTICATION='+Authentication) as conn:

    
##############################
####### then inside connection  read data to pandas  DataFrame  
with pyodbc.connect('DRIVER='+driver+
                    ';SERVER=tcp:'+server+
                    ';PORT=1433;DATABASE='+database+
                    ';UID='+username+
                    ';PWD='+ password) as conn:
    
    data = pd.read_sql_query( Sql_query,  conn)


##############################
####### or inside connection make query  
with pyodbc.connect('DRIVER='+driver+
                    ';SERVER=tcp:'+server+
                    ';PORT=1433;DATABASE='+database+
                    ';UID='+username+
                    ';PWD='+ password) as conn:

    with conn.cursor() as cursor:
        cursor.execute( Sql_query )
        cursor.commit()


############################################################################################################
### With function

import numpy as np
import pandas as pd
import pyodbc

def get_connection(ServerName: str, DBname: str, Driver: str,\
                   Authenication: str = 'trusted',\
                   UserName: str = 'UserName', Password: str= 'Password') -> str:
    
    # Authenication =  'trusted'  or  'password'  or  'trusted-azure'
    
    BaiscConnStr = 'Driver=' + Driver +\
                   ';Server=' + ServerName +\
                   ';PORT=1443' +\
                   ';Database=' + DBname                
          
    if Authenication =='trusted':
          ConnStr = BaiscConnStr +\
                     ";Trusted_Connection=yes"

    elif  Authenication == 'trusted-azure':
          ConnStr = BaiscConnStr +\
                     ";Authentication=ActiveDirectoryMsi"

    elif  Authenication == 'password':
          ConnStr = BaiscConnStr +\
                     ";UID=" + UserName +\
                     ";PWD=" + Password

    
    conn = pyodbc.connect( ConnStr )

    return conn
  
### then

ServerName = 'ServerName.database.windows.net'
DBname = 'DBname'
Driver= '{ODBC Driver 17 for SQL Server}'
UserName = 'UserName'
Password = 'XXX'
    
# Authenication =  'trusted'  or  'password'  or  'trusted-azure'
conn = get_connection( ServerName, DBname, Driver, Authenication, UserName, Password)
    
with conn:
  data = pd.read_sql_query( querySQL,  conn)   
        
############################################################################################################
############################################################################################################
############################################################################################################
### Sql alchemy

### password
params = urllib.parse.quote_plus('DRIVER='+driver+
                                 ';SERVER=tcp:'+server+
                                 ';PORT=1433;DATABASE='+database+
                                 ';UID='+username+
                                 ';PWD='+ password)

### trusted connection 
params = urllib.parse.quote_plus('DRIVER='+driver+
                                 ';SERVER=tcp:'+server+
                                 ';PORT=1433;DATABASE='+database+
                                 ';TRUSTED_CONNECTION=yes')


engine = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params),
                          fast_executemany=True,\
                          connect_args={'connect_timeout': 10},\
                          echo=False)


###########################
### exectue query

with engine.connect() as con:
    con.execute( sql_query )

###############################################################################################################################
###############################################################################################################################
### write dataframe to sql table
###############################################################################################################################
###############################################################################################################################

### with pyodbc

import pyodbc

server = 'serverName'
database = 'dbName'
driver= '{ODBC Driver 17 for SQL Server}'


# replace np.nan with None - ro prevent error from sql
df = df.astype(object).where(df.notnull(), None)


# form SQL statement
SQL_table_name = '[LNG].[LNGliquefactionCapacity_Reuters] '
ColumnsNameList = ['['+ name + ']' for name in df.columns]
values = '('+', '.join(['?']*len(ColumnsNameList))+')'    
sqlQuery = f"INSERT INTO {SQL_table_name} ({', '.join(ColumnsNameList)}) VALUES {values}"

# extract values from DataFrame into list of tuples
DFasListOfTuple = [tuple(x) for x in df.values]

with pyodbc.connect('Driver='+driver +
                    ';Server='+server + 
                    ";PORT=1443;Database="+ database +
                    ";Trusted_Connection=yes") as conn:

    with conn.cursor() as cursor:
        cursor.fast_executemany = True
        cursor.executemany(sqlQuery, DFasListOfTuple)

###########################################################
### second method - with pyodbc

ColumnsNameList = ['['+ name + ']' for name in LNG_production_capacity_AfterReplacement.columns]
ColumnsNameListWithRow =  ['row["'+ name + '"]' for name in LNG_production_capacity_AfterReplacement.columns]

sqlQuery =  f"""INSERT INTO [LNG].[LNGliquefactionCapacity_Reuters] 
                           ({', '.join(ColumnsNameList)}) values({', '.join(['?' for x in ColumnsNameList]) })"""

with pyodbc.connect('Driver='+driver +
                    ';Server='+server + 
                    ";PORT=1443;Database="+ database +
                    ";Trusted_Connection=yes") as conn:

    with conn.cursor() as cursor:
        for index, row in df.iterrows():
            cursor.execute( sqlQuery, row['col_1'], row['col_2'], ..., row['col_n'] )
            cursor.commit()        

###########################################################  
### with SQLAlchemy
# .to_sql only work with sqlAlchemy connection


df.reset_index()\
    .assign(Date = lambda x: x['Date'].astype('str'))\
    .to_sql(con=engine, schema="dbo", name="tablename",\
            if_exists="append",\
            index=False,\
            chunksize=1000)
        
# append - pevent to delate datatypes, so to load all data frame it requires delate all rows:


        
################################################################
###############################################################   
# to preserve primery key and data types

sql_query1 = '''
DROP TABLE [dbo].[tableNameInSql]
CREATE TABLE tableNameInSql (
    [Date]     VARCHAR(30)  NOT NULL PRIMARY KEY,
    Demand   Decimal(8,1) )
'''
# or
table_name = 'tableNameInSql'

sql_query2 = f'''
TRUNCATE TABLE {table_name}
'''

with engine.connect() as con:
    con.execute(sql_query1)
