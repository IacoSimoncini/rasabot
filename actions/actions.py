# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from datetime import date, datetime
from multiprocessing.sharedctypes import Value
from typing import Dict, Text, Any, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker

from rasa_sdk.events import AllSlotsReset

from rasa_sdk import Action

import requests

api_key = "4e648c761eb745c68f4e42ebf6d5cbee"
url_top = 'https://newsapi.org/v2/top-headlines?'
url_everything = 'https://newsapi.org/v2/everything?'
country_dict = {
    'Saudi Arabia': 'ar',
    'Germany': 'de',
    'England': 'en',
    'Spain': 'es',
    'France': 'fr',
    'Israeli': 'he',
    'Italy': 'it',
    'Holland': 'nl',
    'Norway': 'no',
    'Portugal': 'pt',
    'Russia': 'ru',
    'Sweden': 'se'
}

def general_search(lang):
    url = url_top + 'country=' + lang + '&apiKey=' + api_key
    response = requests.get(url)
    return response.json()

def search_category(cat, lang):
    cat = cat.strip()
    url = url_top + 'country=it&category=' + cat + '&apiKey=' + api_key
    response = requests.get(url)
    return response.json()

def search_news(q):
    q = q.strip()
    url = url_everything + 'q=' + q + '&apiKey=' + api_key
    response = requests.get(url)
    return response.json()

def search_news_time(q, time):
    q = q.strip()
    time = time.strip()
    url = url_everything + 'q=' + q + "from=" + time + '&apiKey=' + api_key
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

def news_source(source):
	url = url_top + 'sources=' + source
	response=requests.get(url + '&' + 'apiKey=' + api_key)
	data=response.json()
	return data

def covid():
    return requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json").json() 

class ActionCorona(Action):

    def name(self) -> Text:
        return "action_corona"

    def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            response = covid()
            reg = tracker.get_slot("region")
            reg = reg.capitalize()
            if reg == 'Trento' or reg == 'Bolzano':
                reg = "P.A. " + reg
            message = "I can't find the requested region"
            date = str(response[0]["data"]).split('T')[0]
            if "Trentino" in reg:
                tp = 0
                np = 0
                to = 0
                ti = 0
                for r in response:
                    if r["denominazione_regione"]=='P.A. Bolzano' or r["denominazione_regione"]=='P.A. Trento':
                        tp = tp + r["totale_positivi"]
                        np = np + r["nuovi_positivi"]
                        to = to + r["totale_ospedalizzati"]
                        ti = ti + r["terapia_intensiva"]
                    message = "Number of covid infected in Trentino Alto Adige :" + str(tp)+"\n" + "Today's infections: "+ str(np)+"\n"+ "Hospitalized: "+ str(to)+"\n"+ "Intensive care: "+ str(ti) + "\n" + "Last update: " + date
            else:
                for r in response:
                    if r["denominazione_regione"] == reg:
                        message = "Number of covid infected in "+ reg + ": " + str(r["totale_positivi"]) +"\n" + "Today's infections: "+ str(r["nuovi_positivi"]) +"\n"+ "Hospitalized: "+ str(r["totale_ospedalizzati"]) +"\n"+ "Intensive care: "+ str(r["terapia_intensiva"]) + "\n" + "Last update: " +  date
            dispatcher.utter_message(text=message)
        except:
            dispatcher.utter_message("Sorry: Could not get information due to an internal error")
        return [AllSlotsReset()]

class NewsBBC(Action):
    
    def name(self):
        return "action_bbc"
    
    def run(self, dispatcher, tracker, domain):
        data = news_source("bbc-news")
        for i in range(len(data)):
            text_message = data['articles'][i]['title'] + " " + data['articles'][i]['url']
            dispatcher.utter_message(text=text_message)
        return []

class NewsABC(Action):
    
    def name(self):
        return "action_abc"
    
    def run(self, dispatcher, tracker, domain):
        data = news_source("abc-news")
        for i in range(len(data)):
            text_message = data['articles'][i]['title'] + " " + data['articles'][i]['url']
            dispatcher.utter_message(text=text_message)
        return []

class NewsCNN(Action):
    
    def name(self):
        return "action_cnn"
    
    def run(self, dispatcher, tracker, domain):
        data = news_source("cnn")
        for i in range(len(data)):
            text_message = data['articles'][i]['title'] + " " + data['articles'][i]['url']
            dispatcher.utter_message(text=text_message)
        return []

class newsHeadlineIT(Action):
    def name(self):
        return "action_news_headline_it"

    def run(self, dispatcher, tracker, domain):
        try:
            data = top_headlinesIT()
            dispatcher.utter_message(text='This is what i found: ')
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
            dispatcher.utter_message(text='This is what i found: ')
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
            data = search_category(cat, lang='it')
            dispatcher.utter_message(text='This is what i found for ' + cat + ':')
            for i in range(len(data)):
                text_message = "Title: " + data['articles'][i]['title'] + "\n" + "Description: " + data['articles'][i]['description'] + "\n" + "Url: " + data['articles'][i]['url'] + "\n"
                dispatcher.utter_message(text=text_message)
        except:
            dispatcher.utter_message(text='Something went wrong')
        return []

class actionNewsCategory(Action):
    def name(self):
        return "action_form"

    def run(self, dispatcher, tracker, domain):
        try:
            q = str(tracker.get_slot('topic'))
            time = str(tracker.get_slot('time'))
            if time is None:
                data = search_news(q)
            else:
                data = search_news_time(q, time)
            dispatcher.utter_message(text='This is what i found for ' + q + ":")
            for i in range(len(data)):
                text_message = "Title: " + data['articles'][i]['title'] + "\n" + "Description: " + data['articles'][i]['description'] + "\n" + "Url: " + data['articles'][i]['url'] + "\n"
                dispatcher.utter_message(text=text_message)
        except:
            dispatcher.utter_message(text='Something went wrong')
        return [AllSlotsReset()]

class actionNewsGeneral(Action):
    def name(self):
        return "action_general"

    def run(self, dispatcher, tracker, domain):
        try:
            lang = str(tracker.get_slot('lang'))
            country = country_dict[lang]
            data = general_search(country)
            for i in range(len(data)):
                text_message = "Title: " + data['articles'][i]['title'] + "\n" + "Description: " + data['articles'][i]['description'] + "\n" + "Url: " + data['articles'][i]['url'] + "\n"
                dispatcher.utter_message(text=text_message)
        except:
            dispatcher.utter_message(text='Something went wrong')
        return [AllSlotsReset()]
