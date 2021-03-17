#API ----------------------------------------------------------------------------------------
import requests
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

#Parsing ----------------------------------------------------------------------------------------
import nltk
import csv
import nltk.corpus
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

#GUI ----------------------------------------------------------------------------------------
#import PySimpleGUI as gui
#layout = [[gui.Text("SurveyTextMiner")], [gui.Button("Next")]]
#page2 = [[gui.Text("Page 2")], [gui.Button("OK")]]

#window = gui.Window("Demo", layout)

#while True:
    #event, values = window.read()
    #if event == "Next":
        #window = gui.Window("Demo", page2)
        #event, values = window.read()
    #if event == "OK" or event == gui.WIN_CLOSED:
        #break

#window.close()


#API Info ----------------------------------------------------------------------------------------
with open("user.txt", "r") as file:
    key = file.readline()
    key = key.replace('\n','')
    endpoint = file.readline()

#Main Program ----------------------------------------------------------------------------------------
#Text Mining of Survey Data Using Python
#input: .csv file of survey
#output: total sentiment score (overall sentiment) and top used phrases

#Member Variables ----------------------------------------------------------------------------------------
total_responses_negative = 0
total_responses_mixed = 0
total_responses_positive = 0



def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    ta_client = TextAnalyticsClient(endpoint = endpoint, credential = ta_credential)
    return ta_client

#totals overall sentiment
def sentiment_analysis(text):
    response = client.analyze_sentiment(documents = text)[0]
    if(response.sentiment == "positive"):
        global total_responses_positive
        total_responses_positive += 1
    if(response.sentiment == "mixed"):
        global total_responses_mixed
        total_responses_mixed += 1
    if(response.sentiment == "negative"):
        global total_responses_negative
        total_responses_negative += 1

   
testAmount = 5                      #variable for testing

client = authenticate_client()

with open("commsurvey.csv", "r") as database:
    data = csv.reader(database)
    next(data)

    counter = 0

    for row in data:
        msg = tuple([row[2]])
        sentiment_analysis(msg)
        counter +=1
        
        if counter == testAmount:       #test stop cond
            break

    print("Total Positive: {:.2f} %".format(total_responses_positive / counter * 100))
    print("\nTotal Mixed: {:.2f} %".format(total_responses_mixed / counter * 100))
    print("\nTotal Negative: {:.2f} %".format(total_responses_negative / counter * 100))
        