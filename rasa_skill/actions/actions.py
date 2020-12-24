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
        input_country = tracker.get_slot('country')
        lemmas = self.m.lemmatize(input_country)
        country = lemmas[0].capitalize()
        found = False
        for i in self.countries:
            if country == i["country"] or input_country == i["country"].lower():
                if input_country == i["country"]:
                    country = i["country"]
                found = True
                dispatcher.utter_message(text=f"{i['documents']}")
                break

        if not found:
            dispatcher.utter_message(text=f"Я не знаю такую страну '{country}'")

        return []


class ActionInfo(Action):
    def __init__(self):
        self.m = Mystem()
        self.countries = json.load(open(file, "r"))
        self.schengens = ["Австрия", "Бельгия", "Чешская Республика", "Дания", "Эстония", "Финляндия", "Франция",
                          "Германия", "Греция", "Венгрия", "Исландия", "Италия", "Латвия", "Литва", "Люксембург",
                          "Мальта", "Голландия", "Норвегия", "Польша", "Португалия", "Словакия", "Словения", "Испания",
                          "Швеция", "Швейцария", "Лихтенштейн"]

    def name(self) -> Text:
        return "action_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        input_country = tracker.get_slot('country')
        lemmas = self.m.lemmatize(input_country)
        country = "".join(lemmas).rstrip().capitalize()
        found = False
        for i in self.countries:  # шри ланка
            if country == i["country"] or input_country == i["country"].lower() or input_country == i["country"].replace('-', ' ').lower():
                if input_country == i["country"]:
                    country = i["country"]
                found = True
                if country in self.schengens:
                    button = [{"Документы на Шенген": "Документы на Шенген"}]
                    if 'images' in i:
                        images_d = {"images": []}
                        for image_id in i['images']:
                            images_d["images"].append(image_id)

                        dispatcher.utter_message(text=f"{country} входит в шенгенскую зону.", json_message=images_d,
                                                 buttons=button)
                    else:
                        dispatcher.utter_message(text=f"{country} входит в шенгенскую зону.", buttons=button)

                elif not i["cost"]:
                    if i['visa'] and i['documents']:
                        dispatcher.utter_message(text=f"{i['country']} осуществляет {i['visa']}. {i['documents']}")
                    elif i['visa']:
                        dispatcher.utter_message(text=f"{i['country']} осуществляет {i['visa']}")
                    elif i['documents']:
                        dispatcher.utter_message(text=f"{i['documents']}")
                    else:
                        dispatcher.utter_message(text=f"Мало данных о {i['country']}")
                else:
                    dispatcher.utter_message(
                        text=f"Для визита в {i['country']} нужна виза, {i['visa']} и стоит {i['cost']}. "
                             f"Находиться можно до {i['days']} дней")
                break

        if not found:
            dispatcher.utter_message(text=f"Я не знаю такую страну '{country}'")

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
        buttons = []
        while len(countries) < 3:
            random_countries = sample(self.countries, 6)
            countries = [i["country"] for i in random_countries if i["visa"] == "въезд без визы"]
            buttons.clear()
            for c in countries:
                buttons.append({c: c})
        dispatcher.utter_message(text="В " + ", ".join(countries) + " можно поехать без визы", buttons=buttons)

        return []


class ActionWrongAns(Action):
    def __init__(self):
        self.action_name = "action_wrong_ans"

    def name(self) -> Text:
        return self.action_name

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"Документы в Азербайджан": "Документы в Азербайджан"},
            {"Армения в шенгенской зоне ?": "Армения в шенгенской зоне ?"},
            {"Хочу поехать в Грецию": "Хочу поехать в Грецию"},
            {"Куда можно поехать без визы?": "Куда можно поехать без визы?"},
            {"Документы на Шенген": "Документы на Шенген"},
            {"Список стран Шенгена": "Список стран Шенгена"}
                  ]

        dispatcher.utter_message(text="Давай попробуем еще раз", buttons=buttons)
        return []
