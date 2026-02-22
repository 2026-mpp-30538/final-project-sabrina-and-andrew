import os
import pandas as pd
import numpy as np

# Here we will being to pull in and clean crime data to eventually merge with the main Chetty-Hendren Data
directory = 'c:/Users/s_bea/student30538-w26/final-project-sabrina-and-andrew/data'
file_path = '/crime_data/FBI_Crime_Data'

#importing all my data files and adding year column
crime_2024 = pd.read_excel(f'{directory}{file_path}/2024.xlsx',
                            skiprows=4, skipfooter=2)
crime_2024["Year"] = 2024
crime_2023 = pd.read_excel(f'{directory}{file_path}/2023.xlsx',
                            skiprows=4, skipfooter=2, index_col=[0]).reset_index()
crime_2023["Year"] = 2023
crime_2022 = pd.read_excel(f'{directory}{file_path}/2022.xlsx',
                            skiprows=4, skipfooter=2, index_col=[0]).reset_index()
crime_2022["Year"] = 2022
crime_2021 = pd.read_excel(f'{directory}{file_path}/2021.xlsx',
                            skiprows=4, skipfooter=1, index_col=[0]).reset_index()
crime_2021["Year"] = 2021
crime_2020 = pd.read_excel(f'{directory}{file_path}/2020.xlsx',
                            skiprows=6, skipfooter=9, index_col=[0]).reset_index()
crime_2020["Year"] = 2020
# for files 2019 and before, these are xls, so user will need to install xlrd in terminal
crime_2019 = pd.read_excel(f'{directory}{file_path}/2019.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index() 
crime_2019["Year"] = 2019
crime_2018 = pd.read_excel(f'{directory}{file_path}/2018.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index()
crime_2018["Year"] = 2018 
crime_2017 = pd.read_excel(f'{directory}{file_path}/2017.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index() 
crime_2017["Year"] = 2017 
crime_2016 = pd.read_excel(f'{directory}{file_path}/2016.xls',
                            skiprows=4, skipfooter=9, index_col=[0]).reset_index() 
crime_2016["Year"] = 2016
crime_2015 = pd.read_excel(f'{directory}{file_path}/2015.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index()
crime_2015["Year"] = 2015 
crime_2014 = pd.read_excel(f'{directory}{file_path}/2014.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index()
crime_2014["Year"] = 2014
crime_2013 = pd.read_excel(f'{directory}{file_path}/2013.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index() 
crime_2013["Year"] = 2013
crime_2012 = pd.read_excel(f'{directory}{file_path}/2012.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index() 
crime_2012["Year"] = 2012 
crime_2011 = pd.read_excel(f'{directory}{file_path}/2011.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index() 
crime_2011["Year"] = 2011
crime_2010 = pd.read_excel(f'{directory}{file_path}/2010.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index()
crime_2010["Year"] = 2010 
crime_2009 = pd.read_excel(f'{directory}{file_path}/2009.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index()
crime_2009["Year"] = 2009 
crime_2008 = pd.read_excel(f'{directory}{file_path}/2008.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index()
crime_2008["Year"] = 2008
crime_2007 = pd.read_excel(f'{directory}{file_path}/2007.xls',
                            skiprows=4, skipfooter=7, index_col=[0]).reset_index()
crime_2007["Year"] = 2007
crime_2006 = pd.read_excel(f'{directory}{file_path}/2006.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index() 
crime_2006["Year"] = 2006
crime_2005 = pd.read_excel(f'{directory}{file_path}/2005.xls',
                            skiprows=4, skipfooter=8, index_col=[0]).reset_index() 
crime_2005["Year"] = 2005

all_sheets = [crime_2024, crime_2023, crime_2022, crime_2021, crime_2020, crime_2019, crime_2018,
               crime_2017, crime_2016, crime_2015, crime_2014, crime_2013, 
               crime_2012, crime_2011, crime_2010, crime_2009, crime_2008, 
               crime_2007, crime_2006, crime_2005]
# but for all sheets we want to
for s in all_sheets:
    #get rid of line breaks in column headings
    s.columns = s.columns.str.replace('\n', ' ', regex=True)
    #remove footnote from Arson and Rape Column; rename columns that have inconsistent spacing
    s.rename(columns={'Arson1': 'Arson', 'Arson3': 'Arson', 'Arson2': 'Arson', 'Rape1':'Rape',
                       'Metropolitan/Nonmetropolitan': 'County Type', 'Larceny- theft': 'Larceny-theft',
                       'Forcible Rape': 'Rape', 'Forcible  Rape': 'Rape', 'Forcible rape': 'Rape',
                       'Motor  vehicle  theft':'Motor vehicle theft','Motor Vehicle Theft':'Motor vehicle theft',
                       'Murder and  nonnegligent  manslaughter': 'Murder and nonnegligent manslaughter', 
                       'Rape (revised  definition)1': 'Rape (revised definition)1', 
                       'Aggravated  assault': 'Aggravated assault', 'Property  crime': 'Property crime',
                       'Motor  vehicle  theft': 'Motor vehicle theft', 'Violent Crime': 'Violent crime',
                       'Property Crime': 'Property crime', 'Violent  crime':'Violent crime',
                       'Forcible  rape': 'Rape', 'Violent  Crime': 'Violent crime', 
                       'Property  Crime': 'Property crime'}, inplace=True)
    #some states and counties have footnotes at the end that will mean that they won't merge correctly
    s['County'] = s['County'].str.replace(r'\s*\d+$', '', regex=True)
    s['State'] = s['State'].str.replace(r'\s*\d+$', '', regex=True)
    #make state titlecase
    s['State'] = s['State'].str.title()

#now to split state name from county type
county_dash = [crime_2023, crime_2022, crime_2021, crime_2019, crime_2018,
               crime_2017, crime_2016, crime_2015, crime_2014, crime_2013, 
               crime_2012, crime_2011, crime_2010, crime_2009, crime_2008, 
               crime_2007, crime_2006, crime_2005]
for c in county_dash: 
    c[['State', 'County Type']] = c['State'].str.split('-', n=1, expand=True)

# In 2013-2016 states have slightly different definitions of Rape, 
# We want to combine these numbers to get total count and then drop the old columns
dif_def = [crime_2013, crime_2014, crime_2015, crime_2016]

for d in dif_def: 
    d['Rape'] = d['Rape (revised definition)1'].fillna(0) + d['Rape (legacy definition)2'].fillna(0)
    d.drop(columns=['Rape (revised definition)1','Rape (legacy definition)2'],
           inplace=True)

#for 2020 the metropolitian/not-metropolitian was a merged cell, so we need to reset index again
crime_2020['County Type'] = (crime_2020['County Type'].ffill())
crime_2020['County Type'] = crime_2020['County Type'].str.title()

#and 2008 has a weird extra column
crime_2008.drop(columns=['Unnamed: 12'], inplace=True)

# now we concatinate our list of dfs
crime_all = pd.concat(all_sheets, ignore_index=True)

#write out to derived data folder
output_path = f'{directory}/derived_data/crime_all.csv'
crime_all.to_csv(output_path, index=False)

