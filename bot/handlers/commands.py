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
        "/scores <lab> - show scores for a lab"
    )

async def handle_health() -> str:
    return "Health check - not implemented yet"

async def handle_labs() -> str:
    return "Labs list - not implemented yet"

async def handle_scores(lab: str) -> str:
    return f"Scores for {lab} - not implemented yet"

async def handle_unknown(text: str) -> str:
    return f"Unknown command: {text}\nUse /help to see available commands."
