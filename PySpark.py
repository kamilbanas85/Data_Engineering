
########################################################################
### Convert data type

from pyspark.sql import functions as F

for col in [MainVar, VarName]:
  VarDataFrom__Long_term_modified = VarDataFrom__Long_term_modified.withColumn(
    col,
    F.col(col).cast("double")
  )
  
  
### or ?

df( "colName",df["colName"].cast(StringType()) )


########################################################################
### Return list od DataFrames

from pyspark.sql import DataFrame

def list_dataframes():

    return [k for (k, v) in globals().items() if isinstance(v, DataFrame)]

 
########################################################################
## add column with contant value

from pyspark.sql.functions import lit

df = df('newColName', lit( someValue ) )


########################################################################
### Select first element from colmn as scalar value
              
var = df.first()['colName']
