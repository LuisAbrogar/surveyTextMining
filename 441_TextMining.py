import csv
import requests
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import itertools

#to-do: optimize speed of run time, GUI

key="(insert subscription key)"
endpoint="https://(insert subscription name).cognitiveservices.azure.com/"
sentiment = []
phrases = []

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def sentiment_analysis(text):
    response=client.analyze_sentiment(documents=text)[0]
    sentiment.append(response.sentiment) #append overall sentiments into a list

def key_phrase_extraction(text):
    try:
        response2=client.extract_key_phrases(documents=text)[0]

        if not response2.is_error:
            phrases.append(response2.key_phrases)

        else:
            print(response2.id,response2.error)

    except exception as err:
        print("encountered exception. {}".format(err))

with open(r'c:\users\(insert User)\desktop\community-survey-open-ended-comments-2016-2017-1.csv') as database:
    data = csv.reader(database) 
    next(data) #skips the header

    count=0
    district_sentiment = {}
    sentiment_phrase = {}
    district_phrase = {}

    for row in data:
        msg=tuple([row[2]])         #converts the parsed strings into tuples
        sentiment_analysis(msg)     #textanalyticsclient functions only use tuples as arguments
        key_phrase_extraction(msg)
        count+=1

        #dictionary for sentiment analysis
        if row[1] in district_sentiment:  #makes a dictionary with the row[1]=list of districts, and the list of sentiments                          
            district_sentiment[row[1]].append(sentiment[count-1])
        else:
            district_sentiment[row[1]] = [sentiment[count-1]]

        #dictionary for key phrase extraction
        if sentiment[count-1] in sentiment_phrase:
            sentiment_phrase[sentiment[count-1]].append(phrases[count-1][:])
        else:
            sentiment_phrase[sentiment[count-1]] = [phrases[count-1][:]]
        
        if row[1] in district_phrase:
            district_phrase[row[1]].append(phrases[count-1][:])
        else:
            district_phrase[row[1]] = [phrases[count-1][:]]

        if count==200: #adjusts sample size
            break

#print(district_sentiment)
#print(sentiment_phrase)
#print(district_phrase)

#for x, y in district_sentiment.items():
#    total = y.count("negative") + y.count("mixed") + y.count("positive") + y.count("neutral")
#    print("District#" + str(x))
#    print("Percent Negative: " + str( 100 * y.count("negative") / total )  + "%")
#    print("Percent Mixed: " + str( 100 * y.count("mixed") / total )  + "%")
#    print("Percent Positive: " + str( 100 * y.count("positive") / total )  + "%")
#    print("Percent Neutral: " + str( 100 * y.count("neutral") / total )  + "%")
#    print('\n')

#user input for key phrase extraction
district_input = input("Select District #1-10: ")
sentiment_input = input("Select (positive/negative/mixed/neutral): ")
print("Key Phrases:")

listA = itertools.chain(*sentiment_phrase[sentiment_input])
listB = itertools.chain(*district_phrase[district_input])

setA = set(listA)
setB = set(listB)

setA.intersection(setB)

for item in setA.intersection(setB):
    print (item)

#making grouped bar graph for sentiment analysis
labels = []
positive = []
negative = []
mixed = []
neutral = []

for x, y in district_sentiment.items():
    total = y.count("negative") + y.count("mixed") + y.count("positive") + y.count("neutral")
    labels.append(x)
    positive.append(100 * y.count("positive") / total)
    negative.append(100 * y.count("negative") / total)
    mixed.append(100 * y.count("mixed") / total)
    neutral.append(100 * y.count("neutral") / total)

x = np.arange(len(labels))
width = 0.15

fig, ax = plt.subplots()
rects1 = ax.bar(x - 3*width/2, positive, width, label='Positive')
rects2 = ax.bar(x - width/2, negative, width, label='Negative')
rects3 = ax.bar(x + width/2, mixed, width, label='Mixed')
rects4 = ax.bar(x + 3*width/2, neutral, width, label='Neutral')

ax.set_ylabel('Percent %')
ax.set_xlabel('District #')
ax.set_title('Sentiment Analysis of Community Survey')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

#def autolabel(rects):
#    for rect in rects:
#        height = rect.get_height()
#        ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width()/2, height), xytext=(0,3), textcoords="offset points", ha='center', va='bottom')

#autolabel(rects1)
#autolabel(rects2)
#autolabel(rects3)
#autolabel(rects4)

#fig.tight_layout()

plt.show()