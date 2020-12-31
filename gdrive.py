from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os

SCOPES = [
    'https://www.googleapis.com/auth/drive.file'
]

store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

def create_spreadsheet(name):
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    hunt_folder_id = os.getenv('HUNT_FOLDER_ID')
    data = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [hunt_folder_id],
    }

    return DRIVE.files().create(body=data).execute()


def sheet_link(sheet_id):
    return 'https://docs.google.com/spreadsheets/d/{}/edit'.format(sheet_id)


if __name__ == '__main__':
    sheet = create_spreadsheet('My test sheet')
    print(sheet_link(sheet['id']))
