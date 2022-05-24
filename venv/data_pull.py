import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook, load_workbook
import openpyxl
import os

#######################################################################
#### Main data pull ###################################################
#######################################################################

def data_pull():

    #creates workbook
    w = Workbook()
    os.chdir("C:/Users/Brian/Desktop/beat_bobby_flay/")  #will need to add in dynamic path
    w.save("Beat_Bobby_Flay.xlsx")
    w.close()

    #url for data
    wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
    response=requests.get(wikiurl)
    soup = BeautifulSoup(response.text, 'html.parser')

    # get the number of seasons from wiki table
    number_of_seasons = int(etree.fromstring(response.text).xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[8]/td')[0].text)

    #finds the different season tables on the wiki page
    my_tables = soup.find_all("table",{"class":"wikitable"})
    df = pd.read_html(str(my_tables))

    #creates season data workbook
    writer = pd.ExcelWriter("Beat_Bobby_Flay_season_data.xlsx", engine = 'openpyxl')

    #names sheets
    for i in range(0,number_of_seasons):
        pd.DataFrame(df[i]).to_excel(writer,f"season {i+1}")
        writer.save()

    writer.close()

    #formats the sheets to remove unnecessary headers
    for i in range(0,number_of_seasons):
        wb = load_workbook("C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_season_data.xlsx")
        ws = wb[f'season {i+1}']
        ws.delete_rows(3,1)
        wb.save("C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_season_data.xlsx")

    wb.close()

data_pull()





































# table_class = "wikitable sortable jquery-tablesorter"
# indiatable = soup.find('table',{'class':"wikitable"})
# df = pd.read_html(str(indiatable))
# df = pd.DataFrame(df[0])
# df.to_excel("C:/Users/Brian/Desktop/beat_bobby_flay/beat_bobby_flay.xlsx")

