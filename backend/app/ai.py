import re
from datetime import date, timedelta


def analyze_task(title: str, description: str = ""):
    """
    Analyze a natural-language task and return structured task data.

    Detects:
    - Clean task title
    - Description
    - Priority
    - Category
    - Project ID
    - Due date
    """

    original_title = title.strip()
    original_description = description.strip()

    text = f"{original_title} {original_description}".strip()
    lower_text = text.lower()

    # ==========================================
    # PRIORITY DETECTION
    # ==========================================

    if any(
        phrase in lower_text
        for phrase in [
            "very high priority",
            "high priority",
            "high-priority",
            "urgent",
            "critical",
            "asap",
            "important",
        ]
    ):
        priority = "high"

    elif any(
        phrase in lower_text
        for phrase in [
            "low priority",
            "low-priority",
            "not urgent",
        ]
    ):
        priority = "low"

    else:
        priority = "medium"

    # ==========================================
    # DUE DATE DETECTION
    # ==========================================

    due_date = None
    today = date.today()

    if "day after tomorrow" in lower_text:

        due_date = (
            today + timedelta(days=2)
        ).isoformat()

    elif "tomorrow" in lower_text:

        due_date = (
            today + timedelta(days=1)
        ).isoformat()

    elif "today" in lower_text:

        due_date = today.isoformat()

    # Example:
    # Complete project in 3 days

    match = re.search(
        r"\bin\s+(\d+)\s+days?\b",
        lower_text
    )

    if match:

        days = int(match.group(1))

        due_date = (
            today + timedelta(days=days)
        ).isoformat()

    # ==========================================
    # CATEGORY DETECTION
    # ==========================================

    if any(
        word in lower_text
        for word in [
            "python",
            "javascript",
            "coding",
            "code",
            "programming",
            "development",
            "api",
            "fastapi",
            "frontend",
            "backend",
            "software",
            "github",
        ]
    ):

        category = "Development"

    elif any(
        word in lower_text
        for word in [
            "exam",
            "study",
            "assignment",
            "homework",
            "learn",
            "practice",
            "class",
            "college",
            "school",
        ]
    ):

        category = "Education"

    elif any(
        word in lower_text
        for word in [
            "meeting",
            "call",
            "team",
            "client",
            "office",
            "work",
        ]
    ):

        category = "Work"

    else:

        category = "General"

    # ==========================================
    # PROJECT ID
    # ==========================================

    # Default production project
    # Currently using Project ID 1.

    project_id = 1

    # ==========================================
    # CLEAN TITLE
    # ==========================================

    clean_title = original_title

    # Remove priority phrases

    priority_patterns = [
        r"\bvery\s+high\s+priority\b",
        r"\bhigh\s+priority\b",
        r"\bhigh-priority\b",
        r"\blow\s+priority\b",
        r"\blow-priority\b",
        r"\bnot\s+urgent\b",
    ]

    for pattern in priority_patterns:

        clean_title = re.sub(
            pattern,
            "",
            clean_title,
            flags=re.IGNORECASE,
        )

    # Remove urgency words

    clean_title = re.sub(
        r"\b(urgent|critical|asap)\b",
        "",
        clean_title,
        flags=re.IGNORECASE,
    )

    # Remove date phrases

    clean_title = re.sub(
        r"\bday\s+after\s+tomorrow\b",
        "",
        clean_title,
        flags=re.IGNORECASE,
    )

    clean_title = re.sub(
        r"\btomorrow\b",
        "",
        clean_title,
        flags=re.IGNORECASE,
    )

    clean_title = re.sub(
        r"\btoday\b",
        "",
        clean_title,
        flags=re.IGNORECASE,
    )

    clean_title = re.sub(
        r"\bin\s+\d+\s+days?\b",
        "",
        clean_title,
        flags=re.IGNORECASE,
    )

    # ==========================================
    # CLEAN EXTRA WORDS
    # ==========================================

    clean_title = re.sub(
        r"\s+",
        " ",
        clean_title,
    ).strip()

    clean_title = re.sub(
        r"\bwith\s*$",
        "",
        clean_title,
        flags=re.IGNORECASE,
    ).strip()

    clean_title = re.sub(
        r"\bby\s*$",
        "",
        clean_title,
        flags=re.IGNORECASE,
    ).strip()

    clean_title = re.sub(
        r"[,\-:;]+$",
        "",
        clean_title,
    ).strip()

    # ==========================================
    # FALLBACK TITLE
    # ==========================================

    if not clean_title:

        clean_title = original_title

    # ==========================================
    # DESCRIPTION GENERATION
    # ==========================================

    if original_description:

        generated_description = (
            original_description
        )

    else:

        generated_description = ""

        lower_clean_title = (
            clean_title.lower()
        )

        if "assignment" in lower_clean_title:

            generated_description = (
                f"Complete the {clean_title} "
                "and submit it by the deadline."
            )

        elif "exam" in lower_clean_title:

            generated_description = (
                f"Prepare for the {clean_title} "
                "and complete the required revision."
            )

        elif any(
            word in lower_clean_title
            for word in [
                "python",
                "javascript",
                "coding",
                "programming",
                "code",
            ]
        ):

            generated_description = (
                "Complete the programming task: "
                f"{clean_title}."
            )

        elif "project" in lower_clean_title:

            generated_description = (
                "Work on the project: "
                f"{clean_title}."
            )

        elif "meeting" in lower_clean_title:

            generated_description = (
                "Attend and complete the meeting: "
                f"{clean_title}."
            )

        else:

            generated_description = (
                "Complete the task: "
                f"{clean_title}."
            )

    # ==========================================
    # RETURN STRUCTURED RESULT
    # ==========================================

    return {
        "title": clean_title,
        "description": generated_description,
        "priority": priority,
        "category": category,
        "project_id": project_id,
        "due_date": due_date,
    }