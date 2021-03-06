import requests
import json
from time import sleep, time
import random
from dark_room_map_rooms import dark_island_map
import hashlib

movement_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
my_name = 'Hannah Tuttle'
token = "Token 5740acca65a9d61760e99fb06308fe18cbf29a3c"

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Traversal_Graph:
    def __init__(self):
        self.vertices = {}

    def get_neighbors(self, room_id):
        return set(self.vertices[room_id]['exits'].values())

    '''
    bfs takes 3 args: 
        1. init_response of the room you are in
        2. key_to_search is the attribute of the room you are searching
            a. room_id
            b. title (Room Name)
            c. item or description
        3. value_to_search - (i.e. room#, 'shrine', 'treasure'. It can also be a set if looking for more than one value
    '''

    def bfs(self, init_response, key_to_search, value_to_search):
        queue = Queue()
        queue.enqueue([init_response['room_id']])
        visited = set()
        while queue.size() > 0:
            path = queue.dequeue()
            vertex = path[-1]
            if vertex not in visited:
                if key_to_search == 'room_id':
                    # if looking for more than one room
                    if type(value_to_search) == set:
                        if vertex in value_to_search:
                            directions = []
                            for i in range(1, len(path)):
                                for option in traversal_graph.vertices[path[i - 1]]['exits']:
                                    if traversal_graph.vertices[path[i - 1]]['exits'][
                                            option] == path[i]:
                                        directions.append(option)
                            return(directions)

                        # if looking for a single room
                    elif type(value_to_search) != set:
                        if vertex == value_to_search:
                            directions = []
                            for i in range(1, len(path)):
                                for option in traversal_graph.vertices[path[i - 1]]['exits']:
                                    if traversal_graph.vertices[path[i - 1]]['exits'][
                                            option] == path[i]:
                                        directions.append(option)
                            return(directions)
                    visited.add(vertex)

                # if looking for a room name/s (i.e.'shop')
                if key_to_search == 'title':

                    # if looking for multiple room names
                    if type(value_to_search) == set:
                        if self.vertices[vertex][key_to_search] in value_to_search:
                            directions = []
                            for i in range(1, len(path)):
                                for option in traversal_graph.vertices[path[i - 1]]['exits']:
                                    if traversal_graph.vertices[path[i - 1]]['exits'][
                                            option] == path[i]:
                                        directions.append(option)
                            return(directions)

                        # if only looking for a specific room name
                    if type(value_to_search) != set:
                        if self.vertices[vertex][key_to_search] == value_to_search:
                            directions = []
                            for i in range(1, len(path)):
                                for option in traversal_graph.vertices[path[i - 1]]['exits']:
                                    if traversal_graph.vertices[path[i - 1]]['exits'][
                                            option] == path[i]:
                                        directions.append(option)
                            return(directions)
                    visited.add(vertex)

                # if looking for an item or a word in a description
                if key_to_search in ['items', 'description']:
                    if value_to_search in self.vertices[vertex][key_to_search]:
                        directions = []
                        for i in range(1, len(path)):
                            for option in traversal_graph.vertices[path[i - 1]]['exits']:
                                if traversal_graph.vertices[path[i - 1]]['exits'][
                                        option] == path[i]:
                                    directions.append(option)
                        return(directions)
                    visited.add(vertex)

                for next_vert in self.get_neighbors(vertex):
                    new_path = list(path)
                    new_path.append(next_vert)
                    queue.enqueue(new_path)


def get_init_response():
    init_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init"
    init_headers = {
        "Authorization": token}
    init_response = json.loads(requests.get(
        init_endpoint, headers=init_headers).content)
    sleep(init_response['cooldown'])
    return init_response


def fly(move, init_response, traversal_graph):
    fly_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/fly/"
    fly_headers = {"Content-Type": "application/json",
                   "Authorization": token}
    fly_payload = {"direction": move}
    fly_response = json.loads(requests.post(
        fly_endpoint, data=json.dumps(fly_payload), headers=fly_headers).content)
    print(fly_response['messages'])
    sleep(fly_response['cooldown'])
    return fly_response


# dash move needs to be an array of directions (i.e. [n, e, n, w, e] etc) from the starting room to the ending room


def dash(move, init_response, traversal_graph):
    dash_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/dash/"
    dash_headers = {"Content-Type": "application/json",
                    "Authorization":token}
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
                            "Authorization": token}
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
                    "Authorization": token}
    take_payload = {"name": item}
    take_response = json.loads(requests.post(
        take_endpoint, data=json.dumps(take_payload), headers=take_headers).content)
    sleep(take_response['cooldown'])
    return take_response


