import csv
import requests
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

key="(insert subscription key)"
endpoint="https://(insert subscription name).cognitiveservices.azure.com/"
sentiment = []

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
            for phrase in response2.key_phrases:
                print(phrase)

        else:
            print(response2.id,response2.error)

    except exception as err:
        print("encountered exception. {}".format(err))


with open(r'c:\users\darren li\desktop\community-survey-open-ended-comments-2016-2017-1.csv') as database:
    data = csv.reader(database) 
    next(data) #skips the header

    count=0
    district_sentiment = {}

    print("Key Phrases:")

    for row in data:
        msg=tuple([row[2]])         #converts the parsed strings into tuples
        key_phrase_extraction(msg)
        sentiment_analysis(msg)     #textanalyticsclient functions only use tuples as arguments
        count+=1

        if row[1] in district_sentiment:  #makes a dictionary with the row[1]=list of districts, and the list of sentiments                          
            district_sentiment[row[1]].append(sentiment[count-1])
        else:
            district_sentiment[row[1]] = [sentiment[count-1]]

        if count==30: #adjusts sample size
            break

#print(district_sentiment)

#for x, y in district_sentiment.items():
#    total = y.count("negative") + y.count("mixed") + y.count("positive") + y.count("neutral")
#    print("District#" + str(x))
#    print("Percent Negative: " + str( 100 * y.count("negative") / total )  + "%")
#    print("Percent Mixed: " + str( 100 * y.count("mixed") / total )  + "%")
#    print("Percent Positive: " + str( 100 * y.count("positive") / total )  + "%")
#    print("Percent Neutral: " + str( 100 * y.count("neutral") / total )  + "%")
#    print('\n')

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
width = 0.2

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