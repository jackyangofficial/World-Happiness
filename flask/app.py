#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 00:20:41 2019

@author: jy
"""

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index():
    import pandas as pd
    
    ## read the file
    url = 'https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/passport-index-matrix.csv'
    df0 = pd.read_csv(url,sep=",")
    
    ## set index for the matrix
    df1 = df0.set_index("Passport", drop = False)
    
    ## Replaced -1 with 0 for calculating freedom score
    df_for_score = df1.replace(-1, 0)
    
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
    
    df_to_text = df1.replace(to_replace =[-1, 0, 1, 2, 3], value = ["Passport Not Required", "Visa Required", "eTA Required", "Visa on Arrial", "Visa Free"]) 
    
    ## Append a column that calculates freedom score
    df_for_score.loc[:,'Freedom_Score'] = df_for_score.sum(axis=1)
    
    ## Merge the Freedom_Score column to main df. 
    df = df_to_text.join(df_for_score['Freedom_Score'])
    
    df['Rank'] = df['Freedom_Score'].rank(ascending=0)
    
    country = request.form['country']
    
    print("Passport Index:")
    print("-----------------------------------")
    print(df[country].value_counts())
    print("-----------------------------------")
    print("Travel Freedom Score:", df.at[country, "Freedom_Score"])
    print("Travel Freedom Rank:", int(df.at[country, "Rank"]))
    print("-----------------------------------")
    
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
    text_file = open("templates/visas.html", "w")
    text_file.write(df_country1.to_html())
    text_file.close()
    '''
    
    return render_template('index.html', variable1= country,
                                         variable2 = df[country].value_counts(),
                                         variable3 = df.at[country, "Freedom_Score"],
                                         variable4 = int(df.at[country, "Rank"]),
                                         variable5a = df_rank_min["Passport"],
                                         variable5b = int(df_rank_min["Rank"]),
                                         variable6a = df_rank_max["Passport"],
                                         variable6b = int(df_rank_max["Rank"]))
    
    
    ## return render_template('visas.html', variable7 = df_country1.to_html())
'''                                         
@app.route('/visas.html')
def visas():              
    return render_template('visas.html')                          
'''

if __name__ == '__main__':
    app.debug = True
    app.run()
