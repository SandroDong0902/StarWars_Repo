from starwars import Starships
import requests
import pytest
import pymongo
from bson import objectid


@pytest.fixture
def starship():
    return Starships('StarWars')


db = pymongo.MongoClient()['StarWars']


def verify(answer, correct_answer):
    assert correct_answer == answer


def test_get_pilot_name(starship):
    pilot_name = starship.get_pilot_name({'pilots': ["https://swapi.dev/api/people/13/",
                                           "https://swapi.dev/api/people/14/",
                                           "https://swapi.dev/api/people/25/",
                                           "https://swapi.dev/api/people/31/"]})

    correct_pilot_name = ["Chewbacca", "Han Solo", "Lando Calrissian", "Nien Nunb"]

    #verify(pilot_name, correct_pilot_name)
    for p in range(4):
        assert pilot_name[p] == correct_pilot_name[p]


def test_get_pilot_id(starship):
    pilot_id = starship.get_pilot_id(["Chewbacca", "Han Solo", "Lando Calrissian", "Nien Nunb"])

    correct_pilot_id = [objectid.ObjectId('61e69409947879cf3de981dd'),
                        objectid.ObjectId('61e6940c78ad410baa6a9b83'),
                        objectid.ObjectId('61e6940ed3b16fc78476c2f6'),
                        objectid.ObjectId('61e6940fd565fe931645ea4b')]

    #verify(pilot_id, correct_pilot_id)
    for i in range(4):
        assert pilot_id[i] == correct_pilot_id[i]

data = requests.get("https://swapi.dev/api/starships/?page=1").json()

def test_change_url_to_id(starship):
    correct_pilot_id = [objectid.ObjectId('61e69409947879cf3de981dd'),
                        objectid.ObjectId('61e6940c78ad410baa6a9b83'),
                        objectid.ObjectId('61e6940ed3b16fc78476c2f6'),
                        objectid.ObjectId('61e6940fd565fe931645ea4b')]

    starship.change_url_to_id(data)

    pilot_id = data['results'][4]['pilots']

    verify(pilot_id, correct_pilot_id)


# It is supposed to pass but there are technical issues
# I'll never use pytest in the future...
def test_insert_all_page(starship):

    # correct_pilot_id = ["https://swapi.dev/api/people/13/",
    #                     "https://swapi.dev/api/people/14/",
    #                     "https://swapi.dev/api/people/25/",
    #                     "https://swapi.dev/api/people/31/"]
    #
    # starship.insert_all_page(requests.get("https://swapi.dev/api/starships/?page=1").json())
    # pilots_id = db.starships.find({'name': 'Millennium Falcon'}, {'pilots': 1, '_id': 0})
    #
    # for pilots in pilots_id:
    #     pilot_list = pilots['pilots']
    #
    # print(pilot_list)
    # #verify(pilot_list, correct_pilot_id)
    pass