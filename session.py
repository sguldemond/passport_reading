import requests, json
import image_handler

api_url = "http://127.0.0.1:5000"

class OnboardingSession:
    """
    TODO: 
    - Add documentation, e.g. session status
    - Error handling API calls
    """
    def __init__(self):
        response = requests.post("{0}/{1}".format(api_url, 'init_onboarding'))
        self.session_id = response.json()['session_id']
        print("Started session with session ID: {0}".format(self.session_id))
        image_handler.qr_image(self.session_id)

    def get_status(self):
        data = {"session_id": self.session_id}
        response = requests.post("{0}/{1}".format(api_url, 'get_session_status'), json=data)
        return response.json()['response']

    def get_data(self):
        data = {"session_id": self.session_id}
        response = requests.post("{0}/{1}".format(api_url, 'get_session'), json=data)
        return response.json()['response']

    def attach_encrypted_data(self, data):
        data = {"encrypted_data": data, "session_id": self.session_id}
        response = requests.post("{0}/{1}".format(api_url, 'attach_encrypted_data'), json=data)
        return response.json()['response']