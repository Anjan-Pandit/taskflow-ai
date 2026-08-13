import time


def benchmark_sort(sort_function, records, key):
    data = [record.copy() for record in records]

    start_time = time.perf_counter()

    sort_function(data, key)

    end_time = time.perf_counter()

    return end_time - start_time