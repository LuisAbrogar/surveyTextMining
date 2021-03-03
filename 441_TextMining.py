import csv
import requests
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Author: Darren Li
# so what we want is to show the sentiment analysis and key phrase extraction of a whole sample size
# ie: for five responses, just show a single average sentiment score of all five responses, instead of individual scores for each
# for key phrase extraction, lemmatize the words to their roots and only print out lemmatized phrases that were used the most in the whole document
# as for the amount of API calls, just go as high as 100 for the sample size, if its accurate for 100 samples, its prob good for 3000 so dont drain your credit card
# don't worry about 3000 being too much for the client that would use this b/c they only really need to use this once at a time

key="(insert subscription key)"
endpoint="https://(insert subscription name).cognitiveservices.azure.com/"

def authenticate_client():    
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()


def sentiment_analysis(text):
    response=client.analyze_sentiment(documents=text)[0]
    print("\tResponse Sentiment: {}".format(response.sentiment))
    print("\tOverall scores:\n \tpositive={0:.2f}\n \tneutral={1:.2f}\n \tnegative={2:.2f} \n".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))
    print('\n')


def key_phrase_extraction(text):
    try:
        response2=client.extract_key_phrases(documents=text)[0]

        if not response2.is_error:
            print("\tKey Phrases:\n")
            for phrase in response2.key_phrases:
                print("\t\t",phrase)
            print('\n')

        else:
            print(response2.id,response2.error,'\n')

    except Exception as err:
        print("Encountered exception. {}".format(err),'\n')


with open(r'C:\Users\(User)\(Folder)\community-survey-open-ended-comments-2016-2017-1.csv') as database:
    data = csv.reader(database) 
    next(data)                      #Skips the header

    j=0

    for row in data:
        #print('Survey Response [',j+1,']:\n',row[2],'\n')
        msg=tuple([row[2]])         #Converts the parsed strings into tuples

        sentiment_analysis(msg)     #TextAnalyticsClient functions only use tuples as arguments
        key_phrase_extraction(msg)

        j+=1

        if j==3:
            break

