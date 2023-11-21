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
