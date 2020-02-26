import requests
import json
import random
from time import sleep, time
import os

dirname = os.path.dirname(os.path.abspath(__file__))
movement_dict = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
response_keys = ['title', 'description', 'coordinates', 'elevation',
                 'terrain', 'players', 'items', 'cooldown', 'errors', 'messages']


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


'''
Build adjacency list.  i.e:
{
    "10": {
        "exits": {
            "n": ?,
            "s": ?,
            'e': ?
            "w": ?
        },
        "title": "A Dark Room",
        "description": "You cannot see anything.",
        "coordinates": "(60,61)",
        "elevation": 0,
        "terrain": "",
        "players": [],
        "items": [],
        "cooldown": 100.0,
        "errors": [],
        "messages": ["You have walked north"]
    }
'''


class Traversal_Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, response):
        # add room id
        self.vertices[response['room_id']] = {}
        # add ? as value for each exit found
        self.vertices[response['room_id']]['exits'] = {
            exit: '?' for exit in response['exits']}
        # add other attributes to adjacency list
        for response_key in response_keys:
            self.vertices[response['room_id']
                          ][response_key] = response[response_key]

    def add_edge(self, init_response, move_response, move):
        if (init_response['room_id'] in self.vertices) and (move_response['room_id'] in self.vertices):
            self.vertices[init_response['room_id']
                          ]['exits'][move] = move_response['room_id']
            self.vertices[move_response['room_id']
                          ]['exits'][movement_dict[move]] = init_response['room_id']
        else:
            raise IndexError("That room does not exist!")

    def get_neighbors(self, room_id):
        return set(self.vertices[room_id]['exits'].values())

    def bfs_to_unexplored(self, init_response):
        queue = Queue()
        # enqueue the starting room received back from the init call
        queue.enqueue([init_response['room_id']])
        # to keep track of what rooms we have already visited
        visited = set()
        while queue.size() > 0:
            path = queue.dequeue()
            # get last room in path
            vertex = path[-1]
            if vertex not in visited:
                if vertex == '?':
                    directions = []
                    for i in range(1, len(path[:-1])):
                        for option in traversal_graph.vertices[path[i - 1]][['exits']]:
                            if traversal_graph.vertices[path[i - 1]]['exits'][option] == path[i]:
                                directions.append(option)
                    return directions

                visited.add(vertex)
                # for each edge in the item
                for next_vert in self.get_neighbors(vertex):
                    new_path = list(path)
                    new_path.append(next_vert)
                    queue.enqueue(new_path)


#  method to get and return the init response when invoked
def get_init_response():
    init_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
    init_headers = {
        "Authorization": f"Token e4e970f3235624c19c5e184bd2eadbd897ecc8d4"}
    # convert json to python object
    init_response = json.loads(requests.get(
        init_endpoint, headers=init_headers).content)
    sleep(init_response['cooldown'])
    return init_response


'''
 method to make a move when passed a move direction.  Will sleep based on returned cooldown time to avoid penalty
'''


def make_move(move):
    move_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    move_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token e4e970f3235624c19c5e184bd2eadbd897ecc8d4"}
    move_direction = {"direction": move}
    move_response = json.loads(requests.post(
        move_endpoint, data=json.dumps(move_direction), headers=move_headers).content)
    # sleep for period of time received in move_response
    sleep(move_response['cooldown'])
    return move_response


traversal_graph = Traversal_Graph()  # instantiate

with open(os.path.join(dirname, 'traversal_graph.txt')) as json_file:
    traversal_graph.vertices = json.load(json_file)
