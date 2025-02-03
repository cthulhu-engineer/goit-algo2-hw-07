from functools import lru_cache
import timeit
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, data, parent=None):
        self.key = key
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if self.find(key) is None:
            if self.root is None:
                self.root = Node(key, data)
            else:
                self._insert_node(key, data, self.root)

    def _insert_node(self, key, data, current_node):
        if key < current_node.key:
            if current_node.left_node:
                self._insert_node(key, data, current_node.left_node)
            else:
                current_node.left_node = Node(key, data, current_node)
        else:
            if current_node.right_node:
                self._insert_node(key, data, current_node.right_node)
            else:
                current_node.right_node = Node(key, data, current_node)

    def find(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left_node
            elif key > node.key:
                node = node.right_node
            else:
                self._splay(node)
                return node.data
        return None

    def _splay(self, node):
        while node.parent:
            if node.parent.parent is None:  # Zig
                if node == node.parent.left_node:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:  # Zig-Zig
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:  # Zig-Zig
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.right_node:  # Zig-Zag
                self._rotate_right(node.parent)
                self._rotate_left(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.left_node:  # Zig-Zag
                self._rotate_left(node.parent)
                self._rotate_right(node.parent)

    def _rotate_left(self, node):
        right_child = node.right_node
        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node
        right_child.parent = node.parent
        if not node.parent:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child
        right_child.left_node = node
        node.parent = right_child

    def _rotate_right(self, node):
        left_child = node.left_node
        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node
        left_child.parent = node.parent
        if not node.parent:
            self.root = left_child
        elif node == node.parent.right_node:
            node.parent.right_node = left_child
        else:
            node.parent.left_node = left_child
        left_child.right_node = node
        node.parent = left_child


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


def fibonacci_splay_tree(n, tree):
    cached_value = tree.find(n)
    if cached_value is not None:
        return cached_value

    if n < 2:
        result = n
    else:
        result = fibonacci_splay_tree(n - 1, tree) + fibonacci_splay_tree(n - 2, tree)

    tree.insert(n, result)
    return result


fib_values = list(range(0, 1000, 50))

lru_times = []
splay_times = []

for n in fib_values:
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=10) / 10
    lru_times.append(lru_time)

    splay_tree = SplayTree()
    splay_time = timeit.timeit(lambda: fibonacci_splay_tree(n, splay_tree), number=10) / 10
    splay_times.append(splay_time)

print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
print("-" * 50)
for i, n in enumerate(fib_values):
    print(f"{n:<10}{lru_times[i]:<20.8f}{splay_times[i]:<20.8f}")

plt.figure(figsize=(10, 6))
plt.plot(fib_values, lru_times, label="LRU Cache", marker='o')
plt.plot(fib_values, splay_times, label="Splay Tree", marker='s')
plt.xlabel("Fibonacci Number Index")
plt.ylabel("Time (s)")
plt.title("LRU Cache vs Splay Tree Performance")
plt.legend()
plt.grid(True)
plt.yscale("log")
plt.show()
