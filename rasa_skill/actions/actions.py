# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
#
#
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymystem3 import Mystem
import json
from random import sample

file = "data/countries3.json"


class ActionInZone(Action):
    def __init__(self):
        self.countries = json.load(open(file, "r"))
        self.m = Mystem()
        self.schengens = ["Австрия", "Бельгия", "Чешская Республика", "Дания", "Эстония", "Финляндия", "Франция",
                          "Германия", "Греция", "Венгрия", "Исландия", "Италия", "Латвия", "Литва", "Люксембург",
                          "Мальта", "Голландия", "Норвегия", "Польша", "Португалия", "Словакия", "Словения", "Испания",
                          "Швеция", "Швейцария", "Лихтенштейн"]

    def name(self) -> Text:
        return "is_schengen_zone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        country = tracker.get_slot('country')
        lemmas = self.m.lemmatize(country)
        country = lemmas[0].capitalize()
        if country in self.schengens:
            dispatcher.utter_message(text=f"{country} член шенгенской зоны")
        else:
            dispatcher.utter_message(text=f"{country} не входит в шенгенскую зону")

        return []


class ActionDocs(Action):
    def __init__(self):
        self.m = Mystem()
        self.countries = json.load(open(file, "r"))

    def name(self) -> Text:
        return "action_get_docs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        country = tracker.get_slot('country')
        lemmas = self.m.lemmatize(country)
        country = lemmas[0].capitalize()
        found = False
        for i in self.countries:
            if country == i["country"]:
                found = True
                dispatcher.utter_message(text=f"{i['documents']}")
                break

        if not found:
            dispatcher.utter_message(text=f"{country} не найдена в безе.")

        return []


class ActionInfo(Action):
    def __init__(self):
        self.m = Mystem()
        self.countries = json.load(open(file, "r"))

    def name(self) -> Text:
        return "action_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        country = tracker.get_slot('country')
        lemmas = self.m.lemmatize(country)
        country = lemmas[0].capitalize()
        found = False
        for i in self.countries:
            if country == i["country"]:
                found = True
                if not i["cost"]:
                    dispatcher.utter_message(text=f"В {i['country']} осуществляется {i['visa']}, {i['documents']}")
                else:
                    dispatcher.utter_message(
                        text=f"Для визита в {i['country']} нужна виза, {i['visa']} и стоит {i['cost']}. "
                             f"Для въезда Находиться можно до {i['days']} дней")
                break

        if not found:
            dispatcher.utter_message(text=f"{country} не найдена в безе.")

        return []


class ActionWithoutVisa(Action):
    def __init__(self):
        self.countries = json.load(open(file, "r"))

    def name(self) -> Text:
        return "action_without_visa"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        countries = []
        while len(countries) < 2:
            random_countries = sample(self.countries, 6)
            countries = [i["country"] for i in random_countries if i["visa"] == "въезд без визы"]
        dispatcher.utter_message(text=", ".join(countries))

        return []
