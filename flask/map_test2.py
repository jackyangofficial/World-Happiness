#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 01:30:01 2019

@author: Gabe
"""
"""
import pandas as pd;
import plotly.graph_objects as go;


url = 'https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/passport-index-matrix.csv'
df0 = pd.read_csv(url,sep=",")

## Replaced -1 with 0 for calculating freedom score
df_for_score = df0.replace(-1, 0)

## Replaced code with text

''' 
| Code | Explanation |
|---|---|
|3| visa-free travel|
|2| visa on arrival|
|1| eTA (electronic travel authority) required|
|0| visa required|
|-1| where passport=destination|

'''

df_to_text = df0.replace(to_replace =[-1, 0, 1, 2, 3], value = ["Passport Not Required", "Visa Required", "eTA Required", "Visa on Arrial", "Visa Free"]) 

## Append a column that calculates freedom score
df_for_score.loc[:,'Freedom_Score'] = df_for_score.sum(axis=1)

## Merge the Freedom_Score column to main df. 
df = df_to_text.join(df_for_score['Freedom_Score'])

df['Rank'] = df['Freedom_Score'].rank(ascending=0)


countriescode =pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
countriescode.columns =["Passport","GDP","CODE"]
countriescode.set_index("Passport",drop=False)

dfnew = df.merge(countriescode, on="Passport",how="inner").fillna(0)
"""

from plotly.offline import plot

import plotly.graph_objects as go;

coorddf =pd.read_csv('https://raw.githubusercontent.com/wgygabriel/wgy/9d4ee2ceb25591696522f706d56402f5cf3c1281/coordforcountry.csv')
coorddf = coorddf.set_index("country")


coorddf.head()

country = "Brazil"
country2= "China"


fig = go.Figure(data=go.Scattergeo(
    lat = [coorddf.at[country,'latitude'], coorddf.at[country2,'latitude'] ],
    lon = [coorddf.at[country,'longitude'], coorddf.at[country2,'longitude'] ],
    text = [country, country2],
    mode = 'lines',
    line = dict(width = 1.5, color = 'red'),

    
))




fig.update_layout(
    title_text = country + " to " + country2,
    showlegend = False,
    geo = dict(
        resolution = 50,
        showland = True,
        showlakes = True,

        projection_type = "natural earth", 
        coastlinewidth = 2,
        lataxis = dict(
            range = [-100, 100],
            showgrid = True,
            dtick = 10
        ),
        lonaxis = dict(
            range = [-100, 100],
            showgrid = True,
            dtick = 20
        ),
    )
)
        
fig.show()

plot(fig)