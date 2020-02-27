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
        # if both rooms exist in self.vertices connect them
        if (init_response['room_id'] in self.vertices) and (move_response['room_id'] in self.vertices):
            self.vertices[init_response['room_id']
                          ]['exits'][move] = move_response['room_id']
            self.vertices[move_response['room_id']
                          ]['exits'][movement_dict[move]] = init_response['room_id']
        else:
            raise IndexError("That room does not exist!")

    def get_neighbors(self, room_id):
        return set(self.vertices[room_id]['exits'].values())

    # use bfs to traverse unknown map
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
                # for each edge
                for next_vert in self.get_neighbors(vertex):
                    new_path = list(path)
                    new_path.append(next_vert)
                    queue.enqueue(new_path)


#  method to get and return data from room I am in
def get_init_response():
    init_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
    init_headers = {
        "Authorization": f"Token e4e970f3235624c19c5e184bd2eadbd897ecc8d4"}  # probably need a config file here
    # convert json to python object
    init_response = json.loads(requests.get(
        init_endpoint, headers=init_headers).content)
    # sleep for cooldown time recieved in response
    sleep(init_response['cooldown'])
    return init_response  # and free to make another request right away


def make_move(move):
    move_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    move_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token e4e970f3235624c19c5e184bd2eadbd897ecc8d4"}  # and here
    move_direction = {"direction": move}
    move_response = json.loads(requests.post(
        move_endpoint, data=json.dumps(move_direction), headers=move_headers).content)
    # sleep for period of time received in move_response
    sleep(move_response['cooldown'])
    return move_response


traversal_graph = Traversal_Graph()  # instantiate

with open(os.path.join(dirname, 'traversal_graph.txt')) as json_file:
    traversal_graph.vertices = json.load(json_file)

init_response = get_init_response()  # invoke init and receive response

traversal_graph.add_vertex(init_response)  # send response to add_vertex method

counter = 0
start_time = time()
while len(traversal_graph.vertices) < 500:
    # get room data for romm I am in
    init_response = get_init_response()
    # get exits for room I am in
    exits = init_response['exits']
    # build array for unexplord exits
    unexplored = [option for option in exits if (
        traversal_graph.vertices[init_response['room_id']]['exits'][option] == '?')]
    # for each unexplored exit
    if len(unexplored) > 0:
        # pick an exit at random
        move = random.choice(unexplored)
        # get response back from move made
        move_response = make_move(move)
        counter += 1
        # get room id of room moved to
        post_move_room_id = move_response['room_id']
        if post_move_room_id not in traversal_graph.vertices:
            traversal_graph.add_vertex(move_response)
            print(
                f"{len(traversal_graph.vertices)} rooms found in {counter} moves and {time() - start_time} seconds.")
            with open(os.path.join(dirname, 'traversal_graph.txt'), 'w') as outfile:
                json.dump(traversal_graph.vertices, outfile)
        # connect room came from to room moved to
        traversal_graph.add_edge(init_response, move_response, move)
    else:
        to_unexplored = traversal_graph.bfs_to_unexplored(init_response)
        for move in to_unexplored:
            make_move(move)
            counter += 1


with open(os.path.join(dirname, 'traversal_graph_complete.txt'), 'w') as outfile:
    json.dump(traversal_graph.vertices, outfile)