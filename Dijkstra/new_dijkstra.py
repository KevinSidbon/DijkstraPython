import json
import pprint

# Create a graph in the following dictionary form:

# 1) The graph needs to be a dictionary
# 2) The graph needs to hold the name of the nodes as keys of the dictionary
# 3) The graph needs to hold the value of the key as a dictionary containing:
#     a) An adjacent list
#     b) The previous node (where '' means that the previous node has not been found or doesn't exist)
#     c) the distance from the start node (where 0 is for the start node, and '?' is for unknown distances)

# Below is an example of a graph for reference

graph = {
    "A": {
        'adjacency_list': {"F": 2},
        'previous_node': '',
        'distance_from_start': '?'
    },
    "B": {
        'adjacency_list': {"A": 2},
        'previous_node': '',
        'distance_from_start': '?'
    },
    "C": {
        'adjacency_list': {"B": 2, "D": 4, "E": 2},
        'previous_node': '',
        'distance_from_start': 0
    },
    "D": {
        'adjacency_list': {"G": 1},
        'previous_node': '',
        'distance_from_start': '?'
    },
    "E": {
        'adjacency_list': {"F": 4},
        'previous_node': '',
        'distance_from_start': '?'
    },
    "F": {
        'adjacency_list': {},
        'previous_node': '',
        'distance_from_start': '?'
    },
    "G": {
        'adjacency_list': {"F": 1},
        'previous_node': '',
        'distance_from_start': '?'
    },
    "current_node": 'C',
    "start_node": 'C',
    "end_node": 'F',
    "unexplored_nodes": ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    "explored_nodes": []
}

p = pprint.PrettyPrinter()
p.pprint(graph)


# Create a function that will find each adjacent node (to the current node) 's distance from the start node.
def find_distance_from_start(dictionary_graph):
    # 1) Store Current Node from graph inside variable
    current_node = dictionary_graph['current_node']

    # 2) Store the adjacent nodes to the current node inside a variable (retrieve it from graph)
    adjacency_list = dictionary_graph[current_node]['adjacency_list']

    # 3) Loop through the adjacency list
    for node in adjacency_list:
        update_distance_from_start_and_previous_node(node, dictionary_graph)


# Create a function that will update the distance of a node to the start and set its previous node
def update_distance_from_start_and_previous_node(node, dictionary_graph):
    # 1) Create a variable to store the current node
    current_node = dictionary_graph['current_node']

    # 2) Create a variable that stores the current node's distance from the start
    current_node_distance_start = dictionary_graph[current_node]['distance_from_start']

    # 3) Create a variable to store the adjacent node's distance from the current node.
    adj_node_dist_from_current_node = dictionary_graph[current_node]['adjacency_list'][node]

    # 4) Create a variable that will store the distance of the adjacent node from the start
    temp_distance = adj_node_dist_from_current_node + current_node_distance_start

    # 5) Call the update_node_distance_from_start function
    update_node_distance_from_start(node, temp_distance, dictionary_graph)

    # 6) Call the update_previous_node function
    update_previous_node(node, dictionary_graph)


# Create a function that will return the boolean value to the answer: is the distance of a node unknown?
def is_distance_unknown(node, dictionary_graph):
    # this function simply returns a boolean that checks if distance is unknown (== '?')
    return dictionary_graph[node]['distance_from_start'] == '?'


# Create a function that will return the boolean value to the answer: is the new distance shorter?
def is_new_distance_shorter(node, temp_distance, dictionary_graph):
    # returns boolean and checks if the temp_distance is less than the current distance for the adjacent node
    return temp_distance < dictionary_graph[node]['distance_from_start']


# Create a function that will update a node's distance from the start
def update_node_distance_from_start(node, distance, dictionary_graph):
    # update the adjacent's node distance from start
    dictionary_graph[node]['distance_from_start'] = distance


# Create a function that will update the previous node for a specific adjacent node
def update_previous_node(adjacent_node, dictionary_graph):
    # update the previous node to the current node
    dictionary_graph[adjacent_node]['previous_node'] = dictionary_graph['current_node']


# Create a function that finds the closest unexplored node
def find_closest_unexplored_node(dictionary_graph):
    # 1) Create a variable to store the current closest node and give it a value of None
    current_closest_node = None
    # 2) Retrieve and store the unexplored nodes from the graph
    unexplored_nodes = dictionary_graph['unexplored_nodes']
    # 3) If the end node is not found (use function is_end_node_found):
    if not is_end_node_found(dictionary_graph):
        # If the end node is not found, then call the loop_and_choose_closest function. Store it's return value in a
        # variable (current_closest_node?)
        current_closest_node = loop_and_choose_closest(unexplored_nodes, current_closest_node, dictionary_graph)
    # 4) return current closest node
    return current_closest_node


