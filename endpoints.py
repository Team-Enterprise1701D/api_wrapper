from decouple import config
import requests
from time import sleep
import json


def get_init_response():
    init_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init"
    init_headers = {"Authorization": f"Token {config('SECRET_KEY')}"}
    init_response = json.loads(requests.get(
        init_endpoint, headers=init_headers).content)
    sleep(init_response['cooldown'])
    return init_response


def fly(move, init_response, traversal_graph):
    fly_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/"
    fly_headers = {"Content-Type": "application/json",
                   "Authorization": f"Token {config('SECRET_KEY')}"}
    fly_payload = {"direction": move}
    fly_response = json.loads(requests.post(
        fly_endpoint, data=json.dumps(fly_payload), headers=fly_headers).content)
    print(fly_response['messages'])
    sleep(fly_response['cooldown'])
    return fly_response
