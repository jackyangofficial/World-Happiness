#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:17:16 2019

@author: Gabe
"""

from plotly.offline import plot
import pandas as pd;

url = 'https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/passport-index-matrix.csv'
df0 = pd.read_csv(url,sep=",")

## Replaced -1 with 0 for calculating freedom score
df_for_score = df0.replace(-1, 0)

## Replaced code with text
df_to_text = df0.replace(to_replace =[-1, 0, 1, 2, 3], value = ["Passport Not Required", "Visa Required", "eTA Required", "Visa on Arrial", "Visa Free"]) 

## Append a column that calculates freedom score
df_for_score.loc[:,"Freedom_Score"] = df_for_score.sum(axis=1)

## Merge the Freedom_Score column to main df. 
df = df_to_text.join(df_for_score["Freedom_Score"])

df["Rank"] = df["Freedom_Score"].rank(ascending=0)
df2 = df.copy() 
df2['Rank'] = df2['Rank'].astype(int)

dff = df2[["Passport", "Freedom_Score", "Rank"]]



#Found population data for 2018 from http://worldpopulationreview.com
popdf = pd.read_csv("https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/data.csv")
del popdf["dropdownData"]

new_df = pd.merge(popdf, dff,left_on = "name", right_on = "Passport", how = "left")
new_df.columns =["Code", "country", "Pop", "Area", "Density", "GrowthRate", "WorldPercentage", "Pop_Rank", "Passport", "Freedom_Score", "Freedom_Rank"]

new_df = new_df.drop(["Code", "Passport"], axis=1)
#new_df dataframe containing 230 countries including NaN for both Freedom_Score and Freedom_Rank
#


##https://www.kaggle.com/statchaitya/country-to-continent
#Pull out datafile that has information about both country and the continent
#Merged data set new_df to show continent for each country. Number of rows went down to 131, because some of the
#name of the country might differ from two different data set

cdf = pd.read_csv("https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/countryContinent.csv", encoding='latin-1')
con_df = cdf.filter(items= ['country', 'continent'])
mdf = new_df.merge(con_df, how = 'inner', on = ['country'])
mdf['Freedom_Score'] = mdf['Freedom_Score'].fillna(0)
mdf['Freedom_Rank'] = mdf['Freedom_Rank'].fillna(0)

mdf.tail(100)

hdf = pd.read_csv('https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/whi.csv')
hdf.columns =["Overall rank","country", "Happiness_Score", "GDP per capita", "Social support", "Healthy life expectancy", "Freedom to make life choices", "Generosity", "Perceptions of corruption"] 
hdf.head()

masterdf = mdf.merge(hdf, how = 'inner', on = ['country'])

masterdf.head()


import plotly.express as px

fig = px.scatter(masterdf, x="Happiness_Score", y="Freedom_Score", 
                 color="continent", size='GDP per capita', hover_data=['country'], trendline="ols")
fig.show()



fig = px.scatter(masterdf, x="Freedom_Score", y="Happiness_Score", color="GDP per capita",
                 size='GDP per capita', hover_data =['country'])
fig.show()

fig = px.scatter(masterdf, x="Freedom_Score", y="Happiness_Score", color="Density",
                 size='GDP per capita', hover_data =['country'])
fig.show()


fig = px.scatter(masterdf, x="Freedom_Score", y="Happiness_Score", color="Pop",
                 size='GDP per capita', hover_data =['country'])
fig.show()

plot(fig)
