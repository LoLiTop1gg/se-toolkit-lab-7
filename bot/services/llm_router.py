import json
import sys
import httpx
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LLM_API_KEY, LLM_API_BASE_URL, LLM_API_MODEL
from services.lms_client import (
    get_items, get_pass_rates, get_learners,
    get_scores, get_timeline, get_groups,
    get_top_learners, get_completion_rate, trigger_sync
)

TOOLS = [
    {"type":"function","function":{"name":"get_items","description":"List all labs and tasks","parameters":{"type":"object","properties":{}}}},
    {"type":"function","function":{"name":"get_learners","description":"Get enrolled students and groups","parameters":{"type":"object","properties":{}}}},
    {"type":"function","function":{"name":"get_scores","description":"Get score distribution for a lab","parameters":{"type":"object","properties":{"lab":{"type":"string","description":"Lab identifier e.g. lab-01"}},"required":["lab"]}}},
    {"type":"function","function":{"name":"get_pass_rates","description":"Get per-task average scores and attempt counts for a lab","parameters":{"type":"object","properties":{"lab":{"type":"string","description":"Lab identifier e.g. lab-01"}},"required":["lab"]}}},
    {"type":"function","function":{"name":"get_timeline","description":"Get submissions per day for a lab","parameters":{"type":"object","properties":{"lab":{"type":"string","description":"Lab identifier e.g. lab-01"}},"required":["lab"]}}},
    {"type":"function","function":{"name":"get_groups","description":"Get per-group scores and student counts for a lab","parameters":{"type":"object","properties":{"lab":{"type":"string","description":"Lab identifier e.g. lab-01"}},"required":["lab"]}}},
    {"type":"function","function":{"name":"get_top_learners","description":"Get top N learners by score for a lab","parameters":{"type":"object","properties":{"lab":{"type":"string","description":"Lab identifier e.g. lab-01"},"limit":{"type":"integer","description":"Number of top learners to return"}},"required":["lab"]}}},
    {"type":"function","function":{"name":"get_completion_rate","description":"Get completion rate percentage for a lab","parameters":{"type":"object","properties":{"lab":{"type":"string","description":"Lab identifier e.g. lab-01"}},"required":["lab"]}}},
    {"type":"function","function":{"name":"trigger_sync","description":"Refresh data from autochecker","parameters":{"type":"object","properties":{}}}},
]

TOOL_FUNCTIONS = {
    "get_items": lambda args: get_items(),
    "get_learners": lambda args: get_learners(),
    "get_scores": lambda args: get_scores(args["lab"]),
    "get_pass_rates": lambda args: get_pass_rates(args["lab"]),
    "get_timeline": lambda args: get_timeline(args["lab"]),
    "get_groups": lambda args: get_groups(args["lab"]),
    "get_top_learners": lambda args: get_top_learners(args["lab"], args.get("limit", 5)),
    "get_completion_rate": lambda args: get_completion_rate(args["lab"]),
    "trigger_sync": lambda args: trigger_sync(),
}

async def route(user_message: str) -> str:
    messages = [
        {"role": "system", "content": "You are an LMS assistant. Use the available tools to answer questions about labs, scores, and students. Always use tools to fetch real data before answering."},
        {"role": "user", "content": user_message}
    ]

    async with httpx.AsyncClient(timeout=60) as client:
        for _ in range(5):
            resp = await client.post(
                f"{LLM_API_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {LLM_API_KEY}"},
                json={"model": LLM_API_MODEL, "messages": messages, "tools": TOOLS, "tool_choice": "auto"}
            )
            resp.raise_for_status()
            data = resp.json()
            msg = data["choices"][0]["message"]

            if msg.get("tool_calls"):
                messages.append(msg)
                for tool_call in msg["tool_calls"]:
                    name = tool_call["function"]["name"]
                    args = json.loads(tool_call["function"]["arguments"] or "{}")
                    print(f"[tool] LLM called: {name}({args})", file=sys.stderr)
                    try:
                        result = await TOOL_FUNCTIONS[name](args)
                        result_str = json.dumps(result)
                        print(f"[tool] Result: {result_str[:100]}", file=sys.stderr)
                    except Exception as e:
                        result_str = f"Error: {e}"
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": result_str
                    })
                print(f"[summary] Feeding {len(msg['tool_calls'])} tool results back to LLM", file=sys.stderr)
            else:
                return msg.get("content", "No response from LLM.")

    return "Sorry, I could not complete the request."
