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


# move needs to be an array of directions (i.e. [n, e, n, w, e] etc) from the starting room to the ending room


def dash(move, init_response, traversal_graph):
    dash_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/dash/"
    dash_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token {config('SECRET_KEY')}"}
    move_direction = move[0]
    starting_room = init_response['room_id']
    next_room_ids = []
    for i in range(len(move)):
        next_room_id = traversal_graph.vertices[starting_room]['exits'][move_direction]
        next_room_ids.append(str(next_room_id))
        starting_room = next_room_id
    dash_payload = {"direction": move_direction, "num_rooms": str(
        len(next_room_ids)), "next_room_ids": ','.join(next_room_ids)}
    dash_response = json.loads(requests.post(
        dash_endpoint, data=json.dumps(dash_payload), headers=dash_headers).content)
    print(dash_response['messages'])
    sleep(dash_response['cooldown'])
    return dash_response


def take_item(item):
    take_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/take/"
    take_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token {config('SECRET_KEY')}"}
    take_payload = {"name": item}
    take_response = json.loads(requests.post(
        take_endpoint, data=json.dumps(take_payload), headers=take_headers).content)
    sleep(take_response['cooldown'])
    return take_response


def drop_item(item):
    drop_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/"
    drop_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token {config('SECRET_KEY')}"}
    drop_payload = {"name": item}
    drop_response = json.loads(requests.post(
        drop_endpoint, data=json.dumps(drop_payload), headers=drop_headers).content)
    sleep(drop_response['cooldown'])
    return drop_response


def sell_item(item):
    sell_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/"
    sell_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token {config('SECRET_KEY')}"}
    sell_payload = {"name": item, "confirm": "yes"}
    sell_response = json.loads(requests.post(
        sell_endpoint, data=json.dumps(sell_payload), headers=sell_headers).content)
    sleep(sell_response['cooldown'])
    return sell_response


def examine_item(item):
    examine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/"
    examine_headers = {"Content-Type": "application/json",
                       "Authorization": f"Token {config('SECRET_KEY')}"}
    examine_payload = {"name": item}
    examine_response = json.loads(requests.post(examine_endpoint, data=json.dumps(
        examine_payload), headers=examine_headers).content)
    sleep(examine_response['cooldown'])
    return examine_response


def check_status():
    status_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/status/"
    status_headers = {"Content-Type": "application/json",
                      "Authorization": f"Token {config('SECRET_KEY')}"}
    status_response = json.loads(requests.post(
        status_endpoint, headers=status_headers).content)
    sleep(status_response['cooldown'])
    return status_response


def change_name(name):
    change_name_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/status/"
    change_name_headers = {"Content-Type": "application/json",
                           "Authorization": f"Token {config('SECRET_KEY')}"}
    change_name_payload = {"name": name}
    change_name_response = json.loads(requests.post(
        change_name_endpoint, data=json.dumps(change_name_payload), headers=change_name_headers).content)
    sleep(change_name_response['cooldown'])
    return change_name_response


def mine(proof):
    mine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/"
    mine_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token {config('SECRET_KEY')}"}
    mine_payload = {"proof": proof}
    mine_response = json.loads(requests.post(
        mine_endpoint, data=json.dumps(mine_payload), headers=mine_headers).content)
    sleep(mine_response['cooldown'])
    return mine_response