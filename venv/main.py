from data_pull import data_pull
from format import format
from analysis import Analysis, Datapull
import pandas as pd

# example of how to run

if __name__ == "__main__":
    Datapull("Beat_Bobby_Flay.xlsx",
             "Beat_Bobby_Flay_season_data.xlsx")

    c = Analysis(pd.read_excel("Beat_Bobby_Flay.xlsx"),"Beat_Bobby_Flay_season_data.xlsx")
    c.data_pull()

