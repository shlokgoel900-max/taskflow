import re

SYSTEM_PROMPT = (
    "Parse a task description into title, priority, and due_date_hint. "
    "Priority must be low, medium, or high. Preserve original title casing."
)

PRIORITY_WORDS = ["urgent", "asap", "whenever", "low priority"]
DATE_PHRASES = [
    "today", "tomorrow", "next week",
    "next monday", "next tuesday", "next wednesday", "next thursday",
    "next friday", "next saturday", "next sunday",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
]

def mock_parse(description: str):
    lower = description.lower()

    if "urgent" in lower or "asap" in lower:
        priority = "high"
    elif "whenever" in lower or "low priority" in lower:
        priority = "low"
    else:
        priority = "medium"

    due = None
    for phrase in DATE_PHRASES:
        if phrase in lower:
            due = phrase
            break

    title = description
    # Remove every priority keyword, case-insensitively, from the original-cased text.
    for word in PRIORITY_WORDS:
        title = re.sub(re.escape(word), "", title, flags=re.IGNORECASE)
    # Remove every occurrence of the selected date phrase.
    if due:
        title = re.sub(re.escape(due), "", title, flags=re.IGNORECASE)

    title = title.strip()
    if not title:
        title = "Untitled task"

    return {
        "title": title,
        "priority": priority,
        "due_date_hint": due,
        "system_prompt": SYSTEM_PROMPT,
        "user_message": description,
    }
