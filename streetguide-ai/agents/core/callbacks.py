# agents/core/callbacks.py
import json
from typing import Any, Dict, Optional
from google.adk.tools import BaseTool, ToolContext


def _normalize_finish_task_args(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    finish_task's args shape varies across turns: sometimes structured
    fields directly, sometimes everything wrapped in a single 'result'
    key holding a JSON string. Normalize both into a plain dict.
    """
    if isinstance(args, dict) and set(args.keys()) == {"result"} and isinstance(args["result"], str):
        try:
            return json.loads(args["result"])
        except (TypeError, ValueError):
            return args
    return args


def capture_finish_task_output(output_key: str):
    def after_tool_callback(tool, args, tool_context, tool_response):
        if tool.name == "finish_task":
            tool_context.state[output_key] = _normalize_finish_task_args(args)
        return None
    return after_tool_callback