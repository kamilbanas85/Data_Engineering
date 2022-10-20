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

spark.sql("select * from TableName").toPandas() 

  

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




