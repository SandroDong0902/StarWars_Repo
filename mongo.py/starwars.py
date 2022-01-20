import pymongo
import requests

class Starships:
    """
        This class connects to the StarWars database and pulls the starships
        information from the swapi.dev API. It then links the pilots in each starship,
        to our own characters collection by swapping their pilot url to our characters
        Object ID
    """

    # Initialize the connection with MongoDB
    def __init__(self, db_name):
        self.client = pymongo.MongoClient()
        self.db = self.client[db_name]
        self.db.starships.drop()

        self.collection = self.db.create_collection('starships')
        self.starships = requests.get("https://swapi.dev/api/starships/?page=1").json()

    # Inserts all the results of the starship page to the starships collection
    @property

    def insert_all_page(self, data):
        for i in range(len(data['results'])):
            self.db.starships.insert_one(data['results'][i])

    # Gets the pilot id from the characters collections using the pilot name
    # Returns a list of pilots Object ID
    def get_pilot_id(self, pilot_names):
        pilot_id = []
        for i in pilot_names:
            pilot_id.append(self.db.characters.find({'name': i}, {'_id': 1}).next()['_id'])
        return pilot_id

    # Gets the pilot names from an individual starship
    # Return a list of Strings with pilot names
    def get_pilot_name(self, result):
        pilot_names = []
        for i in result['pilots']:
            pilot = requests.get(i).json()
            pilot_names.append(pilot['name'])
        return pilot_names

    # Swaps the pilot url list to our characters Object_ID list
    def change_url_to_id(self, data):

        for i in range(len(data['results'])):
            if len(data['results'][i]['pilots']) == 0:
                continue
            pilot_names = self.get_pilot_name(data['results'][i])
            pilot_id = self.get_pilot_id(pilot_names)
            print(pilot_id)
            data['results'][i]['pilots'] = pilot_id

    # Main class function
    def start(self):

        while True:
            self.change_url_to_id(self.starships)
            self.insert_all_page(self.starships)

            if self.starships['next'] is None:
                break
            self.starships = requests.get(self.starships['next']).json()

        print('\n')
        print('Done!')
        print('Operation Successfully Completed!')


s = Starships('StarWars')
s.start()
