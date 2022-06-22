from analysis import Datapull
import pandas as pd
import sqlite3

pd.options.display.width = 0
pd.options.display.max_rows = 0

# example of how to run

if __name__ == "__main__":
    Datapull(sqlite3.connect("BBF.db")).read_table()
