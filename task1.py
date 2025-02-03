from functools import lru_cache
import random
import sys
import time


def range_sum_no_cache(array, L, R):
    if L > R:
        L, R = R, L
    return sum(array[L:R+1])

def update_no_cache(array, index, value):
    array[index] = value


class CachedArray:    
    def __init__(self, array, cache_size=1000):
        self.array = array
        self.cache_size = cache_size
        self._cache = {}
    
    def range_sum_with_cache(self, L, R):
        if L > R:
            L, R = R, L
        
        if (L, R) in self._cache:
            return self._cache[(L, R)]
        
        result = sum(self.array[L:R+1])
        if len(self._cache) >= self.cache_size:
            self._cache.pop(next(iter(self._cache))) 
        
        self._cache[(L, R)] = result
        return result
    
    def update_with_cache(self, index, value):
        self.array[index] = value
        self._cache = {key: val for key, val in self._cache.items() if not (key[0] <= index <= key[1])}


def generate_test_data(array_size=100000, query_count=50000):
    array = [random.randint(-sys.maxsize - 1, sys.maxsize) for _ in range(array_size)]
    
    queries = [
        ("Update", random.randint(0, array_size - 1), random.randint(-sys.maxsize - 1, sys.maxsize))
        if random.choice(["Update", "Range"]) == "Update"
        else ("Range", *sorted([random.randint(0, array_size - 1), random.randint(0, array_size - 1)]))
        for _ in range(query_count)
    ]
    
    return array, queries


def time_test(array, queries, use_cache=False):
    copy = array.copy()
    start_time = time.time()
    
    if use_cache:
        cached_array = CachedArray(copy)
        for query in queries:
            if query[0] == "Update":
                cached_array.update_with_cache(query[1], query[2])
            else:
                cached_array.range_sum_with_cache(query[1], query[2])
    else:
        for query in queries:
            if query[0] == "Update":
                update_no_cache(copy, query[1], query[2])
            else:
                range_sum_no_cache(copy, query[1], query[2])
    
    return time.time() - start_time


if __name__ == "__main__":
    array_size = 100000
    queries_count = 50000

    array, queries = generate_test_data(array_size, queries_count)

    print("Time taken without cache:", time_test(array, queries, False))
    print("Time taken with cache:", time_test(array, queries, True))
