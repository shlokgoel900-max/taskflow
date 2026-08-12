from backend.algorithms import insertion_sort_count, binary_search_count, linear_search_count

for n in (10, 500, 3000):
    records = [{"title": f"Task {i:05d}", "priority": "medium", "due_date": None} for i in range(n)]
    # Reverse titles make insertion sort perform substantial work.
    records.reverse()
    sort_records = [dict(x) for x in records]
    sort_count = insertion_sort_count(sort_records, "title")
    target = sort_records[n // 2]["title"]
    binary_count = binary_search_count(sort_records, target, "title")
    linear_count = linear_search_count(records, target, "title")
    print({
        "size": n,
        "insertion_sort_comparisons": sort_count,
        "binary_search": binary_count,
        "linear_search": linear_count,
    })
