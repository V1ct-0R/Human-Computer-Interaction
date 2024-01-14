# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai

openai.api_key = "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"


class GPTAction(Action):
    def name(self) -> Text:
        return "action_generate"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        prompt = "Can you translate the sentence: Hello, the beautiful world into Chinese for me?"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )

        generated_text = response.choices[0].text
        dispatcher.utter_message(text=prompt)
        dispatcher.utter_message(text=generated_text)

        return []


class ActionCase1(Action):
    def name(self) -> Text:
        return "action_case1"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        prompt = "I want you to simulate a virtual pet that emulates the behaviour and personality of my favourite kitten who has just passed away. Her name is Oliver, and she is a Ragdoll. She was very playful and loved playing with balls of yarn once she could reach them. Moreover, she was so affectionate that my bad moods would all go away when she lay on my knees and took a rest. Could you please describe how Oliver would act if we were in my bedroom?"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5,
        )

        generated_text = response.choices[0].text
        # dispatcher.utter_message(text=prompt)
        dispatcher.utter_message(text=generated_text)

        return []


class ActionCase2(Action):
    def name(self) -> Text:
        return "action_case2"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        prompt = "I want you to write a WeChat Moment for me. It is about a fantastic weekend I spent with my senior high school classmates in Shanghai. We were shopping on Nanjing Road Pedestrian Street and took many photos, and we also went to People's Square and visited Shanghai Museum, in which we saw many precious artifacts of historical significance. The most impressing experience was that we took a night tour on the Huangpu River and enjoyed the magnificant night scenery of the Bund. Please express in a literary way."

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.5,
        )

        generated_text = response.choices[0].text
        # dispatcher.utter_message(text=prompt)
        dispatcher.utter_message(text=generated_text)

        return []
