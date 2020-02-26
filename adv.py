import random


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


# our_map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
# room_graph=literal_eval(open(map_file, "r").read())
# world.load_graph(room_graph)

# # Print an ASCII map
# world.print_rooms()

# player = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


class Graph:
    def __init__(self):
        self.visited = {}
        self.visited_rooms = set()

    def bfs(self, starting_room):
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

            current_room = path[-1]
            num_curr_room = numPath[-1]

            for visit in self.visited[current_room.id]:
                if self.visited[current_room.id][visit] == '?':

                    traveled_path = numPath
                    last_room = current_room
                    return (last_room, numPath)

            player.current_room = current_room

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

    def reverse_path(self, path):  # PROBABLY DON"T NEED ###
        temp_path = []
        for id in range(len(path) - 1):
            # print(path[id])
            if path[id] in self.visited:
                for d in self.visited[path[id]]:
                    if self.visited[path[id]][d] == path[id + 1]:

                        temp_path.append(d)

        for d in temp_path:
            traversal_path.append(d)

    def dft(self, starting_room):

        stack = Stack()

        previous_room = None  # store room just came from

        stack.push(starting_room)

        while stack.size() > 0:
            current_room = stack.pop()
            # print('current_room_top', current_room.id)
            ### PERHAPS CREATE CUSTOM PLAYER CLASS ###
            player.current_room = current_room  # THIS NEEDS TO BE LOOKED AT !!!!!
            self.visited_rooms.add(current_room)

            if current_room.id not in self.visited:

                exit_dict = {}  # for N, S, E, W values

                exits = current_room.get_exits()

                for ex in exits:
                    exit_dict[ex] = '?'

                self.visited[current_room.id] = exit_dict

            first_directions = set()
            for emp in self.visited[current_room.id]:

                first_directions.add(self.visited[current_room.id][emp])

            if '?' not in first_directions:
                for d in self.visited[previous_room]:
                    if self.visited[previous_room][d] == current_room.id:
                        traversal_path.append(d)    # MIGHT NOT NEED THIS!

                return current_room

            count = 0
            for visit in self.visited[current_room.id].copy():
                # print('current_room in middle plus', self.visited[current_room.id][visit])
                # print('count', count)
                if count > 0:
                    pass
                elif self.visited[current_room.id][visit] == '?':
                    count += 1

                    for vis in self.visited:

                        for d in self.visited[vis]:

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

                    temp_diretions = set()
                    for emp in self.visited[current_room.id]:

                        temp_diretions.add(self.visited[current_room.id][emp])

                    if '?' not in temp_diretions:

                        return current_room

                    temp_dir = list()
                    temp_room = list()
                    ex = self.visited[current_room.id]

                    for e in ex:
                        if self.visited[current_room.id][e] == '?':

                            player.travel(f'{e}')
                            next_room = player.current_room
                            temp_dir.append(e)
                            temp_room.append(next_room.id)

                            if e == 'n':
                                player.travel('s')
                            if e == 's':
                                player.travel('n')
                            if e == 'e':
                                player.travel('w')
                            if e == 'w':
                                player.travel('e')

                            stack.push(next_room)

                    self.visited[current_room.id][f'{temp_dir[-1]}'] = temp_room[-1]

                previous_room = current_room.id

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
print('traversal_path', traversal_path)
