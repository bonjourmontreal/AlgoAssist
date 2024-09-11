import pygame
from queue import PriorityQueue
import math
from .constants import *
from ui import COLORS

# Base class for pathfinding algorithms
class PathfindingAlgorithm:
    def __init__(self, grid):
        self.grid = grid

# A* algorithm 
class AStarAlgorithm(PathfindingAlgorithm):
    def __init__(self, grid, heuristic):
        super().__init__(grid)
        self.heuristic = heuristic

    def find_path(self, start_cell, end_cell, draw_callback):
        count = 0 
        open_set = PriorityQueue()  # Priority queue for open nodes
        open_set.put((0, count, start_cell)) 
        open_set_hash = {start_cell}  # Set to keep track of nodes in the open set
        
        # Initialize g_score and f_score dictionaries
        g_score = {cell: float("inf") for row in self.grid for cell in row}
        f_score = {cell: float("inf") for row in self.grid for cell in row}
        came_from = {}
        
        g_score[start_cell] = 0
        f_score[start_cell] = self.heuristic(start_cell.get_pos(), end_cell.get_pos())

        nodes_visited = 0  # Counter for nodes visited
        
        while not open_set.empty():
            current_cell = open_set.get()[2]
            open_set_hash.remove(current_cell)
            nodes_visited += 1  # Increment nodes visited count

            if current_cell == end_cell:
                end_cell.make_end()
                path_length = self.reconstruct_path(came_from, end_cell, draw_callback)
                start_cell.make_start()
                print(f"Pathfinding completed. Nodes visited: {nodes_visited}, Path length: {path_length}")

                return nodes_visited, path_length

            for neighbor in current_cell.valid_neighbors:
                temp_g_score = g_score[current_cell] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_cell
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor.get_pos(), end_cell.get_pos())

                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open()

            draw_callback()

            if current_cell != start_cell:
                current_cell.make_closed()

        return nodes_visited, 0

    def reconstruct_path(self, came_from, current_cell, draw_callback):
        path_length = 0  # Initialize path length counter
        while current_cell in came_from:
            current_cell = came_from[current_cell]
            current_cell.make_path()
            path_length += 1  # Increment path length
            draw_callback()
        return path_length

# Breadth-First Search (BFS) algorithm
class BFSAlgorithm(PathfindingAlgorithm):
    def find_path(self, start_cell, end_cell, draw_callback):
        queue = [start_cell]
        came_from = {}
        visited = {start_cell}

        nodes_visited = 0  # Counter for nodes visited

        while queue:
            current_cell = queue.pop(0)
            nodes_visited += 1  # Increment nodes visited count

            if current_cell == end_cell:
                end_cell.make_end()
                path_length = self.reconstruct_path(came_from, end_cell, draw_callback)
                start_cell.make_start()
                print(f"Pathfinding completed. Nodes visited: {nodes_visited}, Path length: {path_length}")

                return nodes_visited, path_length

            for neighbor in current_cell.valid_neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    came_from[neighbor] = current_cell
                    queue.append(neighbor)
                    visited.add(neighbor)
                    neighbor.make_open()

            draw_callback()

            if current_cell != start_cell:
                current_cell.make_closed()

        return nodes_visited, 0

    def reconstruct_path(self, came_from, current_cell, draw_callback):
        path_length = 0  # Initialize path length counter
        while current_cell in came_from:
            current_cell = came_from[current_cell]
            current_cell.make_path()
            path_length += 1  # Increment path length
            draw_callback()
        return path_length

