import csv
import requests
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

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


#def key_phrase_extraction(text):
#    try:
#        response2=client.extract_key_phrases(documents=text)[0]

#        if not response2.is_error:
#            print("\tKey Phrases:\n")
#            for phrase in response2.key_phrases:
#                print("\t\t",phrase)
#            print('\n')

#        else:
#            print(response2.id,response2.error,'\n')

#    except Exception as err:
#        print("Encountered exception. {}".format(err),'\n')


with open(r'C:\Users\(User)\(Folder)\community-survey-open-ended-comments-2016-2017-1.csv') as database:
    data = csv.reader(database) 
    next(data) #skips the header

    count=0
    district_sentiment = {}

    for row in data:
        msg=tuple([row[2]])         #converts the parsed strings into tuples
        sentiment_analysis(msg)     #textanalyticsclient functions only use tuples as arguments
        count+=1

        if row[1] in district_sentiment:  #makes a dictionary with the row[1]=list of districts, and the list of sentiments                          
            district_sentiment[row[1]].append(sentiment[count-1])
        else:
            district_sentiment[row[1]] = [sentiment[count-1]]

        if count==10: #adjusts sample size
            break

#print(district_sentiment)

#this displays the percent sentiment per district
for x, y in district_sentiment.items():
    total = y.count("negative") + y.count("mixed") + y.count("positive") + y.count("neutral")
    print("District#" + str(x))
    print("Percent Negative: " + str( 100 * y.count("negative") / total )  + "%")
    print("Percent Mixed: " + str( 100 * y.count("mixed") / total )  + "%")
    print("Percent Positive: " + str( 100 * y.count("positive") / total )  + "%")
    print("Percent Neutral: " + str( 100 * y.count("neutral") / total )  + "%")
    print('\n')