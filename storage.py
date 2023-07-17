"""
Implement a data storage class that is backed by an in-memory LRU cache.
"""

from typing import Any
from collections import OrderedDict


class LRUCache:
    """
    An in-memory LRU cache.

    The LRU Cache uses a doubly linked queue to keep track of the most recently used 
    items.
    """

    def __init__(self, capacity: int):
        """Construct an LRU Cache."""
        self.capacity = capacity
        self.cache = OrderedDict()
        """
        Use an ordered dict, because as in the Python docs it's stated:
        "The OrderedDict algorithm can handle frequent reordering operations 
        better than dict."
        """

    def insert(self, key: Any, value: Any) -> Any:
        """
        Insert a Key/Value pair into storage.

        If the capacity of the cache is reached, evict the least recently used item.

        :return: The value of the item that was evicted, if any.
        """
        self.cache[key] = value  # the OrderedDict will guarantee order is preserved
        self.cache.move_to_end(
            key=key
        )  # move the item to the beginning (end) of the OrderedDict
        if len(self.cache) > self.capacity:
            return self.cache.popitem(last=False)
        
    def get(self, key: Any) -> Any:
        """
        Get a value from the cache.

        :param key: The key to retrieve the value of.
        :returns: The value of the key, or None if the key does not exist.
        """
        if key not in self.cache:
            return None
        
        # in this case, we're using the end as the "front" of the queue
        self.cache.move_to_end(key=key) 
        return self.cache[key]
    
    def __str__(self) -> str:
        """
        Return a string representation of the cache, for debugging purposes
        """
        b = ""
        for key, value in self.cache.items().__reversed__():
            b += f"\t({key}: {value})\n"
        return b


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
