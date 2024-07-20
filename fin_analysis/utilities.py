import os
import pickle
from datetime import datetime, timedelta


app_name='FinancePro'



def get_tenant(requests):
    return requests.get_host().split('.')[0]


def get_path(requests):
    path=requests.build_absolute_uri().split('/')
    if len(path)<=4:
        return 'HOME'
    else:
        return path[-2].upper()


class CachePickle:
    def __init__(self, cache_dir='cache', expiration=60):
        self.cache_dir = cache_dir
        self.expiration = expiration
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _get_cache_path(self, key):
        return os.path.join(self.cache_dir, f"{key}.pkl")

    def set(self, key, value):
        cache_path = self._get_cache_path(key)
        with open(cache_path, 'wb') as cache_file:
            pickle.dump((datetime.now(), value), cache_file)

    def get(self, key):
        cache_path = self._get_cache_path(key)
        if not os.path.exists(cache_path):
            return None

        with open(cache_path, 'rb') as cache_file:
            timestamp, value = pickle.load(cache_file)

        if datetime.now() - timestamp > timedelta(seconds=self.expiration):
            os.remove(cache_path)
            return None

        return value

    def clear(self):
        for cache_file in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, cache_file))
