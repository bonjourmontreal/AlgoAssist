import math

class Heuristic:
    @staticmethod
    def manhattan(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def euclidean(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    @staticmethod
    def diagonal(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return max(abs(x1 - x2), abs(y1 - y2))

    @staticmethod
    def dijkstra(p1, p2):
        # Normally, Dijkstra's algorithm would calculate based on edge weights.
        # However, for this app, no weights are assigned, so the heuristic remains 0.
        # This effectively turns Dijkstra's algorithm into BFS in this context.
        return 0
