import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook, load_workbook
import openpyxl
import os
import gender_guesser.detector as gender

class Analysis:

    def __init__(self, df, df_by_season):
        self.df = df
        self.df_by_season = df_by_season

    def data_frame(self):
        print(self.df)

    def total_challanges(self):
        print(len(self.df.index))

    def win_breakdown(self):
        data = self.df['Winner'].value_counts()
        file = 'C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_analysis.xlsx'
        sheet ='Win Breakdown'
        book = pd.ExcelWriter(file)

        if sheet not in book.sheetnames:
            book.create_sheet(sheet)
        else:
            pass

        data.to_excel(file, sheet_name=sheet)

        print(f'total challeges {len(data.index)}')
        print(data.head(10))

    def win_breakdown_by_season(self, season=None):
        df = pd.read_excel(self.df_by_season, sheet_name=f'season {season}')
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        data = df['Winner'].value_counts()
        file = 'C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_analysis.xlsx'
        sheet = f'season {season}'
        book = openpyxl.load_workbook(file)

        #checks to see if sheet exist and creates if if it doesn't
        if sheet not in book.sheetnames:
            book.create_sheet(sheet)
        else:
            pass

        #defaults to the latest season if none provided
        if season == None:
            # url for data
            wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
            response = requests.get(wikiurl)
            soup = BeautifulSoup(response.text, 'html.parser')
            season = number_of_seasons = int(etree.fromstring(response.text).xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[8]/td')[0].text)

            data.to_excel(file, sheet_name=sheet)
            df = pd.read_excel(self.df_by_season,sheet_name=f'season {season}')
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])
            print(f'total challeges {len(df.index)}')
            print(df['Winner'].value_counts().head(10))

        else:
            data.to_excel(file, sheet_name=sheet)
            df = pd.read_excel(self.df_by_season,sheet_name=f'season {season}')
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])
            print(f'total challeges {len(df.index)}')
            print(df['Winner'].value_counts().head(10))

    def bobby_win_rate(self):
        wins = self.df['Winner'].value_counts().head(1)
        print(f'Bobby has a {round(wins[0]/len(self.df.index)*100,2)}% win rate')

    def bobby_win_rate_by_season(self):
        # url for data for number of seasons
        wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
        response = requests.get(wikiurl)
        soup = BeautifulSoup(response.text, 'html.parser')
        season = number_of_seasons = int(etree.fromstring(response.text).xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[8]/td')[0].text)

        rows = []

        for i in range(1,(season+1)):

            df = pd.read_excel(self.df_by_season, sheet_name=f'season {i}')
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

            wins = df['Winner'].value_counts().head(1)
            len_of_season = len(df.index)

            rows.append([i, round(wins[0] / len(df.index) * 100, 2),len_of_season])

        # sets up new dataframe
        df2 = pd.DataFrame(rows, columns=["Season", "Win Rate", "Number of Episodes"])

        print(df2.to_string(index=False))

    def winners_dish(self):
        winners_dish = df[self.df['Winner'] != 'Bobby Flay']
        winners_dish = winners_dish[['Dish','Winner']]
        print(winners_dish)

    def winners_dish_by_season(self, season=None):
        if season == None:
            # url for data for number of seasons
            wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
            response = requests.get(wikiurl)
            soup = BeautifulSoup(response.text, 'html.parser')
            season = number_of_seasons = int(etree.fromstring(response.text).xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[8]/td')[0].text)

            df = pd.read_excel(self.df_by_season, sheet_name=f'season {season}')
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])
            if df[df['Winner'] != 'Bobby Flay'].count().all() == 0:
                print('Bobby won every episode...')
            else:
                winners_dish = df[df['Winner'] != 'Bobby Flay']
                winners_dish = winners_dish[['Dish','Winner']]
                print(winners_dish)

        else:
            df = pd.read_excel(self.df_by_season, sheet_name=f'season {season}')
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])
            winners_dish = df[df['Winner'] != 'Bobby Flay']
            winners_dish = winners_dish[['Dish','Winner']]
            print(winners_dish)

    def loss_date(self):
        df = self.df
        df = df[self.df['Winner'] != 'Bobby Flay']
        df = df['Original airdate']
        print(df)

    def loss_year(self):
        df = self.df
        df = df[self.df['Winner'] != 'Bobby Flay']
        df = df['Original airdate'].str[-4:].value_counts().sort_index(ascending=False)
        print(df)

    def loss_month(self):
        cat = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
        df = self.df
        df = df[self.df['Winner'] != 'Bobby Flay']
        df = df['Original airdate'].str[:3].value_counts().reindex(cat)
        print(df)

    def time_of_month(self):
        df = self.df
        df = df[self.df['Winner'] != 'Bobby Flay']
        df = df['Original airdate'].str[-8:-6].value_counts()
        print(df)


if __name__ == "__main__":
    df = pd.read_excel("C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay.xlsx")
    a = Analysis(df,"C:/Users/Brian/Desktop/beat_bobby_flay/Beat_Bobby_Flay_season_data.xlsx")


    a.win_breakdown_by_season(2)







