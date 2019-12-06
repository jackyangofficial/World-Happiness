from plotly.offline import plot
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

fig = go.Figure(data=go.Choropleth(
    locations = dfnew['CODE'],
    z = dfnew["Freedom_Score"],
    text = dfnew['Passport'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Freedom<br>Score',
))


fig.update_layout(
    title_text='World Travel Freedom map',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)

fig.show(renderer='colab')


plot(fig)

