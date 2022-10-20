-- Create schema
CREATE SCHEMA schema_name

-- to deltae shama it must by empty - without tables
DROP SCHEMA schema_name


--
CREATE TABLE Texas_Electricity_Demand2 (
    [Date]     VARCHAR(30)  NOT NULL PRIMARY KEY,
    [Demand]   Decimal(8,1),
    [Date2] DATETIME,
    )


-- delate table
DROP TABLE [dbo].[tableName]


-- copy tables columns and stracture into other table
SELECT  *
    INTO [SchmaName].[TableName1]
FROM [SchmaName1].[TableName2]
    WHERE 1=2
go


-- delate all rows
TRUNCATE TABLE [dbo].[tableName]


-- Insert into Table1 from Table2:
INSERT INTO [schemaName].[Table1] (
       [col1]
      ,[col2] )
SELECT [col1]
      ,[col2] 
FROM [schemaName].[Table2]


-- Delate rows based on condition
DELETE  from [scheaName].[TableName]
where colunmName = 'value'


-- Delate rows from Table1 duplicated in Table2 based on come column:
DELETE t1 
FROM [schemaName].[Table1] as t1
INNER JOIN [schemaName].[Table2] as t2 ON t1.ColNameInTable1 = t2.ColNameInTable2;


-- Update values
UPDATE [scheaName].[TableName]
SET column1 = value1, column2 = value2, ...
WHERE condition; 
