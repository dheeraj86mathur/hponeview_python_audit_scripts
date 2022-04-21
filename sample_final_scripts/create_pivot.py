import pandas as pd
import numpy as np
import openpyxl 
import xlsxwriter
#from openpyxl import load_workbook
df = pd.read_csv(r"../sample_outputs/oneviewqa_allILOusers_30Jul2021.csv")
df.to_excel(r"../sample_outputs/oneviewqa_allILOusers_30Jul2021.xlsx", sheet_name = 'sheet1', index = False)

df.drop(['S.No','Privilege1','Privilege2','Privilege3','Privilege4','Privilege5','Privilege6','Privilege7','Privilege8','Privilege9','Privilege10'],inplace=True,axis=1)
table = pd.pivot_table(df, index=['User name'],aggfunc={lambda x: len(x.unique())})
print(table)
# Create a Pandas Excel writer using XlsxWriter as the engin
writer = pd.ExcelWriter('pandas_table.xlsx', engine='xlsxwriter')
# Write the dataframe data to XlsxWriter. Turn off the default header and
# index and skip one row to allow us to insert a user defined header.
table.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)
writer.save()
# Get the xlsxwriter workbook and worksheet objects.
writer =  pd.ExcelWriter('../sample_outputs/oneviewqa_allILOusers_30Jul2021.xlsx',  mode="a", engine="openpyxl")
table.to_excel(writer, sheet_name='pivot', startrow=1, header=False)
writer.save()
