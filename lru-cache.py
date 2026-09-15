from collections import OrderedDict

class LRUCache:

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        cached_value = self.cache.get(key, -1)
        if cached_value == -1:
            return -1

        self.cache.move_to_end(key)

        return cached_value

    def put(self, key: int, value: int) -> None:
        if self.cache.get(key, -1) != -1:
            self.cache.move_to_end(key)

        elif len(self.cache) == self.capacity:
            self.cache.popitem(last=False)

        self.cache[key] = value
