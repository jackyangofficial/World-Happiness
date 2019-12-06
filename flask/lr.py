#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 21:17:34 2019

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
df_for_score.loc[:,'Freedom_Score'] = df_for_score.sum(axis=1)

## Merge the Freedom_Score column to main df. 
df = df_to_text.join(df_for_score['Freedom_Score'])

df['Rank'] = df['Freedom_Score'].rank(ascending=0)

dff= df[['Passport', 'Freedom_Score', 'Rank']]


masterdf = pd.read_csv('https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/whi.csv')
masterdf.columns =["Overall rank,","Passport", "Score", "GDP per capita", "Social support", "Healthy life expectancy", "Freedom to make life choices", "Generosity", "Perceptions of corruption"] 

m_df = masterdf.merge(dff, how = 'inner', on = ['Passport'])

#Renaming the column
m_df.rename(columns = {"Overall rank,":"Happiness_rank","Passport":"country", 
                       "Score":"Happiness_Score", "GDP per capita":"GDP", 
                       "Social support":"Social_Support", "Healthy life expectancy":"Health", 
                       "Freedom to make life choices":"Freedom_Choice", "Generosity":"Genorosity", 
                       "Perceptions of corruption":"Corruption", "Freedom_Score":"Freedom_Score", 
                       "Rank":"Freedom_Rank"}, inplace = True )

#Pull out datafile that has information about both country and the continent
url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
continents = pd.read_csv(url)

con_df = continents.filter(items= ['country', 'continent'])
u_df = con_df.drop_duplicates(['country', 'continent'])
mdf = m_df.merge(u_df, how = 'inner', on = ['country'])




#from __future__ import print_function
import numpy as np
import pandas as pd

from bokeh.util.browser import view
from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.layouts import column, gridplot
from bokeh.models import Circle, ColumnDataSource, Div, Grid, Line, LinearAxis, Plot, Range1d
from bokeh.resources import INLINE


raw = mdf[['GDP','Social_Support', 'Health', 'Freedom_Choice', 'Genorosity', 'Corruption']]


Hexadecimal = pd.DataFrame(data=raw, columns=
                       ['GDP','Social_Support', 'Health', 'Freedom_Choice', 'Genorosity', 'Corruption'])


circles_source = ColumnDataSource(
    data = dict(
        xi   = Hexadecimal['GDP'],
        yi   = mdf['Freedom_Score'],
        xii  = Hexadecimal['Social_Support'],
        xiii = Hexadecimal['Health'],
        xiv  = Hexadecimal['Freedom_Choice'],
        xV   = Hexadecimal['Genorosity'],
        xVI  = Hexadecimal['Corruption']
    )
   )

x = np.linspace(-0.5, 2, 1)
y = 3 + 0.5 * x
lines_source = ColumnDataSource(data=dict(x=x, y=y))

xdr = Range1d(start=-0.5, end=2)
ydr = Range1d(start=-100, end=600)

def make_plot(title, xname, yname):
    
    plot = Plot(x_range=xdr, y_range=ydr, plot_width=400, plot_height=400,
                background_fill_color='#efefef')
    plot.title.text = title

    xaxis = LinearAxis(axis_line_color=None)
    plot.add_layout(xaxis, 'below')

    yaxis = LinearAxis(axis_line_color=None)
    plot.add_layout(yaxis, 'left')

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

    line = Line(x='x', y='y', line_color="#666699", line_width=2)
    plot.add_glyph(lines_source, line)

    circle = Circle(
        x=xname, y=yname, size=12,
        fill_color="#cc6633", line_color="#cc6633", fill_alpha=0.5
    )
    plot.add_glyph(circles_source, circle)
    return plot

#where will this comment show up
GDP   = make_plot('GDP',   'xi',   'yi')
Social_Support  = make_plot('Social_Support',  'xii',  'yi')
Health = make_plot('Health', 'xiii', 'yi')
Freedom_Choice  = make_plot('Freedom_Choice',  'xiv',  'yi')
Genorosity   = make_plot('Genorosity',   'xV',   'yi')
Corruption  = make_plot('Corruption',   'xVI',   'yi')
grid = gridplot([ [GDP, Social_Support, Health], [Freedom_Choice, Genorosity, Corruption] ], toolbar_location=None)
div = Div(text=
"""
<h1>Indicators with Freedom Score</h1>
<p>This shows the collection of six indicators have nearly
correlated with Happiness Score. (GDP, Social_Support, Health, Freedom_Choice, Genorosity, Corruption)
</p>
""" )

doc = Document()
doc.add_root(column(div, grid, sizing_mode="scale_width"))

if __name__ == "__main__":
    doc.validate()
    filename = "indicator.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Indicators with Happiness Score"))
    print("Wrote %s" % filename)
    view(filename)
    
    
    
    
import plotly.express as px

fig = px.scatter(mdf, x="Happiness_Score", y="Freedom_Score", 
                 color="continent", size='GDP', hover_data=['country'], trendline="ols")
fig.show()



fig = px.scatter(mdf, x="Freedom_Score", y="Happiness_Score", color="GDP",#"Health, Social_Support",
                 size='Freedom_Score', hover_data =['country'])
fig.show()

plot(fig)