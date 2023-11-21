########################################################################
########################################################################
########################################################################
### SECRET SCOPE

#   In Databrics there are two types of secrete scopes:
#   -	Azure Key Valut – backed scopes   <-  it takes all sectrets from key-valut
#   -	Databrics-backed scopes 


# display all methods based on sectrets: 
     dbutils.sectrets.help()

# list all secrets scopes:
     dbutils.secrets.listScopes()

# list all sectretes inside sectrete scope
     dbutils.secrets.list("sectrete_scope_name")  

# get value of sectrete
     dbutils.secrets.get(‘scope_name’,’sectret_name’)


########################################################################
### Create	Azure Key Valut – backed scopes - using UI

'''
go to URL:       https://<databrics-instance>#secrets/createScope

Fill:
  scope name        ->   …..
  Manage Principal  ->   All Users (the best if only 1 person know)
  DNS Name          ->  (Key Valut Recource in Portal -> Properities -> Vault URI)
  Resource ID       ->  (Key Valut Recource in Portal -> Properities -> Resource ID)

'''


########################################################################
########################################################################
########################################################################
### SCRVICE PRINICPAL
'''
# Microsoft Entra ID -> App registration
     -	Add unique name: my-databrics-sp
     -	get 'Service Principal ID'   from"       ‘Application (client) ID’                      
     -	get  'Service Principal Secret'   from:   Go to tab ‘Certificates and sectets’ -> Go to tab ‘Client sectrets’ -> new client sectrete
# add 'Service Principal ID' to ADD group with proper permitions (or add add ADD user to SQL)
# save 'Service Principal ID' and 'Service Principal Secret' to key-valut



########################################################################
### get data from SQL based on sevie principale


     @retry(tries=5, delay=60)
     def read_data_from_AZURE_SQL_db_based_on_sp(SQLquery):
       
       jdbcHostname = "dbURL"
       jdbcDatabase = "baName"
       jdbcPort = 1433
       jdbcPrincipalId = dbutils.secrets.get(scope = "scope_name", key="Service Principal ID")
       jdbcPrincipalSecret = dbutils.secrets.get(scope = "scope_name", key="Service Principal Secret")
       
       jdbcUrl = f"jdbc:sqlserver://{jdbcHostname}:{jdbcPort};database={jdbcDatabase}"
       connectionProperties = {
             "driver":"com.microsoft.sqlserver.jdbc.SQLServerDriver",
             "authentication" : "ActiveDirectoryServicePrincipal",
             "user" : jdbcPrincipalId ,
             "password" : jdbcPrincipalSecret
       }
       
       # Conver SQL query to AZURE SQL query
       sqlQueryForAZURE =  f"({SQLquery})  pushdown_query_alias" 
       
       # Read data from DataBase
       DataFromDataBase = spark.read.jdbc(url = jdbcUrl, table =  sqlQueryForAZURE, properties = connectionProperties)
       
       return DataFromDataBase

### oryginal was:

'''
     connectionProperties = {
         "driver":"com.microsoft.sqlserver.jdbc.SQLServerDriver",
         "authentication" : "ActiveDirectoryServicePrincipal",
         "addSecurePrincipalId" : dbr_PrincipalId ,
         "addSecurePrincipalSecret" : dbr_PrincipalSecret
     }
'''


  

  
