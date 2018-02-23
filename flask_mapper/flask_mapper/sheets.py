import httplib2
import os
import googlemaps
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from local_settings import GOOGLE_MAPS_KEY

gmaps = googlemaps.Client(key=GOOGLE_MAPS_KEY)

# If modifying these scopes, delete your previously saved credentials
# saved in credentials.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = os.path.join(os.getcwd(),
                                  'flask_mapper/flask_mapper'
                                  '/client_secret.json')
APPLICATION_NAME = 'Flask Mapper'
CREDENTIALS = os.path.join(os.getcwd(),
                           'flask_mapper/flask_mapper/credentials.json')

if __name__ == "__main__":
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None


def get_credentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
    Credentials, the obtained credential.
    """
    store = Storage(CREDENTIALS)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print("Credentials: %s" % credentials)
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
    print('Storing credentials to ' + CREDENTIALS)
    return credentials


class Sheet:
    """
    A Sheet object consists of a cache of lat and lng points from
    a Google sheet, and methods for accessing the sheets data.
    """
    def __init__(self, spreadsheet_id, cell_range):
        self.credentials = get_credentials()
        self.spreadsheet_id = spreadsheet_id
        self.cell_range = cell_range
        self.cache = {}
        self.build_cache()

    def get_values(self):
        http = self.credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        result = service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id, range=self.cell_range).execute()
        values = result.get('values', [])

        return values

    def update_cache(self, row):
        if not str(row) in self.cache:
            location_string = '{}, {}'.format(row[4], row[3])
            location = gmaps.geocode(location_string)[0]['geometry']['location']
            self.cache[str(row)] = {'lat': location['lat'],
                                    'lng': location['lng']}

    def build_cache(self):
        values = self.get_values()
        for row in values:
            try:
                self.update_cache(row)
            except IndexError:
                pass

        # invalidate items in the cache that are not in the list of values
        string_vals = [str(row) for row in values]
        for key in list(self.cache.keys()):
            if key not in string_vals:
                del self.cache[key]

    def get_locations(self):
        self.build_cache()
        return self.cache.values()


if __name__ == '__main__':
    get_credentials()
