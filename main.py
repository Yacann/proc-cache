from settings import *
from cache import Cache_LRU, Cache_bit_pLRU
from simulation import Simulation


def main():
    for cache in [Cache_LRU(), Cache_bit_pLRU()]:
        simulation = Simulation(cache)
        simulation.run()
        hit_perc, clock = simulation.get_data()
        print(f"LRU:\thit perc. {hit_perc:3.4f}%\ttime: {clock}")


if __name__ == '__main__':
    main()