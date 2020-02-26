from room import Room
from player import Player
from world import World

import random
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

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

class Graph:
    def __init__(self):
        self.visited = {}
        self.visited_rooms = set()


    def bfs(self,starting_room):
        traveled_path = []
            
        queue = Queue()
        numQueue = Queue()

        visited = set()

        queue.enqueue([starting_room])
        # print('starting_room', starting_room)
        numQueue.enqueue([starting_room.id])

        previous_room = None

        last_room = None

        while queue.size() > 0:

            path = queue.dequeue()
            numPath = numQueue.dequeue()
            # print('path',numPath)

            current_room = path[-1]
            num_curr_room = numPath[-1]

            # print('current_room', current_room.id)
            # if current_room.id not in self.visited:
            #     # self.visited[current_room.id] = None
            #     # print('current_room last', previous_room.id)
            #     traveled_path = numPath
            #     last_room = current_room
            #     return (last_room, numPath)
            for visit in self.visited[current_room.id]:
                if self.visited[current_room.id][visit] == '?':
                    # print("visited", self.visited)
                    traveled_path = numPath
                    last_room = current_room
                    return (last_room, numPath)

            player.current_room = current_room
        
            # print('previous_room', previous_room)
            # print('current_room', current_room.id)
            

            if current_room not in visited:
                visited.add(current_room)


                neighboring_rooms = self.visited[current_room.id]


                for direction in neighboring_rooms:
                    player.travel(f'{direction}')
                    next_room = player.current_room
                    # print('next_room', next_room)
                    if direction == 'n':
                        player.travel('s')
                    if direction == 's':
                        player.travel('n')
                    if direction == 'e':
                        player.travel('w')
                    if direction == 'w':
                        player.travel('e')
                    new_path = list(path)
                    num_path = list(numPath)
                    new_path.append(next_room)
                    num_path.append(next_room.id)
                    queue.enqueue(new_path)
                    numQueue.enqueue(num_path)
                previous_room = current_room


        # return last_room



    def reverse_path(self, path):
        # print('************************************test********************************')
        temp_path = []       
        for id in range(len(path) - 1):
            # print(path[id])
            if path[id] in self.visited:
                for d in self.visited[path[id]]:
                    if self.visited[path[id]][d] == path[id + 1]:
                        # print(d)
                        # print(path[id + 1])
                        temp_path.append(d)
        # print('traveled_path', path)
        # print('temp_path', temp_path)
        for d in temp_path:
            traversal_path.append(d)

    def dft(self, starting_room):

        stack = Stack()

        previous_room = None

        stack.push(starting_room)

        while stack.size() > 0:
            current_room = stack.pop()
            # print('current_room_top', current_room.id) 
            player.current_room = current_room
            self.visited_rooms.add(current_room)



            if current_room.id not in self.visited:

                exit_dict = {}

                exits = current_room.get_exits()

                for ex in exits:
                    exit_dict[ex] = '?'

                self.visited[current_room.id] = exit_dict
                # print('visited after created', self.visited[current_room.id])
            # print('current_room_middle', current_room.id) 

            first_directions = set()
            for emp in self.visited[current_room.id]:
                # print(self.visited[current_room.id][emp])
                first_directions.add(self.visited[current_room.id][emp])
            # print('current_room',current_room.id)
            # print('current_room_directions', self.visited[current_room.id])
            # print('first_directions', first_directions)
            # print('rooms visited so far', len(self.visited_rooms))
            if '?' not in first_directions:
                for d in self.visited[previous_room]:
                    if self.visited[previous_room][d] == current_room.id:
                        traversal_path.append(d)
                # print('current_room in return', current_room)
                return current_room
            # print('current_room in middle', current_room.id)
            count = 0
            for visit in self.visited[current_room.id].copy():
                # print('current_room in middle plus', self.visited[current_room.id][visit])
                # print('count', count)
                if count > 0:
                    pass
                elif self.visited[current_room.id][visit] == '?':
                    count += 1
                    # print('**********checking empty dir**********', self.visited[current_room.id])
                    for vis in self.visited:
                        # print('vis',vis)
                        for d in self.visited[vis]:
                            # print(d)
                            if self.visited[vis][d] == current_room.id and vis == previous_room:
                                a = None
                                if d == 'n':
                                    a = 's'
                                if d == 'n':
                                    a = 's'
                                if d == 'e':
                                    a = 'w'
                                if d == 'w':
                                    a = 'e'
                                traversal_path.append(d)
                                if a is None:
                                    pass
                                elif a is not None:
                                    self.visited[current_room.id][a] = previous_room
                    # print('current_room in second middle', current_room.id)
                    temp_diretions = set()
                    for emp in self.visited[current_room.id]:
                        # print(self.visited[current_room.id][emp])
                        temp_diretions.add(self.visited[current_room.id][emp])
                    # print('current_room',current_room.id)
                    # print('current_room_directions', self.visited[current_room.id])
                    # print('temp_diretions', temp_diretions)
                    if '?' not in temp_diretions:
                        # print('current_room in return', current_room)
                        return current_room
                        # break
                    # print('visited after', self.visited)
                    temp_dir = list()
                    temp_room = list()
                    ex = self.visited[current_room.id]
                    # print('ex',ex)
                    for e in ex:
                        if self.visited[current_room.id][e] == '?':
                            # print('****************test********************')
                            # print('checking question', self.visited[current_room.id][e])
                            player.travel(f'{e}')
                            next_room = player.current_room
                            temp_dir.append(e)
                            temp_room.append(next_room.id)
                            # self.visited[current_room.id][f'{e}'] = next_room.id
                            if e == 'n':
                                player.travel('s')
                            if e == 's':
                                player.travel('n')
                            if e == 'e':
                                player.travel('w')
                            if e == 'w':
                                player.travel('e')
                            # print('next_room', next_room.id)
                            stack.push(next_room)
                        # print('temp, dir', temp_dir)
                        # print('temp_room', temp_room)
                    # print('count', count)
                    # print('current_room', current_room.id)
                    self.visited[current_room.id][f'{temp_dir[-1]}'] = temp_room[-1]
                # print('current room', current_room.id)
                # print('visited rooms',self.visited[current_room.id])
                # print('visited after direction loop', self.visited[current_room.id])
                # print('stack',stack.stack)
                previous_room = current_room.id
                # count += 1
                    
        # print('dft self.visited', self.visited)
    
    def traveling(self, starting_room):
        start = starting_room
        guess = False
        while guess == False:
            guess = True
            # print('**************starting dft***************')
            room = self.dft(start)
            # print('room', room)
            # print('traversal_path',traversal_path)
            if len(self.visited_rooms) < len(room_graph):
                # print('*******************starting bfs*********************************')
                check = self.bfs(room)
                # print('test check', check[1])
                # print('*******************reveral*********************************')
                self.reverse_path(check[1])
                # print('traversal_path',traversal_path)
                # print('check', check[0])
                start = check[0]
                for d in self.visited[check[0].id]:
                    if self.visited[check[0].id][d] == '?':
                        guess = False
            



graph = Graph()

visit = graph.traveling(world.starting_room)
print('traversal_path',traversal_path)