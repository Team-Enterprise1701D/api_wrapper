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
