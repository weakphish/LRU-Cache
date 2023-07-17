"""
Implement a data storage class that is backed by an in-memory LRU cache.
"""

import json
from typing import Any
from collections import OrderedDict


class LRUCache:
    """
    An in-memory LRU cache.

    The cache uses an OrderedDict to keep track of the order of items - the
    standard 'dict' type does not guarantee that order is preserved, and the
    OrderedDict type provides methods for moving items to the front/back.
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


class Storage:
    """JSON File storage class that is backed by an LRU Cache."""

    def __init__(self, filename: str, cache_size: int):
        self.filename = filename
        self.cache = LRUCache(cache_size)

    def insert(self, key: Any, value: Any):
        """
        Insert a key/value pairing into storage.

        :param key: The key to insert.
        :param value: The value to insert.
        """
        self.cache.insert(key, value)
        with open(self.filename, "r+") as f:
            content = f.read()
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                data = {}
            data[key] = value
            f.seek(0)
            json.dump(data, f)

    def get(self, key: Any) -> Any:
        """
        Get a value from storage using it's key.

        :param key: The key to look up with.
        :return: The value of the key, or None if the key does not exist.
        """
        if self.cache.get(key):
            return self.cache.get(key)

        with open(self.filename, "r") as f:
            for line in f:
                data = json.loads(line)
                if key in data:
                    return data[key]

        return None

    def __str__(self) -> str:
        """
        Return the string representation of the storage & cache.
        """
        with open(self.filename, "r") as f:
            return f"Storage: {json.loads(f.read())}\nCache: {self.cache}"


def main():
    storage = Storage("storage.json", 3)
    storage.insert("a", 1)
    storage.insert("b", 2)
    storage.insert("c", 3)
    print("Cache after initial insertion:")
    print(storage)

    storage.get("b")
    print("Cache after get(b):")
    print(storage)

    storage.insert("d", 4)
    print("Cache after insert(d):")
    print(storage)

    storage.get("c")
    print("Cache after get(c):")
    print(storage)


if __name__ == "__main__":
    main()
