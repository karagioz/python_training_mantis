from suds.client import Client
from suds import WebFault


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.config['soap']['url'])
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_user_projects(self, username, password):
        client = Client(self.app.config['soap']['url'])
        try:
            response = list(client.service.mc_projects_get_user_accessible(username, password))
            return response
        except WebFault:
            return False
