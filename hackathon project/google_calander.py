from pprint import pprint
from Google import Create_Service

CLIENT_SECRET_FILE = ''
API_NAME = ''
API_VERSION = ''
SCOPES = ['']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

request