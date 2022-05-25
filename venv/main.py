from analysis import Datapull, Format, Analysis
import pandas as pd

# example of how to run

if __name__ == "__main__":
    Datapull().data_pull()

    Format().format()

    Analysis().bobby_win_rate_by_season()

