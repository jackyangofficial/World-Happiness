#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 00:20:41 2019
@author: jy
"""
'''
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index():
'''
def perc_change (x,y):
    return ((y-x)/x)
def average_per(x,y):
    sumi=[]
    for i,j in zip(x,y):
        sumi.append(perc_change(i,j))
    return (sum(sumi)/len(sumi))*100
    
import pandas as pd
from math import log 
countrydata =pd.read_csv("https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/data.csv")
## read the file
url = 'https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/passport-index-matrix.csv'
df0 = pd.read_csv(url,sep=",")
del countrydata["dropdownData"]
countrydata.columns = ["Code","Passport","Population","Area","PopDensity","GrowthRate","PopPerc","PopRank"]

## set index for the matrix
#df1 = df0.set_index("Passport", drop = False)

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

url = 'https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/whi.csv'
df2 = pd.read_csv(url,sep=",")
df2.columns = df2.columns.str.strip().str.lower().str.replace(' ', '').str.replace('"','').str.replace('(', '').str.replace('ï»¿','').str.replace(')', '')
df2 = df2.set_index("countryorregion")
csv_file = 'https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/crisis.csv'
df3 = pd.read_csv(csv_file)


df['Rank'] = df['Freedom_Score'].rank(ascending=0)
df = df.set_index("Passport")
countrydata = countrydata.set_index("Passport")
x=[]
y=[]
#country = request.form['country']
origin = "India"
destination= "Israel"

if origin == destination:
    print("So you want to leave",origin,"and go to...", destination,"\n","Okay. Sure. Have it your way.")
    print("Here's some data about the country that you're leaving data:")
    print("Passport Index:")
    print("-----------------------------------")
    print("International relationships by way of travel rules")
    print(df[origin].value_counts().to_frame())
    print("-----------------------------------")
    print("Travel Freedom Score:", df.at[origin, "Freedom_Score"])
    print("Travel Freedom Rank:", int(df.at[origin, "Rank"]))
    print("Growth rate:",countrydata.at[origin,"GrowthRate"])
    print("-----------------------------------")
    
    print("Here's some information about the country you're considering moving to:")
    print("-----------------------------------")
    print("International relationships by way of travel rules")
    print(df[destination].value_counts().to_frame())
    print("-----------------------------------")
    print("Moving from",origin,"to",destination,"will have the following impacts:")
    print("\n")
    score_diff = (df.at[destination, "Freedom_Score"]-df.at[origin, "Freedom_Score"])
    y.append(df.at[destination, "Freedom_Score"])
    x.append(df.at[origin, "Freedom_Score"])
    if score_diff < 0:
        print("You will be in a country with weaker international relationships. Your Freedom score will decrease by", abs(score_diff),".")
    elif score_diff == 0:
        print("You will be in a country with roughly equivalent international relationships. Your Freedom score will change by", abs(score_diff),".")
    else:
        print("You will be in a country with stronger international relationships. Your Freedom score will increase by", abs(score_diff),".")
    print("\n")
    freedom_diff = (int(df.at[origin, "Rank"])-int(df.at[destination, "Rank"]))
    if freedom_diff < 0:
        print("As a result, your national freedom rank will be lower. Your Freedom Ranking moves down by", abs(freedom_diff))
    elif freedom_diff == 0:
        print("As a result, your national freedom rank won't be changing much. Your Freedom Ranking will change by", abs(freedom_diff))
    else:
        print("As a result, your national freedom rank will be higher. Your Freedom Ranking will move up by", abs(freedom_diff))
    x.append(1/(df.at[origin, "Rank"]))
    y.append(1/(df.at[destination, "Rank"]))
    print("\n")
    growthdiff= float(countrydata.at[destination,"GrowthRate"]) -float(countrydata.at[origin,"GrowthRate"])
    if growthdiff < 0:
        print(destination,"has a population growth rate lower than ",origin,"by", abs(growthdiff), "points")
    elif growthdiff >0:
        print(destination,"has a population growth rate higher than ",origin,"by", abs(growthdiff), "points")
    else:
        print("Hmm. That's strange.", destination,"has a population growth rate exactly equal to",origin)
    x.append(countrydata.at[origin,"GrowthRate"])
    y.append(countrydata.at[destination,"GrowthRate"])
    print("\n")
    densdiff= float(countrydata.at[destination,"GrowthRate"]) -float(countrydata.at[origin,"GrowthRate"])
    if densdiff < 0:
        print("You can expect to have some room to breathe.", destination,"has a population denstiy lower than ",origin)
    elif densdiff == 0 :
        print("You can expect exactly the amount of room you have now. The population density is the same.")
    else:
        print("You can expect to be pretty crowded.", destination,"has a population density higher than ",origin)
    print("\n")
    x.append(log(countrydata.at[origin,"PopDensity"]))
    y.append(log(countrydata.at[destination,"PopDensity"]))
    happydiff= float(df2.at[destination,"score"]) -float(df2.at[origin,"score"])
    if happydiff < 0:
        print("You can expect to be a bit more melancholy.", destination,"has a World Happiness score lower than",origin, "by",happydiff,"points.")
    elif happydiff == 0 :
        print("The happiness of both places is equal.")
    else:
        print("You can expect to be a bit happier", destination,"has a World Happiness score  higher than ",origin, "by",happydiff,"points.")
    
    
    #print(x)
    #print(y)
    #print(origin,": ",countrydata.at[origin,"GrowthRate"])
    #print(destination,": ",countrydata.at[destination,"GrowthRate"])
    print("\n")
    print("Ultimately, based on factors such as Happiness, Growth, Population Density, Travel Freedom, and others, we predict that moving from",origin,"to",destination,"may end up being...")
    if average_per(x,y)>.05:
        print("good for you. There seem to be some fairly substantial benefits.")
    elif average_per(x,y) == 0:
        print("literally the same. You picked the same country. What did you think was going to happen?" )
    else:
        print("bad for you. The benefits may not be worth making the move.")
    
    
    print("However, statistics aren't everything. Some things are more important than World Happiness or GDP.")
    print("In the last month, there have been", df3[df3.country == destination].shape[0], "acts of violence in the country you're considering moving to. These include riots, protests, explosions and battles.")
    if df3[df3.country == destination].shape[0] < 10:
        print("Actually, that's pretty low. Maybe you'll be fine.")
    if df3[df3.country == destination].shape[0] == 0:
        print("Wait, 0? That can't be right. FAKE NEWS!!!")
    print("")
    print("-----------------------------------")
'''
## Rank country by its freedom score
df_rank_max = df.nlargest(1, "Rank").iloc[0]
df_rank_min = df.nsmallest(1, "Rank").iloc[0]

print("-----------------------------------")
print("Country that has lowest freedom score:")
print(df_rank_max["Passport"], "| Rank:", int(df_rank_max["Rank"]))

print("-----------------------------------")
print("Country that has highest freedom score:")
print(df_rank_min["Passport"], "| Rank:", int(df_rank_min["Rank"]))

## Print the visa requirements for the country to html
print("See the html...")
df_country0 = df.loc[country, : ]
df_country1 = df_country0.to_frame()
'''
'''
text_file = open("templates/visas.html", "w")
text_file.write(df_country1.to_html())
text_file.close()
'''

'''
return render_template('index.html', v1= country1,
                                     v1a = df[origin].value_counts().to_frame(),
                                     
                                     v1b = df.at[origin, "Freedom_Score"],
                                     v1c = int(df.at[origin, "Rank"],
                                     v1d = countrydata.at[origin,"GrowthRate"],
                                     
                                     v2= country2,
                                     v2a = df[origin].value_counts().to_frame(),
                                     
                                     v2b = df.at[destination, "Freedom_Score"],
                                     v2c = int(df.at[destination, "Rank"],
                                     v2d = countrydata.at[destination,"GrowthRate"])
'''
'''

## return render_template('visas.html', variable7 = df_country1.to_html())
'''
''' @app.route('/visas')
def visas():              
    return render_template('visas.html')                          
'''
'''
@app.route('/map', methods=['GET', 'POST'])
def map():
    return render_template('temp-plot.html')


if __name__ == '__main__':
    app.debug = True
    app.run()'''