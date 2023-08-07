import numpy as np
import pygame
import random
import pprint


def create_graph(width, height, start_node, end_node):

    dictionary_graph = {"start_node": start_node,
                        "current_node": start_node,
                        "end_node": end_node,
                        "unexplored_nodes": [],
                        "explored_nodes": []
                        }

    for i in range(width):
        for j in range(height):
            dictionary_graph[str(i) + str(j)] = {
                'adjacency_list': {},
                'previous_node': '',
                'distance_from_start': '?'
            }
            dictionary_graph['unexplored_nodes'].append(str(i)+str(j))

    # pprint.pprint(dictionary_graph)
    return dictionary_graph


def maze_foundations(width, height):
    return np.zeros((width, height), dtype=int)


def draw_bottom_layer(bottom_layer):
    for i in range(10):
        for b in range(10):
            rect = (b * 64, i * 64, 64, 64)
            if b % 2 == 0:
                # If i is a even number
                if i % 2 == 0:
                    pygame.draw.rect(bottom_layer, (255, 0, 0), rect)
                else:
                    pygame.draw.rect(bottom_layer, (0, 255, 0), rect)
            # If b is NOT an even number
            else:
                # If i is an even number
                if i % 2 == 0:
                    pygame.draw.rect(bottom_layer, (0, 255, 0), rect)
                else:
                    pygame.draw.rect(bottom_layer, (255, 0, 0), rect)


def set_base_walls(wall_array):
    for i in range(10):
        for b in range(10):
            height = 8
            if i == 0:
                wall = (b * 64, i * 64 - 8, 64, 16)
                wall_array.append(wall)
            if b == 9:
                wall = ((b * 64) + 56, i * 64, 16, 64)
                wall_array.append(wall)
            wall = (b * 64 - (height / 2), i * 64, height, 64)
            wall_array.append(wall)
            wall = (b * 64, (i * 64) + (64 - height / 2), 64, height)
            wall_array.append(wall)


def draw_walls(bottom_layer, walls):
    for wall in walls:
        pygame.draw.rect(bottom_layer, (0, 0, 255), wall)


def find_adjacent_cells(maze_width, maze_height, cell_x, cell_y):
    adjacency_list = []
    # Left
    if cell_x != 0:
        adjacent_x = cell_x - 1
        adjacent_y = cell_y

        adjacency_list.append((adjacent_x, adjacent_y))
    # Right
    if cell_x != maze_width - 1:
        adjacent_x = cell_x + 1
        adjacent_y = cell_y

        adjacency_list.append((adjacent_x, adjacent_y))
    # Bottom
    if cell_y != 0:
        adjacent_x = cell_x
        adjacent_y = cell_y - 1

        adjacency_list.append((adjacent_x, adjacent_y))
    # Top
    if cell_y != maze_height - 1:
        adjacent_x = cell_x
        adjacent_y = cell_y + 1

        adjacency_list.append((adjacent_x, adjacent_y))
    return adjacency_list


def bfs(start_node, end_node, dictionary_graph):
    cell_x = start_node[0]
    cell_y = start_node[1]
    visited = [(cell_x, cell_y)]
    queue = [start_node]
    # find adjacent cell to current cell
    maze[cell_x, cell_y] = 1  # Sets start node as 1
    while len(queue) > 0:
        cell = queue.pop()
        if cell == end_node:
            break
        adjacency_list = find_adjacent_cells(10, 10, cell[0], cell[1])

        # search if any of those adjacent cells are already visited
        # if they are, remove them from the adjacent cell variable

        adjacency_list = [node for node in adjacency_list if node not in visited]  # We need this because we cant
        # remove an element while iterating through a list in python

        visited.extend(adjacency_list)
        wall_height = 8  # height of the walls positioned on the top and bottom of cells
        wall_width = 8  # Width of the walls positioned on the left and right of the cells
        while len(adjacency_list) > 0:
            chosen_cell = random.choice(adjacency_list)
            adjacency_list.remove(chosen_cell)
            queue.append(chosen_cell)
            chosen_cell_x = chosen_cell[0]
            chosen_cell_y = chosen_cell[1]
            maze[chosen_cell_x, chosen_cell_y] = 1

            dictionary_graph[str(chosen_cell_x)+str(chosen_cell_y)]['adjacency_list'][str(cell[0])+str(cell[1])] = 1

            # Removing the walls from the wall_object array depending on the cell we visit.
            if chosen_cell[0] > cell[0]:
                wall_objects.remove(((chosen_cell[0] * 64 - wall_width / 2), chosen_cell[1] * 64, wall_width, 64))
            elif chosen_cell[0] < cell[0]:
                wall_objects.remove(((cell[0] * 64 - wall_width / 2), cell[1] * 64, wall_width, 64))
            elif chosen_cell[1] > cell[1]:
                wall_objects.remove((chosen_cell[0] * 64, chosen_cell[1] * 64 - (wall_height / 2), 64, wall_height))
            elif chosen_cell[1] < cell[1]:
                wall_objects.remove((cell[0] * 64, cell[1] * 64 - (wall_height / 2), 64, wall_height))

    pprint.pprint(dictionary_graph)


graph = create_graph(10, 10, 0, 9)
maze = maze_foundations(10, 10)
size = (640, 640)
layer = pygame.Surface(size)
wall_objects = []
wall_layer = pygame.Surface(size)
set_base_walls(wall_objects)
bfs((0, 0), (9, 9), graph)
draw_walls(wall_layer, wall_objects)
screen = pygame.display.set_mode(size)
draw_bottom_layer(layer)
screen.blit(layer, (0, 0))
screen.blit(wall_layer, (0, 0))
playing = True

while playing:
    if pygame.event.get(pygame.QUIT):
        playing = False

    # Update the display
    pygame.display.update()
