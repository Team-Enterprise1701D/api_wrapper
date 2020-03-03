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

class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

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


    def dft_to_unexplored(self):
        print('*********************starting dft**********************')
        # get whatever room your are starting your dft in.
        init_response = get_init_response() 
        #create a stack
        stack = Stack()
        #place the starting room from the enpoint response
        stack.push(init_response['room_id'])
        # make a count to keep track of the first move, you don't want to move the player the first time through the loop, becayse the player is already in the first room.
        count = 0
        # update every i move, saving it here just in case i need it.
        move = None
        #this way i set the direction to whatever the last diection is gone on the stack
        direction = None
        previous_init = None
        while stack.size() > 0:
            # pull the first room out of the stack
            print('count', count)
            current_room = stack.pop()
            print('current_room', current_room)
            #get the previous room that the player is currently in before you move them to the room you just popped off.
            response = get_init_response()
            print('previous_init', previous_init)
            print('response', response)
            # if it is the not first time through the loop move the plaer to the current room from the stack.

            # check to see if the popped off room is in self.vertices dict.
            if current_room not in self.vertices:
                # if the count = 0 don't move your player because you are already in the first room.
                if count == 0:
                    # add room into the vertices dictionary of rooms.
                    # print("*****************testing to see if this hits here************")
                    self.add_vertex(response)
                    #add to text file
                    # f.write(f'{traversal_graph.vertices}')
                if count > 0:
                    # add room into the vertices dictionary of rooms.
                    self.add_vertex(move)
                    # add the room connection forwards and backwards.
                    self.add_edge(previous_init, move, direction)
                    print('*************checking edges added correctly**************')
                    print(self.vertices[current_room]['exits'])
                    #add to text file
                    # f.write(f'{traversal_graph.vertices}')
            # add to the count to keep track of when a player can move.
            count += 1
            # print('second check on count', count)

            # checking to see if we hit a dead end
            # creating a set to more easily check for ? rooms
            dead_end_check = set()
            # loop through the exits to get the value
            for ex in self.vertices[current_room]['exits']:
                # print('ex', self.vertices[current_room]['exits'][ex])
                dead_end_check.add(self.vertices[current_room]['exits'][ex])
            # check for un-explored exits "?" if none, then you have hit a dead end.
            print('check for dead end', dead_end_check)
            if '?' not in dead_end_check:
                # return the room_id/current_room so that the bfs traversal has a starting room id. 
                return current_room
            
            #store the room info in a list
            room_info = list()
            # store all the directions in a list
            temp_directions = list()
            # get all the exit values
            exit_vals = self.vertices[current_room]['exits']
            unexplored = [option for option in exit_vals if (
                traversal_graph.vertices[current_room]['exits'][option] == '?')]
            print('unexplored', unexplored)
            #chose a random directon to travel in
            direction = random.choice(unexplored)
            print('direction', direction)
            # set the next room to be the room you travel to.
            previous_init = response
            move = make_move(direction)

            # put the next room on the stack.
            stack.push(move['room_id'])
            
            
        
        
    def bfs_backtrack(self, starting_room):
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
            # check to see if the current room has any exits with a '?'
            unexplored_check = set()
            # loop through the exits to get the value
            for ex in self.vertices[current_room]['exits']:
                # print('ex', self.vertices[current_room]['exits'][ex])
                unexplored_check.add(self.vertices[current_room]['exits'][ex])
            # check for un-explored exits "?" if none, then you have hit a dead end.
            print('check for unexplored', unexplored_check)
            if '?' in unexplored_check:
                # return the path so that the revers path function can move to the last room that has unexplored exits
                return path

            # else mark this as visited
            visited.add(current_room)
            # get the neighbors
            edges = self.vertices[current_room]['exits']
            # print('edges', edges)
            # for each one, ad a Path To IT to the queue
            for edge in edges:
                    new_path = list(path)
                    new_path.append(self.vertices[current_room]['exits'][edge])
                    queue.enqueue(new_path)

    def reverse_travel(self, path):  # PROBABLY DON"T NEED ###
        temp_path = []
        print('*******************traveling back to closest room with unexplored exit')
        for id in range(len(path) - 1):
            # print(path[id])
            if path[id] in self.vertices:
                # print(room_graph[path[id]])
                for d in self.vertices[path[id]]['exits']:
                    # print('d', d)
                    if self.vertices[path[id]]['exits'][d] == path[id + 1]:

                        temp_path.append(d)
        print('reverse travel path', temp_path)
        for idx in range(len(temp_path)):
            make_wise_move(temp_path[idx], f'{path[idx +1]}')
    
    def travel_the_graph(self):
        guess = False
        while guess == False:
            print(f'there are {len(self.vertices)} rooms visited')
            guess = True
            room = self.dft_to_unexplored()
            if len(self.vertices) < 500:
                path = self.bfs_backtrack(room)
                self.reverse_travel(path)
                guess = False

       


#  method to get and return data from room I am in
def get_init_response():
    init_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/init/"
    init_headers = {
        "Authorization": f"Token 5740acca65a9d61760e99fb06308fe18cbf29a3c"}  # probably need a config file here
    # convert json to python object
    init_response = json.loads(requests.get(
        init_endpoint, headers=init_headers).content)
    # sleep for cooldown time recieved in response
    sleep(init_response['cooldown'])
    return init_response  # and free to make another request right away


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

def make_wise_move(move, room):
    move_endpoint = "https://lambda-treasure-hunt.herokuapp.com/api/adv/move/"
    move_headers = {"Content-Type": "application/json",
                    "Authorization": f"Token 5740acca65a9d61760e99fb06308fe18cbf29a3c"}  # and here
    move_direction = {"direction": move, "next_room_id": room}
    move_response = json.loads(requests.post(
        move_endpoint, data=json.dumps(move_direction), headers=move_headers).content)
    # sleep for period of time received in move_response
    sleep(move_response['cooldown'])
    return move_response



traversal_graph = Traversal_Graph()  # instantiate

f = open('dark_world_graph.txt', 'a')

# init_response = get_init_response()  # invoke init and receive response

traversal_graph.travel_the_graph()
print('the amount of rooms vsisted on first dft pass', len(traversal_graph.vertices))
print('finished traversal')



# print('traversal_graph', traversal_graph.vertices)
f.write(f'{traversal_graph.vertices}')
f.close()

# f = open('traversal_graph.txt', 'r')
# print(f)