from settings import *
from line import Line_LRU, Line_bit_pLRU
from abc import ABC, abstractmethod


class Set(ABC):
    def __init__(self, capacity):
        self._capacity = capacity

    def request(self, tag):
        ind, hit = self.victim(tag)
        self.update_state(ind, tag)
        return hit
    
    @abstractmethod
    def victim(self, tag):
        pass
    
    @abstractmethod
    def update_state(self, ind, tag):
        pass


class Set_LRU(Set):
    def __init__(self, capacity):
        super().__init__(capacity)
        self._cache_lines = [Line_LRU() for _ in range(capacity)]
    
    def victim(self, tag):
        ind = 0
        for i in range(self._capacity):
            if self._cache_lines[i].is_valid:
                if self._cache_lines[i].tag == tag:
                    return i, 1
                if self._cache_lines[ind].age < self._cache_lines[i].age:
                    ind = i
        for i in range(self._capacity):
            if not self._cache_lines[i].is_valid:
                return i, 0
        return ind, 0
    
    def update_state(self, ind, tag):
        for i in range(CACHE_WAY):
            self._cache_lines[i].age += 1
        self._cache_lines[ind] = Line_LRU(True, 0, tag)



class Set_bit_pLRU(Set):
    def __init__(self, capacity):
        super().__init__(capacity)
        self._mru_count = 0
        self._cache_lines = [Line_bit_pLRU() for _ in range(capacity)]

    def victim(self, tag):
        ind, hit = 0, 0
        for i in range(self._capacity):
            if not self._cache_lines[i].mru:
                ind = i
        for i in range(self._capacity):
            if self._cache_lines[i].is_valid and self._cache_lines[i].tag == tag:
                ind, hit = i, 1
                break
        if not self._cache_lines[ind].mru:
            self._mru_count += 1
        return ind, hit

    def update_state(self, ind, tag):
        if self._mru_count == self._capacity:
            for i in range(self._capacity):
                self._cache_lines[i].mru = False
            self._mru_count = 1
        self._cache_lines[ind] = Line_bit_pLRU(True, True, tag)
