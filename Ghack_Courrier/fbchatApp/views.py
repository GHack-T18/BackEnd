from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from facebook import GraphAPI
import json
import requests
import logging  
logging.basicConfig(level=logging.INFO)  
ACCESS_TOKEN = 'EAAQLWOTZC6ZC0BOZCPgNleHJTlnxZARI1lu3CSHqpJRNCHEBGJqUQa1ysxf4MHc0q7W5ejEiffoYfknGhK1ZCjiqAhTjztFK6HPEVTjs6MjUsjowl1Jk5ZBbMcY4ZAv5NulWi6bueNLHvvdo8lkixdPYAQUpR1t5bAT6HvZAcZCAYj8XrowsHdZC7oANiWXQtROv56'

@method_decorator(csrf_exempt, name='dispatch')
class FacebookWebhookView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('hub.mode') == 'subscribe' and \
           request.GET.get('hub.verify_token') == 'uq8W68O1mW-6yaU8t4Dcf4apCSUNnTQHRVtjHd3MmQ8':
            logging.info("Vérification du webhook réussie.")
            return HttpResponse(request.GET.get('hub.challenge'))
        else:
            logging.error("Échec de la vérification du webhook.")
            return HttpResponse(status=400)

    def post(self, request, *args, **kwargs):
        # Gérer les messages entrants
        messaging_events = self.parse_messaging_events(request)
        for event in messaging_events:
            sender_id = event['sender']['id']
            message_text = event['message']['text']
            logging.info(f"Message reçu de {sender_id}: {message_text}")
            print(sender_id)
            sender_info = self.get_sender_info(sender_id)
            if sender_info:
                logging.info(f"Sender information: {sender_info}")
        return HttpResponse()

    def parse_messaging_events(self, request):
        messaging_events = []
        data = request.body.decode('utf-8')
        for entry in json.loads(data)['entry']:
            for event in entry['messaging']:
                messaging_events.append(event)
        return messaging_events
    
    def get_sender_info(self, sender_id):
        url = f"https://graph.facebook.com/{sender_id}?fields=name,profile_pic&access_token={ACCESS_TOKEN}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to get sender information. Status code: {response.status_code}")
                return None
        except Exception as e:
            logging.error(f"An error occurred while getting sender information: {str(e)}")
            return None