def drop_item(item):
    drop_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/"
    drop_headers = {"Content-Type": "application/json",
                    "Authorization": token}
    drop_payload = {"name": item}
    drop_response = json.loads(requests.post(
        drop_endpoint, data=json.dumps(drop_payload), headers=drop_headers).content)
    sleep(drop_response['cooldown'])
    return drop_response


def sell_item(item):
    sell_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/"
    sell_headers = {"Content-Type": "application/json",
                    "Authorization": token}
    sell_payload = {"name": item, "confirm": "yes"}
    sell_response = json.loads(requests.post(
        sell_endpoint, data=json.dumps(sell_payload), headers=sell_headers).content)
    sleep(sell_response['cooldown'])
    return sell_response


def examine_item(item):
    examine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/"
    examine_headers = {"Content-Type": "application/json",
                       "Authorization": token}
    examine_payload = {"name": item}
    examine_response = json.loads(requests.post(examine_endpoint, data=json.dumps(
        examine_payload), headers=examine_headers).content)
    sleep(examine_response['cooldown'])
    return examine_response


def check_status():
    status_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/status/"
    status_headers = {"Content-Type": "application/json",
                      "Authorization": token}
    status_response = json.loads(requests.post(
        status_endpoint, headers=status_headers).content)
    sleep(status_response['cooldown'])
    return status_response


def change_name(name):
    change_name_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/"
    change_name_headers = {"Content-Type": "application/json",
                           "Authorization":token}
    change_name_payload = {"name": name, "confirm": "aye"}
    change_name_response = json.loads(requests.post(
        change_name_endpoint, data=json.dumps(change_name_payload), headers=change_name_headers).content)
    sleep(change_name_response['cooldown'])
    return change_name_response


def get_last_proof():
    last_proof_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/"
    last_proof_headers = {
        "Authorization": token}
    last_proof_response = json.loads(requests.get(
        last_proof_endpoint, headers=last_proof_headers).content)
    sleep(last_proof_response['cooldown'])
    return last_proof_response


def mine(proof):
    mine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/"
    mine_headers = {"Content-Type": "application/json",
                    "Authorization": token}
    mine_payload = {"proof": proof}
    mine_response = json.loads(requests.post(
        mine_endpoint, data=json.dumps(mine_payload), headers=mine_headers).content)
    sleep(mine_response['cooldown'])
    return mine_response


def get_lambda_coin_balance():
    lambda_coin_balance_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/"
    lambda_coin_balance_headers = {
        "Authorization": token}
    lambda_coin_balance_response = json.loads(requests.get(
        lambda_coin_balance_endpoint, headers=lambda_coin_balance_headers).content)
    sleep(lambda_coin_balance_response['cooldown'])
    return lambda_coin_balance_response


def pray():
    pray_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/"
    pray_headers = {"Content-Type": "application/json",
                    "Authorization": token}
    pray_response = json.loads(requests.post(
        pray_endpoint, headers=pray_headers).content)
    sleep(pray_response['cooldown'])
    return pray_response


def recall():
    recall_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/recall/"
    recall_headers = {"Content-Type": "application/json",
                      "Authorization": token}
    recall_response = json.loads(requests.post(
        recall_endpoint, headers=recall_headers).content)
    sleep(recall_response['cooldown'])
    return recall_response


def carry(item):
    carry_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/carry/"
    carry_headers = {"Content-Type": "application/json",
                     "Authorization": token}
    carry_payload = {"name": item}
    carry_response = json.loads(requests.post(
        carry_endpoint, data=json.dumps(carry_payload), headers=carry_headers).content)
    sleep(carry_response['cooldown'])
    return carry_response


def receive():
    receive_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/receive/"
    receive_headers = {"Content-Type": "application/json",
                       "Authorization": token}
    receive_response = json.loads(requests.post(
        receive_endpoint, headers=receive_headers).content)
    sleep(receive_response['cooldown'])
    return receive_response


def wear(item):
    wear_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/wear/"
    wear_headers = {"Content-Type": "application/json",
                    "Authorization": token}
    wear_payload = {"name": item}
    wear_response = json.loads(requests.post(
        wear_endpoint, data=json.dumps(wear_payload), headers=wear_headers).content)
    sleep(wear_response['cooldown'])
    return wear_response


