def insertion_sort(records, key):
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0 and records[j][key] > current[key]:
            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current

    return records


def linear_search(records, target, key):
    for i in range(len(records)):
        if records[i][key] == target:
            return i

    return -1


def binary_search(records, target, key):
    left = 0
    right = len(records) - 1

    while left <= right:
        middle = (left + right) // 2
        current_value = records[middle][key]

        if current_value == target:
            return middle

        if current_value < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1