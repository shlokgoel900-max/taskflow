from backend.algorithms import (
    insertion_sort, binary_search, insertion_sort_count,
    binary_search_count, linear_search_count
)

def check(case_name, result, expected):
    if result == expected:
        print(f"PASS: {case_name}")
    else:
        print(f"FAIL: {case_name} — expected {expected}, got {result}")

records = []
insertion_sort(records, "x")
check("empty insertion sort", records, [])

records = [{"x": 7}]
insertion_sort(records, "x")
check("single insertion sort", records, [{"x": 7}])

records = [{"x": 1}, {"x": 3}, {"x": 5}, {"x": 7}, {"x": 9}]
check("binary first", binary_search(records, 1, "x"), 0)
check("binary middle", binary_search(records, 5, "x"), 2)
check("binary last", binary_search(records, 9, "x"), 4)
check("binary absent", binary_search(records, 8, "x"), -1)

records = [{"x": 3}, {"x": 1}, {"x": 2}]
count = insertion_sort_count(records, "x")
check("sort count sorted output", records, [{"x":1},{"x":2},{"x":3}])
check("sort count is int", type(count) == int and count > 0, True)

result = binary_search_count([{"x":1},{"x":2},{"x":3},{"x":4},{"x":5}], 3, "x")
check("binary count shape", result["index"] == 2 and type(result["comparison_count"]) == int and result["comparison_count"] > 0, True)

result = linear_search_count([{"x":1},{"x":2},{"x":3}], 9, "x")
check("linear absent count", result["index"] == -1 and result["comparison_count"] == 3, True)
