### Exctract data from Excel withou Strikethrough
import pandas as pd
import openpyxl

#%%

def ExtractExcelDataWithoutStrikethrough(FileName):
    
    wb = openpyxl.load_workbook(FileName)
    ws = wb.worksheets[0]
    rowsListvalue=[]

    for row in ws:
        rowsListvalue.append( [None if cell.font.strike is True else cell.value  for cell in row] )

    DataDF =  pd.DataFrame(rowsListvalue)
    return DataDF