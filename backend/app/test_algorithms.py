from utils.algorithms import insertion_sort, linear_search, binary_search
from benchmark import benchmark_sort


records = [
    {"title": "Task C", "priority": 3},
    {"title": "Task A", "priority": 1},
    {"title": "Task B", "priority": 2},
]


# Test Insertion Sort
sorted_records = insertion_sort(records.copy(), "priority")
print("Sorted:", sorted_records)


# Test Linear Search
linear_result = linear_search(
    sorted_records,
    2,
    "priority"
)

print("Linear Search Result:", linear_result)


# Test Binary Search
binary_result = binary_search(
    sorted_records,
    2,
    "priority"
)

print("Binary Search Result:", binary_result)


# Test Benchmark
time_taken = benchmark_sort(
    insertion_sort,
    records,
    "priority"
)

print("Insertion Sort Time:", time_taken)