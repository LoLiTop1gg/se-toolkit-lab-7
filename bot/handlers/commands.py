import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.lms_client import get_items, get_pass_rates

async def handle_start() -> str:
    return (
        "Welcome to LMS Bot!\n\n"
        "I can help you interact with the Learning Management System.\n"
        "Use /help to see available commands."
    )

async def handle_help() -> str:
    return (
        "Available commands:\n\n"
        "/start - welcome message\n"
        "/help - show this help\n"
        "/health - check backend status\n"
        "/labs - list available labs\n"
        "/scores <lab> - show scores for a lab (e.g. /scores lab-04)"
    )

async def handle_health() -> str:
    try:
        items = await get_items()
        return f"Backend is healthy. {len(items)} items available."
    except Exception as e:
        return f"Backend error: {e}"

async def handle_labs() -> str:
    try:
        items = await get_items()
        labs = [i for i in items if i.get("type") == "lab"]
        if not labs:
            return "No labs found."
        lines = ["Available labs:\n"]
        for lab in labs:
            lines.append(f"- {lab.get('title', lab.get('lab', ''))}")
        return "\n".join(lines)
    except Exception as e:
        return f"Backend error: {e}"

async def handle_scores(lab: str) -> str:
    if not lab:
        return "Please specify a lab. Example: /scores lab-04"
    try:
        data = await get_pass_rates(lab)
        if not data:
            return f"No scores found for {lab}."
        lines = [f"Pass rates for {lab}:\n"]
        for item in data:
            task = item.get("task", "unknown")
            rate = item.get("pass_rate", 0)
            attempts = item.get("total_attempts", 0)
            lines.append(f"- {task}: {rate:.1%} ({attempts} attempts)")
        return "\n".join(lines)
    except Exception as e:
        return f"Backend error: {e}"

async def handle_unknown(text: str) -> str:
    return f"Unknown command: {text}\nUse /help to see available commands."
