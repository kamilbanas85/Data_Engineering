## Connect to SQL DataBAse (DataBase shoud had JDBC drivers, Azure Databricks has installed the JDBC driver)

### classic
# https://docs.microsoft.com/en-us/azure/databricks/data/data-sources/sql-databases

	jdbcHostname = "<hostname>"
	jdbcDatabase = "employees"
	jdbcPort = 1433
	jdbcUrl = "jdbc:sqlserver://{0}:{1};database={2}".format(jdbcHostname, jdbcPort, jdbcDatabase)
	
	connectionProperties = {
	  "user" : jdbcUsername,
	  "password" : jdbcPassword,
	  "driver" : "com.microsoft.sqlserver.jdbc.SQLServerDriver"
	}
	
	
	#read
	pushdown_query = "(select * from employees where emp_no < 10008) emp_alias"
	df = spark.read.jdbc(url=jdbcUrl, table=pushdown_query, properties=connectionProperties)
	display(df)
	
	#write
	df=spark.createDataFrame([(1, "test1"),(2,"test2")],["id", "name"])
	df.write.jdbc(url=jdbcUrl,table="users",mode="overwrite",properties=connectionProperties)


########################################################################
## save data to local Disc

	spark.createDataFrame( PandasDF.reset_index() ).write.mode("overwrite").saveAsTable("TableName")

########################################################################
## read data from local Disc

	df_spark = spark.sql("select * from TableName")
	
	df_pd = df_spark.toPandas() # or in one line

####################################################################
#### https://docs.databricks.com/dev-tools/python-sql-connector.html

	from databricks import sql
	
	with sql.connect(server_hostname="<server-hostname>",
	                 http_path="<http-path>",
	                 access_token="<access-token>") as connection:
	    with connection.cursor() as cursor:
	        cursor.execute("SELECT * FROM <database-name>.<table-name> LIMIT 2")
	        result = cursor.fetchall()
	
	        for row in result:
	          print(row)

          
###################################################################################          
###################################################################################
#### Mount Storage -> DataLakeStoregeFile (DFSF)

	# For key-valute
	adls_name = dbutils.secrets.get(scope = "scope_in_kv", key="adls-name_in_kv") 
	adls_key = dbutils.secrets.get(scope = "scope_in_kv", key="key_name_in_kv")
	# or from key generated inside storage recource (in Azure)
	adls_key ='xxx=='
	adls_name = 'Name_of_Storage'
	
	
	#Mount adls file system
	container_name = 'Container_Name'
	
	if all(mount.mountPoint != "/mnt/"+container_name for mount in dbutils.fs.mounts()):
	  dbutils.fs.mount(
	    source = "wasbs://"+container_name+"@"+adls_name+".blob.core.windows.net",
	    mount_point = "/mnt/"+container_name,
	    extra_configs = {"fs.azure.account.key."+adls_name+".blob.core.windows.net":adls_key} )
	
	
	  
	# define path to raport folders
	PathToFolder = f'/dbfs/mnt/{container_name}/FolderName/'  
	 
	
	#Unmount adls file system
	mount_point = "/mnt/" + container_name
	
	if any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts()):
	  dbutils.fs.unmount(mount_point)

  
###################################################################################          
###################################################################################
#### write data into FileStore

	FileName.to_csv( "/dbfs/FileStore/MyFolderName/MyFileName.csv" )

### read data

	df = pd.read_csv( '/dbfs/FileStore/MyFolderName/MyFileName.csv' )


###################################################################################          
###################################################################################
#### Clear memory besides some variables

	def ClearMemory( BaseVariableList ):
	
		DataListCurrent = [k for (k,v) in globals().items() ]
		diffVar = list( set(DataListCurrent)-set(BaseVariableList ) )
	
	
		for Var in diffVar:
		   try:
			del globals()[Var]
			import gc
			gc.collect()
		   except KeyError:
			next
    
###################################################################################          
###################################################################################
#### Inside DataBrics Script Define Basic Variable List which shoudn't be delated (return all variables in cuurrent moment)

	DataList = []
	DataList = [k for (k,v) in globals().items() ]
	
	### After the statment below all variables despie of defined in'DataList' will be delated
	
	ClearMemory(DataList)

###################################################################################          
###################################################################################
#### scope list using pyspark

	dbutils.secrets.listScopes()

###################################################################################          
###################################################################################
#### save data into SQL DB

        ### define connection properties

	jdbcUsername = dbutils.secrets.get(scope = "scope_name", key="username_for_db_user")
	jdbcPassword = dbutils.secrets.get(scope = "scope_name", key="password_for_db_user")
	
	
	jdbcHostname = "server_name"
	jdbcPort = 1433
	jdbcDatabase = "db_name"
	
	### define function to write data
	def write_into_SQL_AZURE_with_col_type(df_pandas, schema_name, table_name, columns_type):
	
	  spark.createDataFrame(df_pandas).write \
	      .mode("overwrite")\
	      .format("jdbc")\
	      .option("url", f"jdbc:sqlserver://{jdbcHostname}:1433;databaseName={jdbcDatabase}")\
	      .option("dbtable", f"[{schema_name}].[{table_name}]")\
	      .option("user", f'{jdbcUsername}')\
	      .option("password", f'{jdbcPassword}')\
	      .option("createTableColumnTypes", columns_type)\
	      .save()

        ### define funtion to evaulate data types string
	def evalute_columns_type_string(df, object_type = 'VARCHAR(20)', numeric_type = 'DECIMAL(10, 2)', date_type = 'date'):
	
	  cols_type_object = ", ".join([f"`{column}` {object_type}"  for column in df.select_dtypes(include=['object'] ).columns ])
	  cols_type_numeric = ", ".join([f"`{column}` {numeric_type}"  for column in df.select_dtypes(include= ['number'] ).columns ])
	  cols_type_date = ", ".join([f"`{column}` {date_type}"  for column in df.select_dtypes(include= ['datetime64', 'datetime64[ns]'] ).columns ])
	  
	  cols_type = cols_type_object + ', ' + cols_type_numeric + ', ' + cols_type_date
	
	  return cols_type

	### 
	cols_types = evalute_columns_type_string(df, object_type = 'VARCHAR(30)', numeric_type = 'INT', date_type = 'date')

	### save into SQL
	schema_name = 'schema_name'
	table_name = 'table_name'
	
	write_into_SQL_AZURE_with_col_type(df, schema_name, table_name, cols_types)


###################################################################################          
###################################################################################
#### run stored procedure

	# define ciinection properties

	jdbcUsername = dbutils.secrets.get(scope = "scope_name", key="username_for_db_user")
	jdbcPassword = dbutils.secrets.get(scope = "scope_name", key="password_for_db_user")
	
	
	jdbcHostname = "server_name"
	jdbcPort = 1433
	jdbcDatabase = "db_name"

	# get url
	jdbcUrl = f"jdbc:sqlserver://{jdbcHostname}:1433;databaseName={jdbcDatabase}"
	
	# run procedure
	driver_manager = spark._sc._gateway.jvm.java.sql.DriverManager
	connection = driver_manager.getConnection(jdbcUrl, jdbcUsername, jdbcPassword)
	connection.prepareCall("EXEC Europe.sp_name").execute()
	connection.close()
