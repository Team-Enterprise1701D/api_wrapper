import requests
import json
import random
from time import sleep, time
import os
from ast import literal_eval

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

map_file = "traversal_graph.txt" 
room_graph=literal_eval(open(map_file, "r").read())
# print('room_graph', room_graph)

starting_room = list(room_graph.keys())[-1]
traversal_path = []
print('starting_room', starting_room)
class Traversal:
    def __init__(self):
        self.visited = set()
    def bfs_back_to_room_0(self, starting_room, destination_room):
         # make a queue
        queue = Queue()
        # make a set for visited
        visited = set()
        # enqueues a Path To the starting_vertex
        queue.enqueue([starting_room])
        # while queue isn't empty:
        while queue.size() > 0:
            # dequeue the next path
            path = queue.dequeue()
            # current_node is the last thing in the path
            current_room = path[-1]
            # check if its the target, aka the destination_vertex
            if current_room is destination_room:
            # if so, return path
                print('final_path', path)
                return path
            # else mark this as visited
            visited.add(current_room)
            # get the neighbors
            edges = room_graph[current_room]['exits']
            # print('edges', edges)
            # for each one, ad a Path To IT to the queue
            for edge in edges:
                if room_graph[current_room]['exits'][edge] != '?':
                    new_path = list(path)
                    new_path.append(room_graph[current_room]['exits'][edge])
                    queue.enqueue(new_path)

    def reverse_path(self, path):  # PROBABLY DON"T NEED ###
        temp_path = []
        for id in range(len(path) - 1):
            # print(path[id])
            if path[id] in room_graph:
                # print(room_graph[path[id]])
                for d in room_graph[path[id]]['exits']:
                    # print('d', d)
                    if room_graph[path[id]]['exits'][d] == path[id + 1]:

                        temp_path.append(d)

        for d in temp_path:
            traversal_path.append(d)

def make_move(move):
    move_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    move_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token 5740acca65a9d61760e99fb06308fe18cbf29a3c"}  # and here
    move_direction = {"direction": move}
    move_response = json.loads(requests.post(
        move_endpoint, data=json.dumps(move_direction), headers=move_headers).content)
    # sleep for period of time received in move_response
    sleep(move_response['cooldown'])
    return move_response

trav = Traversal()

current_path = trav.bfs_back_to_room_0(starting_room, 0)
moves = trav.reverse_path(current_path)
print('traversal_path',traversal_path)

for move in traversal_path:
    make_move(move)