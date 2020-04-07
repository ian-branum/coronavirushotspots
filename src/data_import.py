import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
from datetime import datetime

def fixdata(row):
    row['date'] = datetime.strptime(row['date'], '%Y-%m-%d')
    return row

def nyt(fn="./data/raw/covid-19-data/us-counties.csv"):
    df = pd.read_csv(fn)
    df = df.apply(fixdata, axis=1)
    df = df[df['cases'] > 0]
    df = df[df['fips'] > 0]
    #df['fips'].fillna(0, inplace=True)
    #df['cases'].fillna(0, inplace=True)
    #df['deaths'].fillna(0, inplace=True)
    return df

