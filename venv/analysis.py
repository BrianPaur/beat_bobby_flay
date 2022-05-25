import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
from openpyxl import Workbook, load_workbook
import openpyxl
import os
from os.path import exists
import gender_guesser.detector as gender

#######################################################################
#### Main data pull ###################################################
#######################################################################

class Datapull:

    def __init__(self, wbname="Beat_Bobby_Flay.xlsx", wbseason="Beat_Bobby_Flay_season_data.xlsx"):
        self.wbname = wbname
        self.wbseason = wbseason

    def data_pull(self):

        # creates workbook
        w = Workbook()
        w.save(self.wbname)
        w.close()

        # url for data
        wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
        response = requests.get(wikiurl)
        soup = BeautifulSoup(response.text, 'html.parser')

        # get the number of seasons from wiki table
        number_of_seasons = int(
            etree.fromstring(response.text).xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[8]/td')[
                0].text)

        # finds the different season tables on the wiki page
        my_tables = soup.find_all("table", {"class": "wikitable"})
        df = pd.read_html(str(my_tables))

        # creates season data workbook
        writer = pd.ExcelWriter(self.wbseason, engine='openpyxl')

        # names sheets
        for i in range(0, number_of_seasons):
            pd.DataFrame(df[i]).to_excel(writer, f"season {i + 1}")
            writer.save()

        writer.close()

        # formats the sheets to remove unnecessary headers
        for i in range(0, number_of_seasons):
            wb = load_workbook(self.wbseason)
            ws = wb[f'season {i + 1}']
            ws.delete_rows(3, 1)
            wb.save(self.wbseason)

        wb.close()

#######################################################################
#### Formats the workbooks ############################################
#######################################################################

class Format:

    def __init__(self, wbname="Beat_Bobby_Flay.xlsx", wbseason="Beat_Bobby_Flay_season_data.xlsx"):
        self.wbname = wbname
        self.wbseason = wbseason

    def format(self):
        all_df = pd.read_excel(self.wbseason, sheet_name=None)
        df = pd.concat(all_df, ignore_index=True)
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])  # drops headers that were taking up space
        df = df[df['Title'] != 'Title']

        # creates wb for all data to be combine on
        writer = pd.ExcelWriter(self.wbname, engine='openpyxl')
        df.to_excel(writer, "All Data")
        writer.save()
        writer.close()

#######################################################################
#### Analysis functions ###############################################
#######################################################################

class Analysis:

    def __init__(self, df=pd.read_excel("Beat_Bobby_Flay.xlsx"), df_by_season="Beat_Bobby_Flay_season_data.xlsx"):
        self.df = df
        self.df_by_season = df_by_season

    # returns whole dataframe
    def data_frame(self):
        print(self.df)

    # calculates total amount of challeges
    def total_challanges(self):
        print(len(self.df.index))

    # calculates win breakdown
    def win_breakdown(self):
        data = self.df['Winner'].value_counts()

        print(f'total challeges bobby has won: {data.head(1)[0]} out of {len(data)+data.head(1)[0]}')

    # calculates win breakdown by season
    def win_breakdown_by_season(self, season=None):
        #defaults to the latest season if none provided
        if season == None:
            # url for data
            wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
            response = requests.get(wikiurl)
            soup = BeautifulSoup(response.text, 'html.parser')
            season = int(etree.fromstring(response.text).xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[8]/td')[0].text)

            df = pd.read_excel(self.df_by_season,sheet_name=f'season {season}')
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

            print(f'total challeges {len(df.index)}')
            print(df['Winner'].value_counts())

        else:
            df = pd.read_excel(self.df_by_season,sheet_name=f'season {season}')
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])

            print(f'total challeges {len(df.index)}')
            print(df['Winner'].value_counts())

    # calculates bobby's w/l percentage
    def bobby_win_rate(self):
        wins = self.df['Winner'].value_counts().head(1)
        print(f'Bobby has a {round(wins[0]/len(self.df.index)*100,2)}% win rate')

    # calculates bobby's w/l percentage by season
    def bobby_win_rate_by_season(self):
        # url for data for number of seasons
        wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
        response = requests.get(wikiurl)
        soup = BeautifulSoup(response.text, 'html.parser')
        season = int(etree.fromstring(response.text).xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[8]/td')[0].text)

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

    # shows winners dish
    def winners_dish(self):
        winners_dish = df[self.df['Winner'] != 'Bobby Flay']
        winners_dish = winners_dish[['Dish','Winner']]
        print(winners_dish)

    # shows winners dish by season
    def winners_dish_by_season(self, season=None):
        if season == None:
            # url for data for number of seasons
            wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
            response = requests.get(wikiurl)
            soup = BeautifulSoup(response.text, 'html.parser')
            season = int(etree.fromstring(response.text).xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[8]/td')[0].text)

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

    # shows date of losses
    def loss_date(self):
        df = self.df
        df = df[self.df['Winner'] != 'Bobby Flay']
        df = df['Original airdate']
        print(df)

    # tallies up the losses by year
    def loss_year(self):
        df = self.df
        df = df[self.df['Winner'] != 'Bobby Flay']
        df = df['Original airdate'].str[-4:].value_counts().sort_index(ascending=False)
        print(df)

    # tallies up the losses by month
    def loss_month(self):
        cat = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun', 'Jul', 'Aug','Sep', 'Oct', 'Nov', 'Dec']
        df = self.df
        df = df[self.df['Winner'] != 'Bobby Flay']
        df = df['Original airdate'].str[:3].value_counts().reindex(cat)
        print(df)

    # tallies up the losses by day of month
    def time_of_month(self):
        df = self.df
        df = df[self.df['Winner'] != 'Bobby Flay']
        df = df['Original airdate'].str[-8:-6].value_counts()
        print(df)










