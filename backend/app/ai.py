import re
from datetime import date, timedelta


def analyze_task(title: str, description: str = ""):
    """
    Analyze a natural-language task and return structured task data.
    This is a lightweight rule-based AI-style parser that works
    without requiring an external AI API.
    """

    text = f"{title} {description}".strip()
    lower_text = text.lower()

    # ------------------------------------------
    # PRIORITY DETECTION
    # ------------------------------------------

    if any(word in lower_text for word in [
        "urgent",
        "critical",
        "asap",
        "very important",
        "high priority",
        "high-priority"
    ]):
        priority = "high"

    elif any(word in lower_text for word in [
        "low priority",
        "low-priority",
        "not urgent"
    ]):
        priority = "low"

    else:
        priority = "medium"

    # ------------------------------------------
    # DUE DATE DETECTION
    # ------------------------------------------

    due_date = None
    today = date.today()

    if "today" in lower_text:
        due_date = today.isoformat()

    elif "tomorrow" in lower_text:
        due_date = (today + timedelta(days=1)).isoformat()

    elif "day after tomorrow" in lower_text:
        due_date = (today + timedelta(days=2)).isoformat()

    # ------------------------------------------
    # DAYS FROM NOW
    # Example: "in 3 days"
    # ------------------------------------------

    match = re.search(
        r"in\s+(\d+)\s+days?",
        lower_text
    )

    if match:
        days = int(match.group(1))
        due_date = (today + timedelta(days=days)).isoformat()

    # ------------------------------------------
    # CATEGORY DETECTION
    # ------------------------------------------

    if any(word in lower_text for word in [
        "python",
        "javascript",
        "coding",
        "code",
        "programming",
        "development",
        "api",
        "fastapi",
        "frontend",
        "backend"
    ]):
        category = "Development"

    elif any(word in lower_text for word in [
        "exam",
        "study",
        "assignment",
        "homework",
        "learn",
        "practice"
    ]):
        category = "Education"

    elif any(word in lower_text for word in [
        "meeting",
        "call",
        "team",
        "client"
    ]):
        category = "Work"

    else:
        category = "General"

    # ------------------------------------------
    # CLEAN TITLE
    # ------------------------------------------

    clean_title = title.strip()

    # Remove common priority/date phrases from title
    clean_title = re.sub(
        r"\b(high priority|high-priority|low priority|low-priority)\b",
        "",
        clean_title,
        flags=re.IGNORECASE
    )

    clean_title = re.sub(
        r"\b(today|tomorrow|day after tomorrow)\b",
        "",
        clean_title,
        flags=re.IGNORECASE
    )

    clean_title = re.sub(
        r"\bin\s+\d+\s+days?\b",
        "",
        clean_title,
        flags=re.IGNORECASE
    )

    clean_title = re.sub(
        r"\s+",
        " ",
        clean_title
    ).strip()

    if not clean_title:
        clean_title = title.strip()

    return {
        "title": clean_title,
        "description": description.strip(),
        "priority": priority,
        "category": category,
        "due_date": due_date
    }