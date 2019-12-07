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
    origin = request.form['country1']
    destination = request.form['country2']
    
    score_diff = (df.at[destination, "Freedom_Score"]-df.at[origin, "Freedom_Score"])
    y.append(df.at[destination, "Freedom_Score"])
    x.append(df.at[origin, "Freedom_Score"])
    
    freedom_diff = (int(df.at[origin, "Rank"])-int(df.at[destination, "Rank"]))
    x.append(1/(df.at[origin, "Rank"]))
    y.append(1/(df.at[destination, "Rank"]))
    
    growthdiff= float(countrydata.at[destination,"GrowthRate"]) -float(countrydata.at[origin,"GrowthRate"])
    
    x.append(countrydata.at[origin,"GrowthRate"])
    y.append(countrydata.at[destination,"GrowthRate"])
    
    densdiff= float(countrydata.at[destination,"GrowthRate"]) -float(countrydata.at[origin,"GrowthRate"])
    
    x.append(log(countrydata.at[origin,"PopDensity"]))
    y.append(log(countrydata.at[destination,"PopDensity"]))
    
    happydiff= float(df2.at[destination,"score"]) -float(df2.at[origin,"score"])
    
    scoremsg = ""
    freedommsg = ""
    growthmsg = ""
    densdiffmsg = ""
    happydiffmsg = ""
    resultmsg1 = ""
    resultmsg2 = ""
    
    if score_diff < 0:
        scoremsg = "You will be in a country with weaker international relationships."
    elif score_diff == 0:
        scoremsg = "You will be in a country with roughly equivalent international relationships. Your Freedom score will change by"
    else:
        scoremsg = "You will be in a country with stronger international relationships. Your Freedom score will increase by"
        
        
    if freedom_diff < 0:
        freedommsg = "As a result, your national freedom rank will be lower."
    elif freedom_diff == 0:
        freedommsg = "As a result, your national freedom rank won't be changing much."
    else:
        freedommsg = "As a result, your national freedom rank will be higher."

    if growthdiff < 0:
        growthmsg = "The country you moving to has a lower population growth rate"
    elif growthdiff >0:
        growthmsg = "The country you moving to has a higher population growth rate"
    else:
        growthmsg = "Hmm. That's strange. The two counties have exactly same population growth rate."

    densdiff= float(countrydata.at[destination,"GrowthRate"]) -float(countrydata.at[origin,"GrowthRate"])
    if densdiff < 0:
        densdiffmsg = "You can expect to have some room to breathe. The country you moving to has a lower population denstiy."
    elif densdiff == 0 :
        densdiffmsg = "You can expect exactly the amount of room you have now. "
    else:
        densdiffmsg = "You can expect to be pretty crowded. The country you moving to has a higher population denstiy."
    if happydiff < 0:
        happydiffmsg = "You can expect to be a bit more melancholy. The country you moving to has a lower World Happiness score."
    elif happydiff == 0 :
        happydiffmsg = "The happiness of both places is equal."
    else:
        happydiffmsg = "You can expect to be a bit happier, the country you moving to has a higher World Happiness score."
        
    if average_per(x,y)>.05:
        resultmsg1 = "Good for you. There seem to be some fairly substantial benefits."
    elif average_per(x,y) == 0:
        resultmsg1 = "literally the same. You picked the same country. What did you think was going to happen?" 
    else:
        resultmsg1 = "bad for you. The benefits may not be worth making the move."
        
    if df3[df3.country == destination].shape[0] < 10:
        resultmsg2 = "Actually, that's pretty low. Maybe you'll be fine."
    if df3[df3.country == destination].shape[0] == 0:
        resultmsg2 = "Wait, 0? That can't be right. FAKE NEWS!!!"

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

    
    return render_template('index.html', v1 = origin,
                                     v1a = df[origin].value_counts().to_frame(),
                                     
                                     v1b = df.at[origin, "Freedom_Score"],
                                     v1c = df.at[origin, "Rank"],
                                     v1d = countrydata.at[origin,"GrowthRate"],
                                     
                                     v2 = destination,
                                     v2a = df[origin].value_counts().to_frame(),
                                     
                                     v2b = df.at[destination, "Freedom_Score"],
                                     v2c = df.at[destination, "Rank"],
                                     v2d = countrydata.at[destination,"GrowthRate"],
                                     
                                     v3 = origin,
                                     v3a = destination,
                                     v3b = score_diff,
                                     v3c = growthdiff,
                                     v3d = densdiff,
                                     v3e = happydiff,
                                     
                                     v4b = scoremsg,
                                     v4c = growthmsg,
                                     v4d = densdiffmsg,
                                     v4e = happydiffmsg,
                                     
                                     v5 = resultmsg1,
                                     v5b = df3[df3.country == destination].shape[0],
                                     v5c = resultmsg2
                                    
                                     )
    
    
    
    
    ## return render_template('visas.html', variable7 = df_country1.to_html())

''' @app.route('/visas')
def visas():              
    return render_template('visas.html')                          
'''

@app.route('/about', methods=['GET', 'POST'])
def aboutpage():
    return render_template('about.html')

@app.route('/map', methods=['GET', 'POST'])
def worldmap():
    return render_template('map.html')

@app.route('/VISUAL2', methods=['GET', 'POST'])
def visual2():
    return render_template('VISUAL2.html')




if __name__ == '__main__':
    app.debug = True
    app.run()
