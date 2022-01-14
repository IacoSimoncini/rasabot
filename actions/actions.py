# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk import Action
from rasa.core.actions.forms import FormAction

import requests

api_key = "4e648c761eb745c68f4e42ebf6d5cbee"
url_top = 'https://newsapi.org/v2/top-headlines?'
url_everything = 'https://newsapi.org/v2/everything?'

def search_category(cat):
    cat = cat.strip()
    url = url_top + 'country=it&' + 'category=' + cat + '&apiKey=' + api_key
    response = requests.get(url)
    return response.json()

def search_news(q):
    url = url_everything + 'q=' + q + '&apiKey=' + api_key
    response = requests.get(url)
    return response.json()

def top_headlinesIT():
    url = url_top + 'country=it&apiKey=' + api_key
    response = requests.get(url)
    return response.json()

def top_headlinesUS():
    url = url_top + 'country=us&apiKey=' + api_key
    response = requests.get(url)
    return response.json()

class newsHeadlineIT(Action):
    def name(self):
        return "action_news_headline_it"

    def run(self, dispatcher, tracker, domain):
        try:
            data = top_headlinesIT()
            for i in range(len(data)):
                text_message = data['articles'][i]['title'] + " " + data['articles'][i]['url']
                dispatcher.utter_message(text=text_message)
        except:
            dispatcher.utter_message(text='Something went wrong')
        return []

class newsHeadlineUS(Action):
    def name(self):
        return "action_news_headline_us"

    def run(self, dispatcher, tracker, domain):
        try:   
            data = top_headlinesUS()
            for i in range(len(data)):
                text_message = data['articles'][i]['title'] + data['articles'][i]['url']
                dispatcher.utter_message(text=text_message)
        except:
            dispatcher.utter_message(text='Something went wrong')
        return []

class actionNewsCategory(Action):
    def name(self):
        return "action_category"

    def run(self, dispatcher, tracker, domain):
        try:
            cat = str(tracker.get_slot('category'))
            data = search_category(cat)
            for i in range(len(data)):
                text_message = "Title: " + data['articles'][i]['title'] + "\n" + "Description: " + data['articles'][i]['description'] + "\n" + "Url: " + data['articles'][i]['url'] + "\n"
                dispatcher.utter_message(text=text_message)
        except:
            dispatcher.utter_message(text='Something went wrong')
        return []
