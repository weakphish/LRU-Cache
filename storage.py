"""
Implement a data storage class that is backed by an in-memory LRU cache.
"""

from typing import Any


class Node:
    """Node object for implementation in a doubly linked list."""

    def __init__(self, prev: "Node", next: "Node", key: Any, value: Any):
        self.prev = prev
        self.next = next
        self.key = key
        self.value = value
        self.references = 1


class LRUCache:
    """
    An in-memory LRU cache.

    The LRU Cache uses a doubly linked queue to keep track of the most recently used items.
    """

    def __init__(self, capacity: int):
        """Construct an LRU Cache."""
        self.head = None
        self.tail = None  # the tail will be the LRU item
        self.capacity = capacity
        self.size = 0

    def insert(self, key: Any, value: Any) -> Any:
        """
        Insert a Key/Value pair into storage.

        If the capacity of the cache is reached, evict the least recently used item.

        :return: The value of the item that was evicted, if any.

        """
        if self.head is None:
            # This value will be the new head & tail
            self.head = Node(None, None, key, value)
            self.tail = self.head
            self.size += 1
            return None

        evicted = None
        if self.size + 1 > self.capacity:
            # Evict the tail node
            tmp = self.tail
            self.tail = tmp.prev
            tmp.prev.next = self.tail
            self.tail.next = None
            self.size -= 1
            evicted = tmp.value 

        # insert new node at the head of the linked list
        new_head = Node(None, self.head, key, value)
        self.head.prev = new_head
        self.head = new_head
        self.size += 1
        return evicted

    def get(self, key):
        """
        Retrieve a value from storage.

        When a key is referenced, it will be moved to the front of the cache's
        backing linked list.

        :param key: The key of the item to retrieve.
        """
        # search cache
        node = self.head
        # special case: head of the list is our hit
        if node.key == key:
            return node.value

        while node.next is not None:
            node = node.next
            if node.key == key:
                # cache hit - move to front of list
                node.prev.next = node.next
                if node.next:
                    node.next.prev = node.prev
                node.prev = None
                node.next = self.head
                self.head.prev = node
                self.head = node
                return node.value

    def __str__(self):
        """Returns a string representation of the cache, for debugging purposes."""
        node = self.head
        buffer = ""
        while node is not None:
            buffer += f"({node.key}, {node.value})"
            node = node.next
            if node is not None:
                buffer += " -> "
        return buffer


def main():
    cache = LRUCache(3)
    cache.insert("a", 1)
    cache.insert("b", 2)
    cache.insert("c", 3)
    print("Cache after initial insertion:")
    print(cache)

    cache.get("b")
    print("Cache after get(b):")
    print(cache)

    cache.insert("d", 4)
    print("Cache after insert(d):")
    print(cache)

    cache.get("c")
    print("Cache after get(c):")
    print(cache)


if __name__ == "__main__":
    main()
