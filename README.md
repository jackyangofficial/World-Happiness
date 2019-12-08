# CIS9650-ProjectDemo

## World Happiness is a web app created using Flask and written in python

## The app is running on Python Anywhere server

## Web App link: http://jackjoeng.pythonanywhere.com/


**Team members:** 
Shane Ayers, Michael Ramlochan, Thomas Thomas, Gabriel Whang, Jack Yang

**Problem Statement:**

Whether the reasons are economic, political, or recreational, globalization has made migration between countries more accessible than ever before. Say you are an individual looking to relocate to another country. What would you want to know? What factors will help to make the decision to relocate, and where? There are many resources already available that discuss commonly known information about countries, such as Gross Domestic Product, unusual or uniquely oppressive local laws, and current state of the government. What is not usually represented is other relevant information about conditions on the ground. Are people happy there? Is the population growing? Is it a place with a lot of people already? Is it peaceful? Our project sets out to supply that information and an analysis of whether it is a good idea for the user to migrate from one country to another based on these factors. 


**Data Sets:**

World Happiness Data – This came from the World Happiness Report, a global initiative to evaluate and rank the Happiness of each country in the world. 

https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/whi.csv

Passport Index Data – This data was compiled from passportindex.org, a site which collects and displays data regarding travel rules between countries. 

https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/passport-index-matrix.csv

Crisis Data – This data is an excerpt of a much larger database on global conflicts that is updated regularly. It is sourced from The Armed Conflict Location & Event Data Project (ACLED). That is a project to aggregate and conflict events, analysis and mapping. 

https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/crisis.csv

World Population Data – This data is from a website called World Population Review, which aggregates and displays data originally sourced from the United Nations report on World Population Prospects.

https://raw.githubusercontent.com/jackjoeng/CIS9650-JACK/master/data.csv

**Types of Analysis:**

To begin, we calculate a freedom score for each country based on travel restrictions between it and each other country in the data set. We ordinate the different conditions placed on travel and calculate the score from those. For example, a country offering another country Free Visas may count as a 3, or the highest rank of freedom between the two countries, while a 0 may represent completely restricted travel, regardless of presented documents. Following that, we ranked the countries based on the calculated score.

The freedom score and ranking became the index against all of our other data sets were referenced, using the names of countries as the criteria. We did comparison between referenced values from other data sets, such as the World Happiness Data and World Population Data, to generate summary statistics of the differences between living conditions in those countries. We then evaluate the average magnitude of the difference to come up with a standard recommendation about whether or not a person should move from one place to the other.

To conclude, we aggregated crisis data about the target country to present a summary statistic regarding it.

**Running the App in Local:**


1. Git clone the repository 

2. In your terminal, run:
```
$ pip install Flask
```
3. Navigate to Flask folder

4. Run:

``` 
python app.py
```
5. Open in your web browser:
```
http://127.0.0.1:5000/
```


Baruch College CIS9650 Copy Right 2019

