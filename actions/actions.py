# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from unittest import result
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import re

class ValidateInformationForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_information_form"

    @staticmethod
    def concerts_db() -> List[Text]:
        """Database of supported concerts."""

        return [
            "big arena",
            "rock cellar",
        ]
    @staticmethod
    def ticket_type_db() -> List[Text]:
        """Database of supported concerts."""

        return [
            "first",
            "second",
            "third",
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False
    @staticmethod
    def is_email(string: Text) -> bool:
        """Check if a string is valid email address."""
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        if(re.search(regex,string)): 
            return True
        else:
            return False;
        

    def validate_concertname(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate concertname value."""

        if value.lower() in self.concerts_db():
            # validation succeeded, set the value of the "concert" slot to value
             if tracker.get_slot("name") is None:
                dispatcher.utter_message(text="Your name?")
                return {"concertname": value}
             if tracker.get_slot("email") is None:
                dispatcher.utter_message(text="Your email?")
                return {"concertname": value}
             if tracker.get_slot("ticket_type") is None:
                dispatcher.utter_message(text="seat type?")
                if tracker.get_slot("concertname") == "big arena":
                    dispatcher.utter_message(text="1 first-class seats, 4 second-class seats, 4 third-class seats\nwhich seat you want to reserve?")
                    return []
                if tracker.get_slot("concertname") == "rock cellar":
                    dispatcher.utter_message(text="4 first-class seats, 5 second-class seats, 6 third-class seats\nwhich seat you want to reserve?")
                    return []
                return {"concertname": value}
        else:
            dispatcher.utter_message(response="utter_wrong_concertname")
            dispatcher.utter_message(text="We have following concerts")
            for concert in self.concerts_db():
                dispatcher.utter_message(text=concert)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"concertname": None}


    def validate_ticket_type(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate concertname value."""

        if value.lower() in self.ticket_type_db():
            # validation succeeded, set the value of the "ticket_type" slot to value
             if tracker.get_slot("name") is None:
                dispatcher.utter_message(text="Your name?")
                return {"ticket_type": value}
             if tracker.get_slot("email") is None:
                dispatcher.utter_message(text="Your email?")
                return {"ticket_type": value}
             if tracker.get_slot("concertname") is None:
                dispatcher.utter_message(text="which concert you want to reverse?")
                return {"ticket_type": value}
        else:
            dispatcher.utter_message(response="utter_unvalid_ticket_type")
            dispatcher.utter_message(text="We have following type of seats")
            for type in self.ticket_type_db():
                dispatcher.utter_message(text=type)
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"ticket_type": None}

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate email value."""

        if self.is_email(value):
            if tracker.get_slot("name") is None:
                dispatcher.utter_message(text="Your name?")
                return {"email": value}
            if tracker.get_slot("concertname") is None:
                dispatcher.utter_message(text="which concert you want to reverse?")
                return {"email": value}
            if tracker.get_slot("ticket_type") is None:
                dispatcher.utter_message(text="seat type?")
                if tracker.get_slot("concertname") == "big arena":
                    dispatcher.utter_message(text="1 first-class seats, 4 second-class seats, 4 third-class seats\nwhich seat you want to reserve?")
                    return {"email": value}
                if tracker.get_slot("concertname") == "rock cellar":
                    dispatcher.utter_message(text="4 first-class seats, 5 second-class seats, 6 third-class seats\nwhich seat you want to reserve?")
                    return {"email": value}
                return {"email": value}
        else:
            dispatcher.utter_message(response="utter_unvalid_email")
            # validation failed, set slot to None
            return {"email": None}

    def validate_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate name value."""
        if value is None:
            return {"name":None}
        if tracker.get_slot("email") is None:
            dispatcher.utter_message(text="Corret name and what's your email?")
            return {"name": value}
        if tracker.get_slot("concertname") is None:
            dispatcher.utter_message(text="Corret name and which concert you want to reverse?")
            return {"name": value}
        if tracker.get_slot("ticket_type") is None:
            dispatcher.utter_message(text="seat type?")
            if tracker.get_slot("concertname") == "big arena":
                dispatcher.utter_message(text="1 first-class seats, 4 second-class seats, 4 third-class seats\nwhich seat you want to reserve?")
                return {"name": value}
            if tracker.get_slot("concertname") == "rock cellar":
                dispatcher.utter_message(text="4 first-class seats, 5 second-class seats, 6 third-class seats\nwhich seat you want to reserve?")
                return {"name": value}
            return {"name": value}



class ActionSearchConcerts(Action):
    def name(self):
        return "action_search_concerts"

    def run(self, dispatcher, tracker, domain):
        concerts = [
            {"artist": "Foo Fighters", "reviews": 4.5},
            {"artist": "Katy Perry", "reviews": 5.0},
        ]
        description = ", ".join([c["artist"] for c in concerts])
        dispatcher.utter_message(text=f"{description}")
        return [SlotSet("concerts", concerts)]


class ActionSearchVenues(Action):
    def name(self):
        return "action_search_venues"

    def run(self, dispatcher, tracker, domain):
        venues = [
            {"name": "Big Arena", "reviews": 4.5},
            {"name": "Rock Cellar", "reviews": 5.0},
        ]
        dispatcher.utter_message(text="here are some venues I found")
        description = ", ".join([c["name"] for c in venues])
        dispatcher.utter_message(text=f"{description}")
        return [SlotSet("venues", venues)]


class ActionShowConcertReviews(Action):
    def name(self):
        return "action_show_concert_reviews"

    def run(self, dispatcher, tracker, domain):
        concerts = tracker.get_slot("concerts")
        dispatcher.utter_message(text=f"concerts: {concerts}")
        return []


class ActionShowVenueReviews(Action):
    def name(self):
        return "action_show_venue_reviews"

    def run(self, dispatcher, tracker, domain):
        venues = tracker.get_slot("venues")
        dispatcher.utter_message(text=f"venues: {venues}")
        return []


class ActionSetMusicPreference(Action):
    def name(self):
        return "action_set_music_preference"

    def run(self, dispatcher, tracker, domain):
        """Sets the slot 'likes_music' to true/false dependent on whether the user
        likes music"""
        intent = tracker.latest_message["intent"].get("name")

        if intent == "affirm":
            return [SlotSet("likes_music", True)]
        elif intent == "deny":
            return [SlotSet("likes_music", False)]
        return []
#action_artificial_service
class ActionArtificialService(Action):
    def name(self):
        return "action_artificial_service"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I am sorry, sir. My name is Lucy, can I help you?\n")
        return []
#action_remaining_seats
class ActionRemainingSeats(Action):
    def name(self):
        return "action_remaining_seats"

    def run(self, dispatcher, tracker, domain):
         if tracker.get_slot("concertname") == "big arena":
            dispatcher.utter_message(text="1 first class seats, 4 second class seats, 4 third class seats\nwhich seat you want to reserve?")
            return []
         if tracker.get_slot("concertname") == "rock cellar":
            dispatcher.utter_message(text="4 first class seats, 5 second class seats, 6 third class seats\nwhich seat you want to reserve?")
            return []
         dispatcher.utter_message(text=tracker.get_slot("concertname"))
class ActionSubmit(Action):
    def name(self):
        return "action_submit"

    def run(self, dispatcher, tracker, domain):
        import MySQLdb
        import time
        
        db = MySQLdb.connect("localhost","root","ybs66666","rasa")
        cursor = db.cursor()
        stamp = time.mktime(time.localtime())
        sql = "INSERT INTO concert_order(id_order,name, \
       email, concert_name, ticket_type) \
       VALUES ('%d','%s', '%s', '%s', '%s')" % \
       (stamp,tracker.get_slot('name'), tracker.get_slot('email'), tracker.get_slot('concertname'), tracker.get_slot('ticket_type'))
        #q = "insert into concer_order(name,email,concert_name,ticket_type) VALUES (%s,%s,%s,%s)"
        #v = (tracker.get_slot('name'),tracker.get_slot('email'),tracker.get_slot('concertname'),tracker.get_slot('ticket_type'))
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(str(e))
            dispatcher.utter_message(text=str(e)) 
            db.rollback()
        db.close()
        dispatcher.utter_message(text="All done!")
        dispatcher.utter_message(text="Here is your order id:")
        dispatcher.utter_message(text=str(int(stamp)))
        return []


class ValidateOrderForm(FormValidationAction):
    """Example of an order form validation action."""

    def name(self) -> Text:
        return "validate_order_form"


    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_order_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate concertname value."""
        try:
            int(value)
            import MySQLdb

            # Open database connection
            db = MySQLdb.connect("localhost","root","ybs66666","rasa" )

            # prepare a cursor object using cursor() method
            cursor = db.cursor()

            # Prepare SQL query to INSERT a record into the database.
            sql = "SELECT * FROM concert_order \
            WHERE id_order = '%s'" % (value)
            try:
                # Execute the SQL command
                cursor.execute(sql)
                 # Fetch all the rows in a list of lists.
                results = cursor.fetchall()
                if(len(results)==0):
                    dispatcher.utter_message(text="order dosen't exist")
                    return {"order_id": value}
                for row in results:
                    text_reply = "order id:%s name: %s, email: %s, \n name of concert:%s, type of seat: %s" % \
                        (row[0],row[1],row[2],row[3],row[4])
                    dispatcher.utter_message(text=text_reply)   
            except Exception as e:
                print(str(e))             
                db.close()
            return {"order_id": value}
        except ValueError:
            dispatcher.utter_message(text="Wrong order id format")
            return {"order_id": None}



#- action_reset_information_form
#- action_reset_order_form

class ActionResetConcertname(Action):
    def name(self):
        return "action_reset_concertname"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("concertname",None)]
class ActionResetName(Action):
    def name(self):
        return "action_reset_name"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("name",None)]
class ActionResetEmail(Action):
    def name(self):
        return "action_reset_email"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("email",None)]
class ActionResetTicketType(Action):
    def name(self):
        return "action_reset_ticket_type"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("ticket_type",None)]


class ActionResetOrderid(Action):
    def name(self):
        return "action_reset_order_id"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("order_id",None)]


#class ActionSessionStart(Action):
#    def name(self):
#        return "action_session_start"

#    def run(self, dispatcher, tracker, domain):
#        dispatcher.utter_message(text="I am a concert bot, powered by rasa!")
#        return []
        