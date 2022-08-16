--------------------------------------------------------
-- add user to azure DB
--
-- You should be loged as 'Azure Active Directory admin' to give access to user from AD
-- The best create group in AD and give access to group
--

CREATE USER [GroupNameInAD] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [GroupNameInAD];
GO



##############################
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
