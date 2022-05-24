import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook, load_workbook
import openpyxl
import os

all_df = pd.read_excel("C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_season_data.xlsx",sheet_name=None)
df = pd.concat(all_df, ignore_index=True)
df = df.rename(columns=df.iloc[0]).drop(df.index[0])
df = df[df['Title']!='Title']

writer = pd.ExcelWriter("C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay.xlsx", engine = 'openpyxl')
df.to_excel(writer,"All Data")
writer.save()
writer.close()

wb = openpyxl.Workbook()
wb.save(filename="C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_analysis.xlsx")
