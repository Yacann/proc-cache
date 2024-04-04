from settings import *


class Simulation():
    _M = 64
    _N = 60
    _K = 32
    _abegin = 0x40000
    _bbegin = _abegin + _M * _K
    _cbegin = _bbegin + 2 * _K * _N

    def __init__(self, cache):
        self._cache = cache
        self._clock = 0
    
    def run(self):
        self.init()
        pa = self._abegin
        self.init()
        pc = self._cbegin

        for y in range(self._M):
            self.iter()

            for x in range(self._N):
                self.iter()
                self.init()
                pb = self._bbegin
                self.init()

                for k in range(self._K):
                    self.iter()
                    self.add()
                    self.mult()
                    self.request(pa + k, 1, 1)
                    self.request(pb + 2 * x, 2, 1)
                    self.add()
                    pb += 2 * self._N
                
                self.request(pc + 4 * x, 4, 0)

            self.add()            
            pa += self._K
            self.add()
            pc += 4 * self._N
        
        self.exit()
    
    def init(self):
        self._clock += INITIALIZATION_TIME
    
    def iter(self):
        self._clock += ITERATION_TIME
    
    def mult(self):
        self._clock += MULTIPLICATION_TIME
    
    def add(self):
        self._clock += ADDITION_TIME

    def request(self, address, bytes, rw):
        self._clock += self._cache.request(address, bytes, rw)
    
    def exit(self):
        self._clock += FUNCTION_EXIT_TIME
    
    def get_data(self):
        hits = self._cache.hits
        requests = self._cache.requests
        return 100 * hits / requests, self._clock