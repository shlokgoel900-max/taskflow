def insertion_sort(records, key):
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1
        while j >= 0 and records[j][key] > current[key]:
            records[j + 1] = records[j]
            j -= 1
        records[j + 1] = current

def binary_search(sorted_records, target_value, key):
    low, high = 0, len(sorted_records) - 1
    while low <= high:
        mid = (low + high) // 2
        value = sorted_records[mid][key]
        if value == target_value:
            return mid
        if value < target_value:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def linear_search(records, target_value, key):
    for i, record in enumerate(records):
        if record[key] == target_value:
            return i
    return -1

def insertion_sort_count(records, key):
    count = 0
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1
        while j >= 0:
            count += 1
            if records[j][key] > current[key]:
                records[j + 1] = records[j]
                j -= 1
            else:
                break
        records[j + 1] = current
    return count

def binary_search_count(sorted_records, target_value, key):
    low, high = 0, len(sorted_records) - 1
    count = 0
    while low <= high:
        mid = (low + high) // 2
        count += 1
        value = sorted_records[mid][key]
        if value == target_value:
            return {"index": mid, "comparison_count": count}
        if value < target_value:
            low = mid + 1
        else:
            high = mid - 1
    return {"index": -1, "comparison_count": count}

def linear_search_count(records, target_value, key):
    count = 0
    for i, record in enumerate(records):
        count += 1
        if record[key] == target_value:
            return {"index": i, "comparison_count": count}
    return {"index": -1, "comparison_count": count}
