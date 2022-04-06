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


###################################################################################          
###################################################################################
#### Write data to local storage

