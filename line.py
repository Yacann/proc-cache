class Line_LRU():
    def __init__(self, is_valid = False, age = 0, tag = 0):
        self.is_valid = is_valid
        self.age = age
        self.tag = tag


class Line_bit_pLRU():
    def __init__(self, is_valid = False, mru = False, tag = 0):
        self.is_valid = is_valid
        self.mru = mru
        self.tag = tag
