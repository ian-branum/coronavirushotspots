import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
from datetime import datetime
import mpu
#from util import get_state


def fix_nyt_date(row):
    row['date'] = datetime.strptime(row['date'], '%Y-%m-%d')
    return row

def extract_nyt(fn="./data/raw/covid-19-data/us-counties.csv"):
    df = pd.read_csv(fn)
    df = df.apply(fix_nyt_date, axis=1)
    df = df.apply(strip_state, axis=1)
    df['sc'] = df['state'] + ':' + df['county']
    df = df[df['cases'] > 0]
    df = df[df['fips'] > 0]
    #df['fips'].fillna(0, inplace=True)
    #df['cases'].fillna(0, inplace=True)
    #df['deaths'].fillna(0, inplace=True)
    return df

def strip_state(row):
    row['state'] = row['state'].strip()
    row['county'] = row['county'].strip()
    return row

def extract_hhi(fn="./data/raw/Census/HH_income.csv"):
    df = pd.read_csv(fn)
    df['county'] = df['Geographic Area Name'].str.split(",",expand=True,)[0].str.split(" ", expand=True)[0]
    df['state'] = df['Geographic Area Name'].str.split(",",expand=True,)[1]
    df = df.apply(strip_state, axis=1)
    df['sc'] = df['state'] + ':' + df['county']
    return df[[
        'sc',
        'state', 
        'county',
        'Estimate!!Households!!Total',
        'Estimate!!Households!!Median income (dollars)',
        'Estimate!!Households!!Mean income (dollars)'
    ]]

def extract_public_transport(fn="./data/raw/Census/lots_of_census_data.csv"):
    df = pd.read_csv(fn)
    df['county'] = df['Geographic Area Name'].str.split(",",expand=True,)[0].str.split(" ", expand=True)[0]
    df['state'] = df['Geographic Area Name'].str.split(",",expand=True,)[1]
    df = df.apply(strip_state, axis=1)
    df['sc'] = df['state'] + ':' + df['county']
    return df[[
        'sc',
        'state', 
        'county',
        'Estimate!!Total!!Workers 16 years and over!!MEANS OF TRANSPORTATION TO WORK!!Public transportation (excluding taxicab)'
    ]]

def extract_edu(fn="./data/raw/Census/edu.csv"):
    df = pd.read_csv(fn)
    df['county'] = df['Geographic Area Name'].str.split(",",expand=True,)[0].str.split(" ", expand=True)[0]
    df['state'] = df['Geographic Area Name'].str.split(",",expand=True,)[1]
    df = df.apply(strip_state, axis=1)
    df['sc'] = df['state'] + ':' + df['county']
    return df[[
        'sc',
        'state', 
        'county',
        'Estimate!!Total!!Population 25 years and over',
        'Estimate!!Male!!Population 25 years and over',
        'Estimate!!Percent!!Population 25 years and over!!High school graduate (includes equivalency)',
        'Estimate!!Percent!!Population 25 years and over!!Some college, no degree',
        'Estimate!!Percent!!Population 25 years and over!!Associate\'s degree',
        'Estimate!!Percent!!Population 25 years and over!!Bachelor\'s degree',
        'Estimate!!Percent!!Population 25 years and over!!Graduate or professional degree',
        'Estimate!!Percent!!Population 25 years and over!!Bachelor\'s degree or higher',
        'Estimate!!Total!!Population 25 years and over!!Population 65 years and over',
        'Estimate!!Total!!Population 25 years and over!!Population 65 years and over!!Bachelor\'s degree or higher',
        'Estimate!!Percent!!Population 25 years and over!!Population 65 years and over!!Bachelor\'s degree or higher',
        'Estimate!!Total!!RACE AND HISPANIC OR LATINO ORIGIN BY EDUCATIONAL ATTAINMENT!!White alone',
        'Estimate!!Total!!RACE AND HISPANIC OR LATINO ORIGIN BY EDUCATIONAL ATTAINMENT!!White alone!!Bachelor\'s degree or higher',
        'Estimate!!Percent!!RACE AND HISPANIC OR LATINO ORIGIN BY EDUCATIONAL ATTAINMENT!!White alone!!Bachelor\'s degree or higher',
        'Estimate!!Percent!!RACE AND HISPANIC OR LATINO ORIGIN BY EDUCATIONAL ATTAINMENT!!White alone, not Hispanic or Latino!!Bachelor\'s degree or higher'     
    ]]

