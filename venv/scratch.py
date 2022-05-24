import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook, load_workbook
import openpyxl
import os
import gender_guesser.detector as gender

# class Gendr:
#
#     def __init__(self, name):
#         self.name = name
#
#     def gender_guesser(self):
#         print(gender.Detector().get_gender(self.name.title()))
#
#     def data_frame(self):
#         df = pd.read_excel("C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_season_data.xlsx",sheet_name=None)
#         print(df)
#
#
# Gendr('brian').data_frame()



def comma_split_guest():
    #creates workbook
    writer = pd.ExcelWriter("C:/Users/Brian/Desktop/beat_bobby_flay/Split_guests.xlsx", engine = 'openpyxl')

    #reads workbook
    df = pd.read_excel("C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_season_data.xlsx",sheet_name='season 1')
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])

    #creates first dataframe split
    df1 = df.iloc[:,:4]

    #seperates out guest by comma
    dfguest = df['Guest(s)'].str.split(',', expand=True)
    dfguest = dfguest.rename(columns={0:'Guest 1',1:'Guest 2'})

    #creates third dataframe split
    df3 = df['Ingredient(s)']

    #seperates out contestant by comma
    dfcontestant = df['Contestants'].str.split(',', expand=True)
    dfcontestant = dfcontestant.rename(columns={0:'Contestant 1',1:'Contestant 2'})

    #contestant gender

    #seperates out judge by comma
    dfjudge = df['Judges'].str.split(',', expand=True)
    dfjudge = dfjudge.rename(columns={0:'Judge 1',1:'Judge 2',2:'Judge 3'})

    #judge gender

    df4 = df.iloc[:,10:]

    df5 = df1.join(dfguest, how='outer')
    df5 = df5.join(df3, how='outer')
    df5 = df5.join(dfcontestant, how='outer')
    df5 = df5.join(dfjudge, how='outer')
    df5 = df5.join(df4, how='outer')

    print(df5)

    df5.to_excel(writer,"All Data")
    writer.save()
    writer.close()




