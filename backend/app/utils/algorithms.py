def insertion_sort(records, key):
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        # key string hai ya function, dono support karo
        if callable(key):
            current_value = key(current)
        else:
            current_value = current[key]

        while j >= 0:
            if callable(key):
                previous_value = key(records[j])
            else:
                previous_value = records[j][key]

            if previous_value <= current_value:
                break

            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current

    return records


def linear_search(records, target, key):
    for i in range(len(records)):

        if callable(key):
            value = key(records[i])
        else:
            value = records[i][key]

        if value == target:
            return i

    return -1


def binary_search(records, target, key):
    left = 0
    right = len(records) - 1

    while left <= right:

        middle = (left + right) // 2

        if callable(key):
            current_value = key(records[middle])
        else:
            current_value = records[middle][key]

        if current_value == target:
            return middle

        if current_value < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1