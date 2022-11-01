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
    #### Creates Tables ###################################################
    #######################################################################

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

    def db_table(self):
        # establishes db connection
        connection = self.db_bobby
        cursor = connection.cursor()

        # tries to create table is none exists
        try:
            cursor.execute(
                "CREATE TABLE beat_bobby_flay ("
                "episode_no INTEGER UNIQUE, "
                "season_episode_no INTEGER, "
                "title TEXT, "
                "original_air_date TEXT, "
                "guests TEXT, "
                "ingredients TEXT, "
                "contestants TEXT, "
                "judges TEXT, "
                "dish TEXT, "
                "winner TEXT, "
                "season INTEGER)"
            )
        except:
            pass

    def win_rate_dim(self):
        # establishes db connection
        connection = self.db_bobby
        cursor = connection.cursor()

        # tries to create table is none exists
        try:
            cursor.execute(
                "CREATE TABLE win_rate_dim ("
                "season INTEGER UNIQUE, "
                "win_rate FLOAT, "
            )

        except:
            pass

    def winners_dish_dim(self):
        # establishes db connection
        connection = self.db_bobby
        cursor = connection.cursor()

        # tries to create table is none exists
        try:
            cursor.execute(
                "CREATE TABLE winners_dish_dim ("
                "episode_no INTEGER UNIQUE, "
                "season INTEGER, "
                "winner TEXT, "
                "dish TEXT, "
            )
        except:
            pass

    def loss_date_dim(self):
        # establishes db connection
        connection = self.db_bobby
        cursor = connection.cursor()

        # tries to create table is none exists
        try:
            cursor.execute(
                "CREATE TABLE loss_date_dim ("
                "loss_date TEXT UNIQUE, "
                "total INTEGER, "
            )
        except:
            pass

    def loss_date_by_year_dim(self):
        # establishes db connection
        connection = self.db_bobby
        cursor = connection.cursor()

        # tries to create table is none exists
        try:
            cursor.execute(
                "CREATE TABLE loss_date_by_year_dim ("
                "year INTEGER UNIQUE, "
                "total INTEGER, "
            )
        except:
            pass

    def loss_date_by_month_dim(self):
        # establishes db connection
        connection = self.db_bobby
        cursor = connection.cursor()

        # tries to create table is none exists
        try:
            cursor.execute(
                "CREATE TABLE loss_date_by_month_dim ("
                "month TEXT UNIQUE, "
                "total INTEGER, "
            )
        except:
            pass

    def loss_date_by_day_dim(self):
        # establishes db connection
        connection = self.db_bobby
        cursor = connection.cursor()

        # tries to create table is none exists
        try:
            cursor.execute(
                "CREATE TABLE loss_date_by_day_dim ("
                "day INTEGER UNIQUE, "
                "total INTEGER, "
            )
        except:
            pass


    #######################################################################
    #### Populates Tables #################################################
    #######################################################################

    def season_data(self):

        ''' need to update to create temp table then compare back to main table then insert missing values'''

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

            engine = create_engine("sqlite:///BBF.db", echo=False)

            df1.to_sql(
                "beat_bobby_flay",
                con=engine,
                if_exists="append",
                index=False
            )

    def win_rate_pop(self):
        connection = self.db_bobby
        cursor = connection.cursor()
        seasons = self.number_of_seasons()

        # creates empty lists that we'll use to populate table
        season = []
        rate = []

        # loops through seasons to populate df
        for i in range(1, seasons + 1):
            seasons_list_range = i
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(i,),
            )

            wins = df["winner"].value_counts().head(1)
            win_rate = (round(wins[0] / len(df.index) * 100, 2))

            season.append(i)
            rate.append(win_rate)

        # creates df we're going to throw in table
        df = pd.DataFrame()
        df['season']=season
        df['win_rate']=rate

        engine = create_engine("sqlite:///BBF.db", echo=False)

        df.to_sql(
            "win_rate_dim",
            con=engine,
            if_exists="replace",
            index=False
        )

        df.to_csv("C:/Users/Brian/PycharmProjects/beat_bobby_flay/venv/csv/win_rate.csv",index=False, encoding='utf-8-sig')

    def winners_dish_pop(self):
        connection = self.db_bobby
        cursor = connection.cursor()

        df = pd.read_sql_query(
            "SELECT * FROM beat_bobby_flay",
            connection
        )
        winners_dish = df[df["winner"] != "Bobby Flay"]
        winners_dish = winners_dish[["season","episode_no","winner","dish"]]

        engine = create_engine("sqlite:///BBF.db", echo=False)

        winners_dish.to_sql(
            "winners_dish_dim",
            con=engine,
            if_exists="replace",
            index=False
        )

        df.to_csv("C:/Users/Brian/PycharmProjects/beat_bobby_flay/venv/csv/winners_dish.csv", index=False, encoding='utf-8-sig')

    def loss_date_pop(self):
        connection = self.db_bobby
        cursor = connection.cursor()

        df = pd.read_sql_query(
            "SELECT * FROM beat_bobby_flay",
            connection
        )

        df = df[df["winner"] != "Bobby Flay"]
        df = df[["winner", "original_air_date"]]

        engine = create_engine("sqlite:///BBF.db", echo=False)

        df.to_sql(
            "loss_date_dim",
            con=engine,
            if_exists="replace",
            index=False
        )

        df.to_csv("C:/Users/Brian/PycharmProjects/beat_bobby_flay/venv/csv/loss_date.csv", index=False, encoding='utf-8-sig')

    def loss_date_by_year_pop(self):
        connection = self.db_bobby
        cursor = connection.cursor()

        df = pd.read_sql_query(
            "SELECT * FROM beat_bobby_flay",
            connection
        )

        df = pd.read_sql_query(
            "SELECT * FROM beat_bobby_flay",
            connection
        )
        df = df[df["winner"] != "Bobby Flay"]
        df = (
            df["original_air_date"]
                .str[-4:]
                .value_counts()
                .sort_index(ascending=False)
        )

        engine = create_engine("sqlite:///BBF.db", echo=False)

        df.to_sql(
            "loss_date_by_year_dim",
            con=engine,
            if_exists="replace",
            index=False
        )

        df.to_csv("C:/Users/Brian/PycharmProjects/beat_bobby_flay/venv/csv/loss_date_by_year.csv", encoding='utf-8-sig')

    def loss_date_by_month_pop(self):
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

        df = pd.read_sql_query(
            "SELECT * FROM beat_bobby_flay",
            connection
        )

        df = pd.read_sql_query(
            "SELECT * FROM beat_bobby_flay",
            connection
        )

        df = df[df["winner"] != "Bobby Flay"]
        df = df["original_air_date"].str[:3].value_counts().reindex(cat)


        engine = create_engine("sqlite:///BBF.db", echo=False)

        df.to_sql(
            "loss_date_by_month_dim",
            con=engine,
            if_exists="replace",
            index=False
        )

        df.to_csv("C:/Users/Brian/PycharmProjects/beat_bobby_flay/venv/csv/loss_date_by_month.csv", encoding='utf-8-sig')

    def loss_date_by_day_pop(self):
        connection = self.db_bobby
        cursor = connection.cursor()

        df = pd.read_sql_query(
            "SELECT * FROM beat_bobby_flay",
            connection
        )

        df = pd.read_sql_query(
            "SELECT * FROM beat_bobby_flay",
            connection,
        )
        df = df[df["winner"] != "Bobby Flay"]
        df = df["original_air_date"].str[-8:-6].value_counts()

        engine = create_engine("sqlite:///BBF.db", echo=False)

        df.to_sql(
            "loss_date_by_month_dim",
            con=engine,
            if_exists="replace",
            index=False
        )

        df.to_csv("C:/Users/Brian/PycharmProjects/beat_bobby_flay/venv/csv/loss_date_by_day.csv", encoding='utf-8-sig')

    #######################################################################
    #### View Tables ######################################################
    #######################################################################

    def win_rate(self):
        connection = self.db_bobby
        cursor = connection.cursor()

        data = pd.read_sql_query("SELECT * FROM win_rate_dim",connection)
        print(type(data['season'][0]))



    def winners_dish(self):
        connection = self.db_bobby
        cursor = connection.cursor()

    def loss_date(self):
        connection = self.db_bobby
        cursor = connection.cursor()

    def loss_date_by_year(self):
        connection = self.db_bobby
        cursor = connection.cursor()

    def loss_date_by_month(self):
        connection = self.db_bobby
        cursor = connection.cursor()

    def loss_date_by_day(self):
        connection = self.db_bobby
        cursor = connection.cursor()

    #######################################################################
    #### Analysis functions         #######################################
    #### Draws data from fact table #######################################
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
            print(f"{len(df.index)} total challenges")
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            print(f"{len(df.index)} total challenges in season {season}")
        else:
            print(f"{season} doesn't exist or hasn't aired yet")

    # calculates win breakdown
    def win_breakdown(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            data = df["winner"].value_counts()
            print('total challeges bobby has won: %s out of %s' % (data.head(1)[0],(len(data) + data.head(1)[0])))

        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            data = df["winner"].value_counts()
            print(f'total challeges bobby has won: %s out of %s in season %s' % (data.head(1)[0], (len(data) + data.head(1)[0]),season))
        else:
            print('%s season does not exist or has not aired yet' % (season))

    # calculates bobby's w/l percentage
    def bobby_win_rate(self, season=None):
        connection = self.db_bobby
        cursor = connection.cursor()

        if season == None:
            df = pd.read_sql_query("SELECT * FROM beat_bobby_flay", connection)
            wins = df["winner"].value_counts().head(1)
            print("Bobby has a %s win rate" % (round(wins[0] / len(df.index) * 100, 2)))
        elif season > 0 and season <= self.number_of_seasons():
            df = pd.read_sql_query(
                "SELECT * FROM beat_bobby_flay WHERE season = ?",
                connection,
                params=(season,),
            )
            wins = df["winner"].value_counts().head(1)
            print("Bobby has a %s win rate" % (round(wins[0] / len(df.index) * 100, 2)))

        else:
            print('%s season does not exist or has not aired yet' % (season))

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
            print('%s season does not exist or has not aired yet' % (season))

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
            print('%s season does not exist or has not aired yet' % (season))

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
            print('%s season does not exist or has not aired yet' % (season))

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
            print('%s season does not exist or has not aired yet' % (season))

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
            print('%s season does not exist or has not aired yet' % (season))