# Depth-First Search (DFS) algorithm
class DFSAlgorithm(PathfindingAlgorithm):
    def find_path(self, start_cell, end_cell, draw_callback):
        stack = [start_cell]
        came_from = {}
        visited = {start_cell}

        nodes_visited = 0  # Counter for nodes visited

        while stack:
            current_cell = stack.pop()
            nodes_visited += 1  # Increment nodes visited count

            if current_cell == end_cell:
                end_cell.make_end()
                path_length = self.reconstruct_path(came_from, end_cell, draw_callback)
                start_cell.make_start()
                print(f"Pathfinding completed. Nodes visited: {nodes_visited}, Path length: {path_length}")

                return nodes_visited, path_length

            for neighbor in current_cell.valid_neighbors:
                if neighbor not in visited and not neighbor.is_barrier():
                    came_from[neighbor] = current_cell
                    stack.append(neighbor)
                    visited.add(neighbor)
                    neighbor.make_open()

            draw_callback()

            if current_cell != start_cell:
                current_cell.make_closed()

        return nodes_visited, 0

    def reconstruct_path(self, came_from, current_cell, draw_callback):
        path_length = 0  # Initialize path length counter
        while current_cell in came_from:
            current_cell = came_from[current_cell]
            current_cell.make_path()
            path_length += 1  # Increment path length
            draw_callback()
        return path_length

