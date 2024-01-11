from math import trunc
from flask import Flask, render_template, request, redirect, url_for
# The below handles some deprecated dependencies in Python > 3.10 that Flask Navigation needs
import collections
collections.MutableSequence = collections.abc.MutableSequence
collections.Iterable = collections.abc.Iterable
from flask_navigation import Navigation
# Import Azure SQL helper code
import requests
from azuresqlconnector import *
import json
import re


app = Flask(__name__)
nav = Navigation(app)

nav.Bar ('top', [
    nav.Item('Home','index'),
    nav.Item('Results table', 'table')
])


@app.route('/') 
def index():
    return render_template('form-example-home.html')

@app.route('/form') 
def form():
    return render_template('form.html')


@app.route('/form_submit', methods=['POST']) 
def form_submit():
    api_key = 'your_api_key'
    endpoint_url = 'your_azure_endpoint'
    api_endpoint = f"{endpoint_url}language/:analyze-text?api-version=2023-04-15-preview"

    headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': api_key,
    }

    form_data1 = request.form['text1']

    print("Submitting data:")
    print('Text 1: ', form_data1)

    # Create the request payload
# Create the request payload
    payload = {
        "kind": "SentimentAnalysis",
        "parameters": {
            "modelVersion": "latest",
            "opinionMining": "true"
        },
        "analysisInput": {
            "documents": [
                {
                    "id": "1",
                    "language": "en",
                    "text": form_data1
                }
            ]
        }
    }


    response = requests.post(api_endpoint, headers=headers, json=payload) #this is the response code

    


# Check the status code
    if response.status_code == 200:
        # Successful response
        result = response.json()
    else:
        # Error handling
        print(f"Error: {response.status_code}")

    #extract the important data from the json response
    important_data =(result['results'])['documents']
    overall_sentiment = (important_data[0])['sentiment']
    positive= (important_data[0])['confidenceScores']['positive']
    negative = (important_data[0])['confidenceScores']['negative']
    neutral = (important_data[0])['confidenceScores']['neutral']
    stri =  "The overall sentiment of this text is " + overall_sentiment + "." " The text contains a " + str(positive)  + " positive score, a " + str(negative) + " negative score, and a " + str(neutral) + " neutral score."

    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()
  

    sql_query = f"""
        INSERT INTO CognitiveServices.ExampleTable
        VALUES (
         '{form_data1}',
         '{stri}'
         );
        """

    cursor.execute(sql_query)

    print("Data submitted. . .")

    # IMPORTANT: The connection must commit the changes.
    conn.commit()

    print("Changes commited.")

    cursor.close()

    print("Redirecting. . .")

    # Redirect back to form page after the form is submitted
    return redirect(url_for('table'))



@app.route('/table') 
def table():

    # Initialize SQL connection
    conn = SQLConnection()
    conn = conn.getConnection()
    cursor = conn.cursor()

    sql_query = f"""
        SELECT * FROM CognitiveServices.ExampleTable;
        """

    cursor.execute(sql_query)

    records = cursor.fetchall()

    cursor.close()

    return render_template('table.html', records=records)