def undress(item):
    undress_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/undress/"
    undress_headers = {"Content-Type": "application/json",
                       "Authorization": token}
    undress_payload = {"name": item}
    undress_response = json.loads(requests.post(undress_endpoint, data=json.dumps(
        undress_payload), headers=undress_headers).content)
    sleep(undress_response['cooldown'])
    return undress_response


def transmogrify(item):
    transmogrify_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/transmogrify/"
    transmogrify_headers = {"Content-Type": "application/json",
                            "Authorization": token}
    transmogrify_payload = {"name": item}
    transmogrify_response = json.loads(requests.post(transmogrify_endpoint, data=json.dumps(
        transmogrify_payload), headers=transmogrify_headers).content)
    sleep(transmogrify_response['cooldown'])
    return transmogrify_response

def examine_item(item):
    examine_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/"
    examine_headers = {"Content-Type": "application/json",
                       "Authorization": token}
    examine_payload = {"name": item}
    examine_response = json.loads(requests.post(examine_endpoint, data=json.dumps(
        examine_payload), headers=examine_headers).content)
    sleep(examine_response['cooldown'])
    return examine_response

def get_lambda_coin_balance():
    lambda_coin_balance_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/bc/get_balance/"
    lambda_coin_balance_headers = {
        "Authorization": token}
    lambda_coin_balance_response = json.loads(requests.get(
        lambda_coin_balance_endpoint, headers=lambda_coin_balance_headers).content)
    sleep(lambda_coin_balance_response['cooldown'])
    return lambda_coin_balance_response

def warp():
    warp_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/warp/"
    warp_headers = {
        "Authorization": token}
    warp_response = json.loads(requests.post(
        warp_endpoint, headers=warp_headers).content)
    sleep(warp_response['cooldown'])
    return warp_response

traversal_graph = Traversal_Graph()
traversal_graph.vertices = dark_island_map

# *******************uncomment when you have at least 7 lamnda coins*************************

check_status_response = check_status()
print(f'CHECK STATUS RESPONSE: {check_status_response}')
encumbrance = check_status_response['encumbrance']
init_response = get_init_response()
print(f'CHECK INIT RESPONSE: {init_response}')


def goToRoom(destinationRoom):
    init_response = get_init_response()
    print("Init response : ", init_response)

    check_status_response = check_status()
    print("Current status ", check_status_response)

    counter = 0
    to_room = traversal_graph.bfs(init_response, 'room_id', destinationRoom)
    for move in to_room:
        # make move
        make_wise_move(move, init_response,
                       check_status_response, traversal_graph)
        counter += 1
        print(f'{counter} moves made.')  # to let me know it's running!
        init_response = get_init_response()

    init_response = get_init_response()
    print("Init response : ", init_response)


def find_wishing_well(traversal_graph):
    init_response = get_init_response()
    check_status_response = check_status()
    wishing_well =  None
    # first get a set of the locations of all shrines
    for vertex in traversal_graph.vertices:
        if 'Wishing' in traversal_graph.vertices[vertex]['title']:
            wishing_well  = vertex
            break

    if not wishing_well:
        print("Could not find wishing well")
        return

    print("Look for wishing well ", wishing_well)
    to_wishing_well = traversal_graph.bfs(init_response, 'room_id', wishing_well)
    counter = 0
    for move in to_wishing_well:
        # make move
        make_wise_move(move, init_response,
                       check_status_response, traversal_graph)
        counter += 1
        print(f'{counter} moves made.')  # to let me know it's running!
        init_response = get_init_response()
        traversal_graph.vertices[init_response['room_id']]['items'] = init_response['items']
    wish_response = examine_item("WELL")
    description = wish_response['description']
    print(f'CHECK WELL RESPONSE: {wish_response}')
    print(f'getting room returned: {description}')
    room_to_mine = description.split()[-1]
    print(f'room to mine: {room_to_mine}')
    return int(room_to_mine)

# find_wishing_well(traversal_graph)


def continuous_snitch_finding(traversal_graph):
    count = 0
    start_time = time()
    while True:
        print(f"{count} snitches found in {time() - start_time} seconds")
        room_to_mine = find_wishing_well(traversal_graph)
        goToRoom(room_to_mine)
        item_response = examine_item('golden snitch')
        print('ITEM RESPONSE', item_response)
        take_item('golden snitch')
        status = check_status()
        print('STATUS:', status)
        count +=1

continuous_snitch_finding(traversal_graph)