def extract_housing(fn="./data/raw/Census/housing.csv"):
    df = pd.read_csv(fn)
    df['county'] = df['Geographic Area Name'].str.split(",",expand=True,)[0].str.split(" ", expand=True)[0]
    df['state'] = df['Geographic Area Name'].str.split(",",expand=True,)[1]
    df = df.apply(strip_state, axis=1)
    df['sc'] = df['state'] + ':' + df['county']
    return df[[
        'sc',
        'state', 
        'county',
        'Estimate!!VALUE!!Owner-occupied units!!Median (dollars)',
        'Estimate!!GROSS RENT!!Occupied units paying rent!!Median (dollars)',
        'Percent Estimate!!HOUSING OCCUPANCY!!Total housing units',
        'Estimate!!HOUSING OCCUPANCY!!Total housing units!!Occupied housing units',
        'Percent Estimate!!HOUSING OCCUPANCY!!Total housing units!!Occupied housing units',
        'Percent Estimate!!UNITS IN STRUCTURE!!Total housing units!!1-unit, detached',
        'Percent Estimate!!UNITS IN STRUCTURE!!Total housing units!!5 to 9 units',
        'Percent Estimate!!UNITS IN STRUCTURE!!Total housing units!!10 to 19 units',
        'Percent Estimate!!UNITS IN STRUCTURE!!Total housing units!!20 or more units'
    ]]

def fix_state_abbr(row):
    row['state'] = get_state(row['state_abbr'])
    return row

def extract_election(fn="./data/raw/US_County_Level_Election_Results_08-16/2016_US_County_Level_Presidential_Results.csv"):
    df = pd.read_csv(fn)
    df['county'] = df['county_name'].str.split(" ",expand=True,)[0]
    df = df.apply(fix_state_abbr, axis=1)
    df['sc'] = df['state'] + ':' + df['county']
    return df[[
        'sc',
        'state', 
        'county',
        'per_dem',
        'per_gop'
    ]]

def convert_airport_numbers(ap):
    ap.pax = int(ap.pax.replace(',', ''))
    ap.domestic = int(ap.domestic.replace(',', ''))
    ap.international = int(ap.international.replace(',', ''))
    return ap 

def extract_airports(fn="./data/raw/Airports.csv"):
    df = pd.read_csv(fn)
    df = df.apply(convert_airport_numbers, axis=1)
    return df

def fix_state_abbr_geo(row):
    row['State'] = get_state(row['State'])
    return row

def fix_county_latlon(county):
    county['Lat'] = float(county['Lat'])
    county['Lon'] = float(county['Lon'].replace('–','-'))
    return county 

def extract_geography(fn="./data/raw/County Physical.csv"):
    df = pd.read_csv(fn, sep='\t')
    df = df.apply(fix_state_abbr_geo, axis=1)
    df['sc'] = df['State'] + ':' + df['County']
    return df

def calc_intl_arrivals_index(lat, lon, threshold, airports_df):
    domestic = 0
    intl = 0
    airports = []
    for i, airport in airports_df.iterrows():
        #print(airport)
        alat = airport['lat']
        alon = airport['lon']
        dist = mpu.haversine_distance((lat, lon), (alat, alon))
        #print('{} is {} km away'.format(airport['airport'], dist))
        if dist < threshold:
            intl += int(airport['international'])
            domestic += int(airport['domestic'])
            airports.append(airport['airport'])
    return intl, domestic, airports
        
def build_intl_arrivals_index_df(counties_df, airports_df, threshold):
    res = pd.DataFrame(columns=['sc', 'international', 'domestic', 'airports'])
    for i, county in counties_df.iterrows():
        intl, domestic, airports = calc_intl_arrivals_index(county['Lat'], float(county['Lon']), threshold, airports_df)
        res.loc[i] = [county['sc'], intl, domestic, airports]
    return res
 

###### Supposed to be in util.py :( 


def get_state(code):
    return states[code]

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

