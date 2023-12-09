from queue import PriorityQueue
import functools

# https://bugs.python.org/issue31145
@functools.total_ordering
class Prio:
    def __init__(self, f, node):
        self.f = f
        self.node = node

    def __eq__(self, other):
        return self.f == other.f

    def __lt__(self, other):
        return self.f < other.f


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


# https://en.wikipedia.org/wiki/A*_search_algorithm
def astar(start, adjacent, h, is_target) -> list:
    open_queue = PriorityQueue()
    open_queue.put(Prio(0, start))
    open_set = set([start])
    came_from = dict()
    g_score = {start: 0}

    while not open_queue.empty():
        current = open_queue.get()
        open_set.remove(current.node)

        if is_target(current.node):
            return reconstruct_path(came_from, current.node)

        for time, child in adjacent(current.node):
            g = g_score[current.node] + time
            if child not in g_score or g < g_score[child]:
                came_from[child] = current.node
                g_score[child] = g
                f = g + h(child)
                if child not in open_set:
                    open_set.add(child)
                    open_queue.put(Prio(f, child))
