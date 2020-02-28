import requests
import json
import random
from time import sleep, time
import os

dirname = os.path.dirname(os.path.abspath(__file__))
movement_dict = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
response_keys = ['title', 'description', 'coordinates', 'elevation', 'terrain',
                 'players', 'items', 'cooldown', 'errors', 'messages']


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

    def add_vertex(self, response):
        self.vertices[response['room_id']] = {}
        self.vertices[response['room_id']]['exits'] = {
            exit: '?' for exit in response['exits']}
        for response_key in response_keys:
            self.vertices[response['room_id']
                          ][response_key] = response[response_key]

    def add_edge(self, init_response, move_response, move):
        if (init_response['room_id'] in self.vertices) and (
                move_response['room_id'] in self.vertices):
            self.vertices[init_response['room_id']
                          ]['exits'][move] = move_response['room_id']
            self.vertices[move_response['room_id']]['exits'][
                movement_dict[move]] = init_response['room_id']
        else:
            raise IndexError("That room does not exist!")

    def get_neighbors(self, room_id):
        return set(self.vertices[room_id]['exits'].values())

    def bfs_to_unexplored(self, init_response):
        queue = Queue()
        queue.enqueue([init_response['room_id']])
        visited = set()
        while queue.size() > 0:
            path = queue.dequeue()
            vertex = path[-1]
            if vertex not in visited:
                if vertex == '?':
                    directions = []
                    for i in range(1, len(path[:-1])):
                        for option in traversal_graph.vertices[path[i - 1]]['exits']:
                            if traversal_graph.vertices[path[i - 1]]['exits'][
                                    option] == path[i]:
                                directions.append(option)
                    return directions
                visited.add(vertex)
                for next_vert in self.get_neighbors(vertex):
                    new_path = list(path)
                    new_path.append(next_vert)
                    queue.enqueue(new_path)


def get_init_response():
    init_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
    init_headers = {
        "Authorization": f"Token e4e970f3235624c19c5e184bd2eadbd897ecc8d4"}
    init_response = json.loads(requests.get(
        init_endpoint, headers=init_headers).content)
    sleep(init_response['cooldown'])
    return init_response


def make_move(move):
    move_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    move_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token e4e970f3235624c19c5e184bd2eadbd897ecc8d4"}
    move_payload = {"direction": move}
    move_response = json.loads(requests.post(
        move_endpoint, data=json.dumps(move_payload), headers=move_headers).content)
    sleep(move_response['cooldown'])
    return move_response


traversal_graph = Traversal_Graph()
f = open('traversal_graph.txt', 'a')
init_response = get_init_response()
traversal_graph.add_vertex(init_response)

counter = 0
start_time = time()
while len(traversal_graph.vertices) < 500:
    init_response = get_init_response()
    exits = init_response['exits']
    unexplored = [option for option in exits if (
        traversal_graph.vertices[init_response['room_id']]['exits'][option] == '?')]
    if len(unexplored) > 0:
        move = random.choice(unexplored)
        move_response = make_move(move)
        counter += 1
        post_move_room_id = move_response['room_id']
        if post_move_room_id not in traversal_graph.vertices:
            traversal_graph.add_vertex(move_response)
            print(
                f"{len(traversal_graph.vertices)} rooms found in {counter} moves and {time() - start_time} seconds")
        traversal_graph.add_edge(init_response, move_response, move)
    else:
        to_unexplored = traversal_graph.bfs_to_unexplored(init_response)
        for move in to_unexplored:
            make_move(move)
            counter += 1

f.write(f'{traversal_graph.vertices}')
f.close()
