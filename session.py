import image_handler

from requests.exceptions import ConnectionError
import requests, json, logging, sys


class OnboardingSession:
    """
    This class handles all the communcation with the session manager.

    session_id: Session ID of session retrieved from Session Manager
    """
    def __init__(self, api_url):
        """
        Initiate the class as an object and initiate a session at the session manager

        :param string api_url: URL of Session Manager to connect with
        """
        self.api_url = api_url
        error_message_init = "Could not connect to API [{}], please check connection".format(self.api_url)
        error_message_lost = "Connection with API lost [{}], please check connection".format(self.api_url)

        try:
            response = requests.post("{0}/{1}".format(self.api_url, 'init_onboarding'))
            self.session_id = response.json()['session_id']
            print "Started session [{}]".format(self.session_id)
        except ConnectionError as e:
            logging.error(e)
            print self.error_message_init
            sys.exit(1)

    def get_status(self):
        """
        Get status of the session by its session ID
        """
        data = {"session_id": self.session_id}
        try:
            response = requests.post("{0}/{1}".format(self.api_url, 'get_session_status'), json=data)
            return response.json()['response']
        except ConnectionError as e:
            logging.error(e)
            print self.error_message_lost

    def get_data(self):
        """
        Get all the data of a session by its session ID
        """
        data = {"session_id": self.session_id}
        try:
            response = requests.post("{0}/{1}".format(self.api_url, 'get_session'), json=data)
            return response.json()['response']
        except ConnectionError as e:
            logging.error(e)
            print self.error_message_lost

    def attach_encrypted_data(self, data):
        """
        Add encrypted data to the session

        :param string data: String retrieved from encryption library with encrypted data
        """
        data = {"encrypted_data": data, "session_id": self.session_id}
        try:
            response = requests.post("{0}/{1}".format(self.api_url, 'attach_encrypted_data'), json=data)
            print "Added data to session [{}]".format(self.session_id)
            return response.json()['response']
        except ConnectionError as e:
            logging.error(e)
            print self.error_message_lost