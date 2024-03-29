################################################################
### create user or gropu from active directory:

CREATE USER [AZ-Users] FROM EXTERNAL PROVIDER
or
CREATE USER [Group Name] FROM EXTERNAL PROVIDER

### add role read or write to user or group (can be withou paanthesis 'MYUSER' :

ALTER ROLE db_datareader ADD MEMBER [MYUSER]
GO
ALTER ROLE db_datawriter ADD MEMBER [MYUSER] 
GO

####
## so to add permitions to new group in ActiveDcirectory

CREATE USER [Group_Name] FROM EXTERNAL PROVIDER

ALTER ROLE db_datareader ADD MEMBER [Group_Name]
GO
ALTER ROLE db_datawriter ADD MEMBER [Group_Name] 
GO

#####

################################################################
###  Grant Schema Permissions

GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA :: <schema> TO <user>;
or based on role ctration:

 -- Create the database role
CREATE ROLE TableSelector AUTHORIZATION [dbo]
GO
 ---- Grant access rights to a specific schema in the database
GRANT 
      SELECT, INSERT, UPDATE, DELETE, ALTER 
ON SCHEMA::dbo
      TO TableSelector 
GO

-- Add an existing user to the new role created 
EXEC sp_addrolemember 'TableSelector', 'MyDBUser'
GO


There is no difference between the two as of SQL Server 2012.

alter role [RoleName] add member [MemberName];
is equivalent to
exec sp_addrolemember N'RoleName', N'MemberName';

 

############################## full code axample

CREATE ROLE db_hza_datawriter AUTHORIZATION [dbo]
GO

 ---- Grant access rights to a specific schema in the database
GRANT 
      SELECT, INSERT, UPDATE, DELETE, ALTER 
ON SCHEMA::hza
      TO db_hza_datawriter 
GO

---- create user
CREATE USER [mf-p-db-hza-write] FROM EXTERNAL PROVIDER


--- add role to gruop
alter role db_hza_datawriter add member [mf-p-db-hza-write];


############################################################ 
############################################################ 
### Create role and add permitions to all stored procedures


CREATE ROLE [db_storedprocedure]

GRANT EXECUTE TO [db_storedprocedure]
GRANT CREATE PROCEDURE TO [db_storedprocedure]
GRANT ALTER TO [db_storedprocedure];

ALTER ROLE db_storedprocedure ADD MEMBER [UserName_or_GroupName]
GO


### in case on schame lavel

GRANT EXECUTE ON SCHEMA ::SchemaName TO [db_storedprocedure]
GRANT CREATE ON SCHEMA ::SchemaName PROCEDURE TO [db_storedprocedure]
GRANT ALTER ON SCHEMA ::SchemaName TO [db_storedprocedure];


################################################################ 
################################################################ 
################################################################
### check perimssion 

## check user permission

SELECT  pri.name As Username
,       pri.type_desc AS [User Type]
,       permit.permission_name AS [Permission]
,       permit.state_desc AS [Permission State]
,       permit.class_desc Class
,       object_name(permit.major_id) AS [Object Name]
FROM    sys.database_principals pri
LEFT JOIN
        sys.database_permissions permit
ON      permit.grantee_principal_id = pri.principal_id


##########
### however when user has db_writer database role it dosn't be listed with command above
### below command shows userrs with database role

SELECT DP1.name AS DatabaseRoleName,   
   isnull (DP2.name, 'No members') AS DatabaseUserName   
 FROM sys.database_role_members AS DRM  
 RIGHT OUTER JOIN sys.database_principals AS DP1  
   ON DRM.role_principal_id = DP1.principal_id  
 LEFT OUTER JOIN sys.database_principals AS DP2  
   ON DRM.member_principal_id = DP2.principal_id  
WHERE DP1.type = 'R'
ORDER BY DP1.name; 

