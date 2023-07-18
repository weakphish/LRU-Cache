from storage import LRUCache

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
    assert str(cache) == "(b: 2) (c: 3) (a: 1) "

    assert cache.insert("d", 4) == ('a', 1) # should evict 'a'
    assert str(cache) == "(d: 4) (b: 2) (c: 3) "
