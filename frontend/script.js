const API = "http://127.0.0.1:8000";
const list = document.getElementById("taskList");
const form = document.getElementById("taskForm");
const title = document.getElementById("title");
const error = document.getElementById("error");

function cache(tasks) { localStorage.setItem("taskflow_tasks", JSON.stringify(tasks)); }

function render(tasks) {
  list.textContent = "";
  tasks.forEach(task => {
    const item = document.createElement("div");
    item.className = "task";
    const info = document.createElement("div");
    const name = document.createElement("strong");
    name.textContent = task.title;
    const meta = document.createElement("div");
    meta.textContent = `Priority: ${task.priority} | Due: ${task.due_date || "None"} | Status: ${task.status}`;
    info.appendChild(name); info.appendChild(meta);

    const controls = document.createElement("div");
    const edit = document.createElement("button");
    edit.textContent = "Edit";
    edit.addEventListener("click", async () => {
      const next = prompt("New title:", task.title);
      if (next === null) return;
      const clean = next.trim();
      if (!clean) return;
      await fetch(`${API}/tasks/${task.id}`, {
        method: "PUT", headers: {"Content-Type":"application/json"},
        body: JSON.stringify({title: clean})
      });
      load();
    });
    const del = document.createElement("button");
    del.textContent = "Delete";
    del.addEventListener("click", async () => {
      await fetch(`${API}/tasks/${task.id}`, {method: "DELETE"});
      load();
    });
    controls.appendChild(edit); controls.appendChild(del);
    item.appendChild(info); item.appendChild(controls); list.appendChild(item);
  });
}

async function load() {
  const cached = localStorage.getItem("taskflow_tasks");
  if (cached) render(JSON.parse(cached));
  const response = await fetch(`${API}/tasks`);
  const tasks = await response.json();
  cache(tasks); render(tasks);
}

form.addEventListener("submit", async event => {
  event.preventDefault();
  if (!title.value.trim()) { error.textContent = "Title cannot be empty."; return; }
  error.textContent = "";
  const response = await fetch(`${API}/tasks`, {
    method: "POST", headers: {"Content-Type":"application/json"},
    body: JSON.stringify({
      title: title.value.trim(),
      priority: document.getElementById("priority").value,
      due_date: document.getElementById("dueDate").value || null,
      project_id: Number(document.getElementById("projectId").value),
      status: "todo"
    })
  });
  if (!response.ok) { error.textContent = "Could not create task."; return; }
  form.reset(); document.getElementById("projectId").value = 1; load();
});
title.addEventListener("input", () => { if (title.value.trim()) error.textContent = ""; });

load();
