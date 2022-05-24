import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook, load_workbook
import openpyxl
import os

#######################################################################
#### Formats the workbooks ############################################
#######################################################################
def format():
    all_df = pd.read_excel("Beat_Bobby_Flay_season_data.xlsx",sheet_name=None)
    df = pd.concat(all_df, ignore_index=True)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0]) #drops headers that were taking up space
    df = df[df['Title']!='Title']

    #creates wb for all data to be combine on
    writer = pd.ExcelWriter("Beat_Bobby_Flay.xlsx", engine = 'openpyxl')
    df.to_excel(writer,"All Data")
    writer.save()
    writer.close()

