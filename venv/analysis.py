import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
import sqlite3
from sqlalchemy import create_engine
import gender_guesser.detector as gender
import os


class Datapull:
    def __init__(self, db_bobby=None):
        self.db_bobby = db_bobby

    #######################################################################
    #### Main data pull ###################################################
    #######################################################################

    def db_table(self):
        # establishes db connection
        connection = self.db_bobby
        cursor = connection.cursor()

        # tries to create table is none exists
        try:
            cursor.execute(
                "CREATE TABLE beat_bobby_flay (episode_no INTEGER UNIQUE, season_episode_no INTEGER, title TEXT, original_air_date TEXT, guests TEXT, ingredients TEXT, contestants TEXT, judges TEXT, dish TEXT, winner TEXT, season INTEGER)"
            )
        except:
            pass

        df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)

        return df

    def number_of_seasons(self):
        # url for data
        wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
        response = requests.get(wikiurl)
        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))
        return int(
            dom.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[8]/td')[
                0
            ].text
        )

    def season_data(self):

        try:
            # url for data
            wikiurl = "https://en.wikipedia.org/wiki/Beat_Bobby_Flay"
            response = requests.get(wikiurl)
            soup = BeautifulSoup(response.content, "html.parser")
            my_tables = soup.find_all("table", {"class": "wikitable"})
            df = pd.read_html(str(my_tables))
            seasons = self.number_of_seasons()

            for i in range(1, seasons + 1):
                seasons_list_range = i - 1

                # selects season from table list
                df1 = df[(i - 1)]

                # adds season column
                df1["season"] = None

                # add season number to dataframe
                df1 = df1.assign(season=i)

                # reassigns the headers
                df1.columns = [
                    "episode_no",
                    "season_episode_no",
                    "title",
                    "original_air_date",
                    "guests",
                    "ingredients",
                    "contestants",
                    "judges",
                    "dish",
                    "winner",
                    "season",
                ]

                print(df1)

                engine = create_engine("sqlite:///BBF.db", echo=False)

                df1.to_sql(
                    "beat_bobby_flay", con=engine, if_exists="append", index=False
                )
        except:
            print("all data up to date")

    #######################################################################
    #### Analysis functions ###############################################
    #######################################################################

    # returns whole dataframe
    def read_table(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            print(pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection))
        elif season > 0 and season <= self.number_of_seasons():
            print(
                pd.read_sql_query(
                    "SELECT * FROM beat_bobby_flay WHERE season = ?",
                    connection,
                    params=(season,),
                )
            )
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # calculates total amount of challeges
    def total_challanges(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            return len(df.index)
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            return len(df.index)
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # calculates win breakdown
    def win_breakdown(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            data = df["winner"].value_counts()
            print(
                f"total challeges bobby has won: {data.head(1)[0]} out of {len(data) + data.head(1)[0]}"
            )

        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            data = df["winner"].value_counts()
            print(
                f"total challeges bobby has won: {data.head(1)[0]} out of {len(data) + data.head(1)[0]}"
            )
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # calculates bobby's w/l percentage
    def bobby_win_rate(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            wins = df["winner"].value_counts().head(1)
            print(f"Bobby has a {round(wins[0] / len(df.index) * 100, 2)}% win rate")
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            wins = df["winner"].value_counts().head(1)
            print(
                f"Bobby has a {round(wins[0] / len(df.index) * 100, 2)}% win rate for season {season}"
            )
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # shows winners dish
    def winners_dish(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            winners_dish = df[df["winner"] != "Bobby Flay"]
            winners_dish = winners_dish[["winner", "dish"]]
            print(winners_dish)
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            winners_dish = df[df["winner"] != "Bobby Flay"]
            winners_dish = winners_dish[["winner", "dish"]]
            print(winners_dish)
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # shows date of losses
    def loss_date(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            df = df[df["winner"] != "Bobby Flay"]
            df = df[["winner", "original_air_date"]]
            print(df)
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            df = df[df["winner"] != "Bobby Flay"]
            df = df[["winner", "original_air_date"]]
            print(df)
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # tallies up the losses by year
    def loss_by_year(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            df = df[df["winner"] != "Bobby Flay"]
            df = (
                df["original_air_date"]
                .str[-4:]
                .value_counts()
                .sort_index(ascending=False)
            )
            print(df)
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            df = df[df["winner"] != "Bobby Flay"]
            df = (
                df["original_air_date"]
                .str[-4:]
                .value_counts()
                .sort_index(ascending=False)
            )
            print(df)
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # tallies up the losses by month
    def loss_month(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        cat = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            df = df[df["winner"] != "Bobby Flay"]
            df = df["original_air_date"].str[:3].value_counts().reindex(cat)
            print(df)
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            df = df[df["winner"] != "Bobby Flay"]
            df = df["original_air_date"].str[:3].value_counts().reindex(cat)
            print(df)
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # tallies up the losses by day of month
    def day_of_month(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            df = df[df["winner"] != "Bobby Flay"]
            df = df["original_air_date"].str[-8:-6].value_counts()
            print(df)
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            df = df[df["winner"] != "Bobby Flay"]
            df = df["original_air_date"].str[-8:-6].value_counts()
            print(df)
        else:
            print(f"{season} doesn't exist or hasn't aired yet")
