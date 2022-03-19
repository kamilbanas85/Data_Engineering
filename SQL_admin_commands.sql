--------------------------------------------------------
-- add user to azure DB 

CREATE USER [DashboardProba003] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [DashboardProba003];
GO


--------------------------------------------------------
-- check users and them permissions

select name as username,
       create_date,
       modify_date,
       type_desc as type,
       authentication_type_desc as authentication_type
from sys.database_principals
where type not in ('A', 'G', 'R', 'X')
      and sid is not null
      and name != 'guest'
order by username;
