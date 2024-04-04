from settings import *
from set import Set_LRU, Set_bit_pLRU
from abc import ABC, abstractmethod


class Cache(ABC):
    @abstractmethod
    def __init__(self):
        self.hits = 0
        self.requests = 0
    
    def request(self, address, bytes, rw):
        self.requests += 1

        tag, ind = self.parse_address(address)
        hit = self._sets[ind].request(tag)

        data_trans_time = (bytes + DATA_BUS_LEN - 1) // DATA_BUS_LEN
        if rw == 1:
            if hit == 1:
                dclock = data_trans_time * 2 + CACHE_HIT_TIME
            else:
                dclock = data_trans_time * 2 + CACHE_MISS_TIME + 1 + MEMORY_TIME + (CACHE_LINE_SIZE + DATA_BUS_LEN - 1) // DATA_BUS_LEN
        else:
            if hit == 1:
                dclock = data_trans_time + CACHE_HIT_TIME + 1
            else:
                dclock = data_trans_time + CACHE_MISS_TIME + 1
        
        self.hits += hit
        return dclock

    def parse_address(self, address):
        tag = address >> ADDR_LEN - CACHE_TAG_LEN
        ind = (address >> CACHE_OFFSET_LEN) % (1 << CACHE_IND_LEN)
        return tag, ind
    

class Cache_LRU(Cache):
    def __init__(self):
        super().__init__()
        self._sets = [Set_LRU(CACHE_WAY) for _ in range(CACHE_SET_COUNT)]


class Cache_bit_pLRU(Cache):
    def __init__(self):
        super().__init__()
        self._sets = [Set_bit_pLRU(CACHE_WAY) for _ in range(CACHE_SET_COUNT)]