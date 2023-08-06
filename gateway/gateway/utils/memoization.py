from functools import lru_cache
from cachetools import TTLCache

def ttl_cache(maxSize=128, ttl=300):
    return TTLCache(maxsize=maxSize, ttl=ttl)

def memoize_with_ttl(expiration=10):
    cache = ttl_cache(ttl=expiration)
    
    def decorator(fn):
        @lru_cache(maxsize=None)
        def wrapper(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in cache:
                return cache[cache_key]
            result = fn(*args, **kwargs)
            cache[cache_key] = result
            return result
        
        return wrapper
    
    return decorator