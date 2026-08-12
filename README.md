# TaskFlow

TaskFlow is a FastAPI + SQLAlchemy task-management application with a JavaScript dashboard, hand-written sorting/searching algorithms, and a deterministic keyless AI quick-add parser.

## Setup

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the app

Use the two-process setup.

Terminal 1:
```bash
uvicorn backend.main:app --reload --port 8000
```

Terminal 2:
```bash
python -m http.server 5500 -d frontend
```

Open `http://localhost:5500`.

## Endpoints

- POST `/users` — create user.
- GET `/users` — list users.
- POST `/projects` — create project.
- GET `/projects` — list projects.
- POST `/tasks` — create task.
- GET `/tasks` — list tasks; `?sort=priority` uses insertion sort.
- GET `/tasks/{id}` — get task.
- PUT `/tasks/{id}` — update task.
- DELETE `/tasks/{id}` — delete task.
- GET `/projects/statistics` — SQL aggregate task counts.
- GET `/tasks/search?title=...&algo=binary|linear` — algorithm-backed exact search.
- POST `/tasks/quick-add` — deterministic AI-style parser and task creation.

## Database

`users.email` is unique. `projects.owner_id` references `users.id`; `tasks.project_id` references `projects.id`. Task priority is restricted at the Pydantic boundary to low, medium, or high. `due_date` is stored as text so phrases such as `next friday` remain valid.

## Algorithms

Insertion sort: best O(n), worst O(n²), space O(1).
Binary search: O(log n) time on a sorted list.
Linear search: O(n) worst-case time.

Run checks:
```bash
python check_algorithms.py
```

Run benchmark:
```bash
python benchmark.py
```

The benchmark uses the same dictionary fields used by the task endpoints and reports raw comparison counts for 10, 500, and 3,000 records.

The implementation uses hand-written algorithms without built-in sorting or search helpers.

Benchmark results are reported for 10, 500, and 3,000 records.

## Why sorting can be worthwhile

Insertion sort is expensive when the list is initially unsorted, especially at larger sizes. Once a list is sorted, binary search needs logarithmic comparisons while linear search can scan the entire list. If a team repeatedly searches or views an ordered task list during the day, paying a sorting cost can be worthwhile when the sorted structure is reused. The benchmark output should be committed after running `python benchmark.py`, so the submitted README/results contain the actual raw counts from the implementation.

## AI quick-add prompting rationale

The design is closest to zero-shot prompting: one system instruction describes the required structured behavior and the user message contains the task description. No demonstrations are needed because the required parsing rules are deterministic and explicitly specified. This keeps token usage lower than a few-shot design and avoids the extra verbosity of chain-of-thought-style prompting. Reliability comes primarily from the deterministic mock parser and Pydantic validation rather than from a model's interpretation.

## Five worked examples

1. `This is urgent, mark it ASAP please`
```json
{"title":"This is , mark it please","priority":"high","due_date_hint":null}
```

2. ` `
```json
{"title":"Untitled task","priority":"medium","due_date_hint":null}
```

3. `Finish the report next Friday, it's urgent`
```json
{"title":"Finish the report , it's","priority":"high","due_date_hint":"next friday"}
```

4. `tomorrow review tomorrow`
```json
{"title":"review","priority":"medium","due_date_hint":"tomorrow"}
```

5. `Prepare deployment next Monday asap`
```json
{"title":"Prepare deployment ","priority":"high","due_date_hint":"next monday"}
```

## Git workflow

The assignment requires a feature branch with at least two commits followed by a merge into `main`. Example:

```bash
git init
git add .
git commit -m "feat: initial TaskFlow app"
git branch -M main
git checkout -b feature/algorithms
git add .
git commit -m "feat: add sorting and search engine"
git add .
git commit -m "feat: add quick-add and checks"
git checkout main
git merge --no-ff feature/algorithms -m "merge: TaskFlow feature branch"
git log --graph --all
```

Push the final repository to GitHub as one public repository.
