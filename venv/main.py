from analysis import Datapull
import pandas as pd
import sqlite3

pd.options.display.width = None
pd.options.display.max_columns = None
pd.set_option("display.max_rows", 3000)
pd.set_option("display.max_columns", 3000)
pd.set_option("display.float_format", lambda x: "%.5f" % x)

# example of how to run

if __name__ == "__main__":

    #######################################################################
    #### creates data warehouse ###########################################
    #######################################################################

    Datapull(sqlite3.connect("BBF.db")).db_table()
    Datapull(sqlite3.connect("BBF.db")).win_rate_dim()
    Datapull(sqlite3.connect("BBF.db")).winners_dish_dim()
    Datapull(sqlite3.connect("BBF.db")).loss_date_dim()
    Datapull(sqlite3.connect("BBF.db")).loss_date_by_year_dim()
    Datapull(sqlite3.connect("BBF.db")).loss_date_by_month_dim()
    Datapull(sqlite3.connect("BBF.db")).loss_date_by_day_dim()

    #######################################################################
    #### populates tables #################################################
    #######################################################################

    Datapull(sqlite3.connect("BBF.db")).season_data()
    Datapull(sqlite3.connect("BBF.db")).win_rate_pop()
    Datapull(sqlite3.connect("BBF.db")).winners_dish_pop()
    Datapull(sqlite3.connect("BBF.db")).loss_date_pop()
    Datapull(sqlite3.connect("BBF.db")).loss_date_by_year_pop()
    Datapull(sqlite3.connect("BBF.db")).loss_date_by_month_pop()
    Datapull(sqlite3.connect("BBF.db")).loss_date_by_day_pop()

    #######################################################################
    #### data view ########################################################
    #######################################################################

    # Datapull(sqlite3.connect("BBF.db")).win_rate()

    #######################################################################
    #### data display #####################################################
    #######################################################################

    # Datapull(sqlite3.connect("BBF.db")).number_of_seasons()
    # Datapull(sqlite3.connect("BBF.db")).read_table()
    # Datapull(sqlite3.connect("BBF.db")).total_challanges()
    # Datapull(sqlite3.connect("BBF.db")).win_breakdown()
    # Datapull(sqlite3.connect("BBF.db")).bobby_win_rate(31)
    # Datapull(sqlite3.connect("BBF.db")).winners_dish()
    # Datapull(sqlite3.connect("BBF.db")).loss_date()
    # Datapull(sqlite3.connect("BBF.db")).loss_by_year()
    # Datapull(sqlite3.connect("BBF.db")).loss_month()
    # Datapull(sqlite3.connect("BBF.db")).day_of_month()



