from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []



# set up the reverse directions to go backwards through the graph to go back through the rooms to move out of again
backwards = []
go_back = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
# use a set to store all of the visited rooms inside of
visited = set()
# Use a loop to go through all of the rooms until every room is visited
while len(visited) < len(room_graph):
    # create a variable to use for our next player movement
    next_direction = None
     # loop through n, s, e, and w to find the exits of the room
    for exit in player.current_room.get_exits():
         # if the room has not been added to 'visited', set it to the next movement
         # loop will break because rooms have more than one exit
        if player.current_room.get_room_in_direction(exit) not in visited:
            next_direction = exit
            break
    # When there is a direction that is not None
    if next_direction is not None:
        # add the move to the traversal path
        traversal_path.append(next_direction)
        # add the backwards direction to the trail
        backwards.append(go_back[next_direction])
        # move the player and add the visited vertice to the set
        player.travel(next_direction)  
        visited.add(player.current_room)
    # if there is no move, we have to go back and find a move the player can make
    else:
        # remove the last thing entered from backwards
        next_direction = backwards.pop()
        # add that move to traversal path
        traversal_path.append(next_direction)
        # move the player
        player.travel(next_direction)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