# Greedy Best-First Search (GBFS) algorithm (uses heuristic only)
class GBFSAlgorithm(PathfindingAlgorithm):
    def __init__(self, grid, heuristic):
        super().__init__(grid)
        self.heuristic = heuristic

    def find_path(self, start_cell, end_cell, draw_callback):
        count = 0  # This will act as a tie-breaker in the PriorityQueue
        open_set = PriorityQueue()  # Priority queue for open nodes
        open_set.put((0, count, start_cell))
        open_set_hash = {start_cell}  # Set to keep track of nodes in the open set
        closed_set = set()  # Set to keep track of nodes that have been visited and processed
        came_from = {}

        nodes_visited = 0  # Counter for nodes visited

        while not open_set.empty():
            current_cell = open_set.get()[2]  # Get the cell with the highest priority (lowest heuristic)
            open_set_hash.remove(current_cell)
            nodes_visited += 1  # Increment nodes visited count

            if current_cell == end_cell:
                # Path found, reconstruct it
                end_cell.make_end()
                path_length = self.reconstruct_path(came_from, end_cell, draw_callback)
                start_cell.make_start()
                print(f"Pathfinding completed. Nodes visited: {nodes_visited}, Path length: {path_length}")
                return nodes_visited, path_length

            closed_set.add(current_cell)  # Mark this node as processed

            for neighbor in current_cell.valid_neighbors:
                if neighbor not in open_set_hash and neighbor not in closed_set and not neighbor.is_barrier():
                    came_from[neighbor] = current_cell
                    priority = self.heuristic(neighbor.get_pos(), end_cell.get_pos())
                    count += 1  # Increment count for tie-breaking
                    open_set.put((priority, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

            draw_callback()

            if current_cell != start_cell:
                current_cell.make_closed()

        print("No path found.")
        return nodes_visited, 0

    def reconstruct_path(self, came_from, current_cell, draw_callback):
        path_length = 0  # Initialize path length counter
        while current_cell in came_from:
            current_cell = came_from[current_cell]
            current_cell.make_path()
            path_length += 1  # Increment path length
            draw_callback()
        return path_length

# Jump Point Search (JPS) algorithm
class JPSAlgorithm(PathfindingAlgorithm):
    def __init__(self, grid, heuristic):
        super().__init__(grid)
        self.heuristic = heuristic

    def find_path(self, start_cell, end_cell, draw_callback):
        count = 0
        open_set = PriorityQueue()  # Priority queue for open nodes
        open_set.put((0, count, start_cell))
        open_set_hash = {start_cell}  # Set to keep track of nodes in the open set
        came_from = {}

        g_score = {cell: float("inf") for row in self.grid for cell in row}
        g_score[start_cell] = 0

        nodes_visited = -1  # Start at -1 to account for off-by-one error

        while not open_set.empty():
            current_cell = open_set.get()[2]
            open_set_hash.remove(current_cell)
            nodes_visited += 1  # Increment nodes visited count

            if current_cell == end_cell:
                end_cell.make_end()
                path_length, number_of_jumps = self.reconstruct_path(came_from, start_cell, end_cell, draw_callback)
                start_cell.make_start()
                print(f"Pathfinding completed. Nodes visited: {nodes_visited}, Number of jumps: {number_of_jumps + 1}, Path length: {path_length}")
                return nodes_visited, path_length

            neighbors = self.get_neighbors(current_cell, start_cell, end_cell)

            for neighbor in neighbors:
                tentative_g_score = g_score[current_cell] + self.distance(current_cell, neighbor)

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_cell
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor.get_pos(), end_cell.get_pos())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score, count, neighbor))
                        open_set_hash.add(neighbor)

            draw_callback()

            if current_cell != start_cell:
                current_cell.make_closed()

        print("No path found.")
        return nodes_visited, 0

    def get_neighbors(self, current_cell, start_cell, end_cell):
        neighbors = []
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, down, left, right
            jump_point = self.jump(current_cell, direction, end_cell)
            if jump_point:
                neighbors.append(jump_point)
        return neighbors

    def jump(self, current_cell, direction, end_cell):
        next_col = current_cell.col + direction[0]
        next_row = current_cell.row + direction[1]

        if not (0 <= next_col < COLS and 0 <= next_row < ROWS):
            return None  # Out of bounds

        next_cell = self.grid[next_row][next_col]

        if next_cell.is_barrier():
            return None  # Hit a barrier

        if next_cell == end_cell:
            return next_cell  # Reached the goal

        # Horizontal or vertical jumps
        if direction[0] != 0 and direction[1] == 0:  # Horizontal
            if (self.is_walkable(next_col, next_row - 1) and not self.is_walkable(next_col - direction[0], next_row - 1)) or \
               (self.is_walkable(next_col, next_row + 1) and not self.is_walkable(next_col - direction[0], next_row + 1)):
                return next_cell

        if direction[1] != 0 and direction[0] == 0:  # Vertical
            if (self.is_walkable(next_col - 1, next_row) and not self.is_walkable(next_col - 1, next_row - direction[1])) or \
               (self.is_walkable(next_col + 1, next_row) and not self.is_walkable(next_col + 1, next_row - direction[1])):
                return next_cell

        return self.jump(next_cell, direction, end_cell)

    def is_walkable(self, col, row):
        if 0 <= col < COLS and 0 <= row < ROWS:
            return not self.grid[row][col].is_barrier()
        return False

    def distance(self, cell1, cell2):
        return int(math.sqrt((cell1.col - cell2.col) ** 2 + (cell1.row - cell2.row) ** 2))

    def reconstruct_path(self, came_from, start_cell, end_cell, draw_callback):
        path = []
        current_cell = end_cell
        number_of_jumps = 0

        while current_cell != start_cell:
            path.append(current_cell)
            current_cell = came_from[current_cell]

        path.append(start_cell)  # Ensure the start cell is included
        path.reverse()

        # Draw the path neighbor by neighbor
        full_path_length = 0
        for i in range(1, len(path)):
            if path[i] != end_cell:
                if self.is_jump(path[i - 1], path[i]):
                    path[i].color = COLORS["PINK"]  # Color jump points on the path as pink
                    number_of_jumps += 1  # Count this as a jump in the final path
                else:
                    path[i].make_path()  # Color regular path as purple
            self.draw_full_path(path[i - 1], path[i], draw_callback)
            full_path_length += self.distance(path[i - 1], path[i])

        return full_path_length, number_of_jumps

    def draw_full_path(self, from_cell, to_cell, draw_callback):
        step_col = to_cell.col - from_cell.col
        step_row = to_cell.row - from_cell.row

        col_increment = 1 if step_col > 0 else -1 if step_col < 0 else 0
        row_increment = 1 if step_row > 0 else -1 if step_row < 0 else 0

        current_col = from_cell.col
        current_row = from_cell.row

        while (current_col, current_row) != (to_cell.col, to_cell.row):
            current_col += col_increment
            current_row += row_increment
            cell = self.grid[current_row][current_col]
            if cell != to_cell and cell.color != COLORS["PINK"]:  # Avoid overwriting the pink jumps
                cell.make_path()
            draw_callback()

    def is_jump(self, from_cell, to_cell):
        return abs(from_cell.col - to_cell.col) > 1 or abs(from_cell.row - to_cell.row) > 1