# Create a function that will return the boolean value to the answer: is the end node found?
def is_end_node_found(dictionary_graph):
    # check if the current node is equals to the end node
    return dictionary_graph['current_node'] == dictionary_graph['end_node']


# Create a function that will loop through the unexplored nodes and return the closest one
def loop_and_choose_closest(unexplored_nodes, current_closest_node, dictionary_graph):
    # 1) create temp_distance variable and set to None
    temp_distance = None
    # 2) Loop through unexplored nodes
    for node in unexplored_nodes:
        # Make temp_distance == None
        # a) if is_node_closer_from_start returns true:
        if is_node_closer_from_start(temp_distance, node, dictionary_graph):
            # Make this node, the current node
            current_closest_node = node
            temp_distance = dictionary_graph[current_closest_node]['distance_from_start']

    # 3) return the current closest node
    return current_closest_node


# Create a function that returns the boolean answer for the question: is the node closer to the start?
def is_node_closer_from_start(temp_distance, node, dictionary_graph):
    # 1) Create a variable to store the node's distance from start
    node_distance_from_start = dictionary_graph[node]['distance_from_start']
    # 2) Check if temp_distance is None; in which case you return true
    if temp_distance is None and node_distance_from_start != '?':
        return True
    # 3) Otherwise, return the boolean value of: is the distance from start is '?' and the temp_distance is > than
    # distance from start.
    else:
        return node_distance_from_start != '?' and temp_distance > node_distance_from_start


# Create a function that updates the UNEXPLORED nodes
def update_unexplored_nodes(dictionary_graph):
    # Update the unexplored nodes (you can use the .remove function)
    dictionary_graph['unexplored_nodes'].remove(dictionary_graph['current_node'])


# Create a function that updates the EXPLORED nodes
def update_explored_nodes(dictionary_graph):
    # Update the explored nodes (you can use the .append function)
    dictionary_graph['explored_nodes'].append(dictionary_graph['current_node'])


# Create a function that sets the current node to be the closest node
def set_current_node(closest_node, dictionary_graph):
    # Set the current node to closest node
    dictionary_graph['current_node'] = closest_node


# Create a function that will find the path
def find_path(dictionary_graph):
    # Create a list to store the path
    path = []
    # Create a variable (current_node_path?) that will store the node as we walk through the path. Make it equals to
    # the end node at first
    current_node_path = dictionary_graph['end_node']
    # while the current node is not equals to '':
    while current_node_path != '':
        # append the current_node_path to the path
        path.append(current_node_path)
        # update the current_node_path and make equals to the previous node of our current_node_path
        current_node_path = dictionary_graph[current_node_path]['previous_node']

    # Return path
    return path


# Create a function that will print the path
def print_path(path):
    # while the length of the path is more than 0:
    while len(path) > 0:
        # pop() the last node our of the path list and store it in a variable
        node = path.pop()
        # print that variable
        print(node)


# Create a run function that takes in the graph
def run_me(dictionary_graph):
    # Create a loop that will repeat as long as the dictionary_graph's current node is not equals to the end node
    while dictionary_graph['current_node'] != dictionary_graph['end_node']:
        # 1) Find distance from start
        find_distance_from_start(dictionary_graph)
        # 2) Update the unexplored nodes
        update_unexplored_nodes(dictionary_graph)
        # 3) Update the explored nodes
        update_explored_nodes(dictionary_graph)
        # 4) Find the closest unexplored node and store it inside a variable
        closest_node = find_closest_unexplored_node(dictionary_graph)
        # 5) Set the current node to the closest node
        set_current_node(closest_node, dictionary_graph)

    # Once the graph has reached the end node, search for the path and store it inside a variable
    path_found = find_path(dictionary_graph)
    # Print the path out
    print_path(path_found)
    # This commented line below can help you print our the graph in a more readable fashion
    # print(json.dumps(graph, indent=4))


# Call the run function for the algorithm
run_me(graph)

# Challenges:
# 1) Handle the case when the end node is unreachable
# 2) Handle negative weights
# 3) Make sure your algorithm can handle a weight of 0
