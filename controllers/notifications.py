import requests

from settings import NOTIFICATIONS_SERVICE_URL

class NotificationsController(object):

    def __init__(self, endpoint: str):
        self.url = f'{NOTIFICATIONS_SERVICE_URL}/{endpoint}'

    def notify(self, notification_data: dict):
        try:
            response = requests.post(self.url, json=notification_data)
            return response
        except Exception as e:
            print(e)