# Bidirectional A* Search algorithm
class BiAStarAlgorithm(PathfindingAlgorithm):
    def __init__(self, grid, heuristic):
        super().__init__(grid)
        self.heuristic = heuristic

    def find_path(self, start_cell, end_cell, draw_callback, delay=0):  # Added delay parameter
        count = 0
        open_set_start = PriorityQueue()  # Priority queue for nodes from start to goal
        open_set_goal = PriorityQueue()   # Priority queue for nodes from goal to start
        open_set_start.put((0, count, start_cell))
        open_set_goal.put((0, count, end_cell))
        came_from_start = {}
        came_from_goal = {}
        open_set_hash_start = {start_cell}
        open_set_hash_goal = {end_cell}

        g_score_start = {cell: float("inf") for row in self.grid for cell in row}
        g_score_goal = {cell: float("inf") for row in self.grid for cell in row}
        g_score_start[start_cell] = 0
        g_score_goal[end_cell] = 0

        nodes_visited = 0  # Counter for nodes visited

        while not open_set_start.empty() and not open_set_goal.empty():
            current_cell_start = open_set_start.get()[2]
            open_set_hash_start.remove(current_cell_start)
            current_cell_goal = open_set_goal.get()[2]
            open_set_hash_goal.remove(current_cell_goal)
            nodes_visited += 1  # Increment nodes visited count

            # Add a delay to visualize the process
            pygame.time.delay(delay)
            draw_callback()

            # Check if the search fronts meet
            if current_cell_start in open_set_hash_goal or current_cell_goal in open_set_hash_start:
                # Path found
                intersection = current_cell_start if current_cell_start in open_set_hash_goal else current_cell_goal
                path_length = self.reconstruct_path(came_from_start, came_from_goal, start_cell, end_cell, intersection, draw_callback)
                start_cell.make_start()
                end_cell.make_end()
                print(f"Pathfinding completed. Nodes visited: {nodes_visited}, Path length: {path_length}")
                return nodes_visited, path_length

            # Explore neighbors for the start side
            for neighbor in current_cell_start.valid_neighbors:
                tentative_g_score = g_score_start[current_cell_start] + 1

                if tentative_g_score < g_score_start[neighbor]:
                    came_from_start[neighbor] = current_cell_start
                    g_score_start[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor.get_pos(), end_cell.get_pos())
                    if neighbor not in open_set_hash_start:
                        count += 1
                        open_set_start.put((f_score, count, neighbor))
                        open_set_hash_start.add(neighbor)
                        neighbor.make_open()

            # Explore neighbors for the goal side
            for neighbor in current_cell_goal.valid_neighbors:
                tentative_g_score = g_score_goal[current_cell_goal] + 1

                if tentative_g_score < g_score_goal[neighbor]:
                    came_from_goal[neighbor] = current_cell_goal
                    g_score_goal[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor.get_pos(), start_cell.get_pos())
                    if neighbor not in open_set_hash_goal:
                        count += 1
                        open_set_goal.put((f_score, count, neighbor))
                        open_set_hash_goal.add(neighbor)
                        neighbor.make_open()

            draw_callback()

            if current_cell_start != start_cell:
                current_cell_start.make_closed()
            if current_cell_goal != end_cell:
                current_cell_goal.make_closed()

        print("No path found.")
        return nodes_visited, 0
    
    def reconstruct_path(self, came_from_start, came_from_goal, start_cell, end_cell, intersection, draw_callback):
        # Reconstruct the path from start to intersection
        path = []
        current_cell = intersection

        while current_cell != start_cell:
            path.append(current_cell)
            current_cell = came_from_start[current_cell]

        path.append(start_cell)  # Ensure the start cell is included
        path.reverse()

        # Reconstruct the path from intersection to end
        current_cell = intersection

        while current_cell != end_cell:
            current_cell = came_from_goal[current_cell]
            path.append(current_cell)

        # Draw the path neighbor by neighbor
        full_path_length = 0
        for i in range(1, len(path)):
            path[i].make_path()
            draw_callback()
            full_path_length += 1

        return full_path_length
