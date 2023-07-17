from .storage import LRUCache

def test_LRU():
    """
    Test that the LRUCache does indeed move the most recently accessed elements
    to the front of the queue, and that the least recently accessed items
    bubble to the end of the queue.
    """
    cache = LRUCache(3)
    cache.insert("a", 1)
    cache.insert("b", 2)
    cache.insert("c", 3)

    assert cache.get("b") == 2
    # assert that the cache has been updated to our expected order
    assert str(cache) == "\t(b: 2)\n\t(c: 3)\n\t(a: 1)\n"

    assert cache.insert("d", 4) == ('a', 1) # should evict 'a'
    assert str(cache) == "\t(d: 4)\n\t(b: 2)\n\t(c: 3)\n"