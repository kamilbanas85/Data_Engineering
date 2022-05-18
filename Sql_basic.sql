-- Create schema
CREATE SCHEMA schema_name


--
CREATE TABLE Texas_Electricity_Demand2 (
    [Date]     VARCHAR(30)  NOT NULL PRIMARY KEY,
    Demand   Decimal(8,1) )


-- delate table
DROP TABLE [dbo].[tableName]


-- delate all rows
TRUNCATE TABLE [dbo].[tableName]


-- insert into Table1 from Table2:
INSERT INTO [schemaName].[Table1] (
       [col1]
      ,[col2] )
SELECT [col1]
      ,[col2] 
FROM [schemaName].[Table2]


-- delate rows from Table1 duplicated in Table2 based on come column:
DELETE t1 
FROM [schemaName].[Table1] as t1
INNER JOIN [schemaName].[Table2] as t2 ON t1.ColNameInTable1 = t2.ColNameInTable2;


