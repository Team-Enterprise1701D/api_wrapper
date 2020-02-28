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


def make_wise_move(move, init_response, check_status_response, traversal_graph):
    # if 'move' is a list of moves and 'dash' is in our list of abilities > dash
    if ('dash' in check_status_response['abilities']) and (type(move) == list):
        dash(move, init_response, traversal_graph)
    else:
        next_room_id = traversal_graph.vertices[init_response['room_id']]['exits'][move]
        current_elevation = init_response['elevation']
        next_room_elevation = traversal_graph.vertices[next_room_id]['elevation']
        elevation_change = next_room_elevation - current_elevation
        # if going from a higher elevation to a lower elevation then 'fly'
        if ('fly' in check_status_response['abilities']) and (elevation_change < 0):
            fly(move, init_response, traversal_graph)
        else:  # make a normal move
            move_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
            move_headers = {"Content-Type": "application/json",
                            "Authorization": f"Token {config('SECRET_KEY')}"}
            move_payload = {"direction": move,
                            "next_room_id": str(next_room_id)}
            move_response = json.loads(requests.post(
                move_endpoint, data=json.dumps(move_payload), headers=move_headers).content)
            print(move_response['messages'])
            sleep(move_response['cooldown'])
            return move_response


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


def get_last_proof():
    last_proof_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/"
    last_proof_headers = {"Authorization": f"Token {config('SECRET_KEY')}"}
    last_proof_response = json.loads(requests.get(
        last_proof_endpoint, headers=last_proof_headers).content)
    sleep(last_proof_response['cooldown'])
    return last_proof_response


def mine(proof):
    mine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/"
    mine_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token {config('SECRET_KEY')}"}
    mine_payload = {"proof": proof}
    mine_response = json.loads(requests.post(
        mine_endpoint, data=json.dumps(mine_payload), headers=mine_headers).content)
    sleep(mine_response['cooldown'])
    return mine_response


def get_lambda_coin_balance():
    lambda_coin_balance_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/"
    lambda_coin_balance_headers = {
        "Authorization": f"Token {config('SECRET_KEY')}"}
    lambda_coin_balance_response = json.loads(requests.get(
        lambda_coin_balance_endpoint, headers=lambda_coin_balance_headers).content)
    sleep(lambda_coin_balance_response['cooldown'])
    return lambda_coin_balance_response


def pray():
    pray_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/"
    pray_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token {config('SECRET_KEY')}"}
    pray_response = json.loads(requests.post(
        pray_endpoint, headers=pray_headers).content)
    sleep(pray_response['cooldown'])
    return pray_response


def recall():
    recall_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/recall/"
    recall_headers = {"Content-Type": "application/json",
                      "Authorization": f"Token {config('SECRET_KEY')}"}
    recall_response = json.loads(requests.post(
        recall_endpoint, headers=recall_headers).content)
    sleep(recall_response['cooldown'])
    return recall_response


def carry(item):
    carry_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/carry/"
    carry_headers = {"Content-Type": "application/json",
                     "Authorization": f"Token {config('SECRET_KEY')}"}
    carry_payload = {"name": item}
    carry_response = json.loads(requests.post(
        carry_endpoint, data=json.dumps(carry_payload), headers=carry_headers).content)
    sleep(carry_response['cooldown'])
    return carry_response


def receive():
    receive_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/receive/"
    receive_headers = {"Content-Type": "application/json",
                       "Authorization": f"Token {config('SECRET_KEY')}"}
    receive_response = json.loads(requests.post(
        receive_endpoint, headers=receive_headers).content)
    sleep(receive_response['cooldown'])
    return receive_response


def wear(item):
    wear_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/wear/"
    wear_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token {config('SECRET_KEY')}"}
    wear_payload = {"name": item}
    wear_response = json.loads(requests.post(
        wear_endpoint, data=json.dumps(wear_payload), headers=wear_headers).content)
    sleep(wear_response['cooldown'])
    return wear_response


def undress(item):
    undress_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/undress/"
    undress_headers = {"Content-Type": "application/json",
                       "Authorization": f"Token {config('SECRET_KEY')}"}
    undress_payload = {"name": item}
    undress_response = json.loads(requests.post(undress_endpoint, data=json.dumps(
        undress_payload), headers=undress_headers).content)
    sleep(undress_response['cooldown'])
    return undress_response


def transmogrify(item):
    transmogrify_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/transmogrify/"
    transmogrify_headers = {"Content-Type": "application/json",
                            "Authorization": f"Token {config('SECRET_KEY')}"}
    transmogrify_payload = {"name": item}
    transmogrify_response = json.loads(requests.post(transmogrify_endpoint, data=json.dumps(
        transmogrify_payload), headers=transmogrify_headers).content)
    sleep(transmogrify_response['cooldown'])
    return transmogrify_response
