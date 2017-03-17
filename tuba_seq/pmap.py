
try:
    import multiprocessing
except ImportError:
    print("Cannot import 'multiprocessing' module. Parallelization not possible.")
    pmap = map
    CPUs = 1
finally:
    CPUs = multiprocessing.cpu_count()
    def pmap(func, Iter, processes=CPUs):
        with multiprocessing.Pool(processes=processes) as P:
            return P.map(func, Iter)
