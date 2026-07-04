import time
from google.genai import types

def safe_generate(agent_fn, fallback_value, retries=2):
    """
    Wrapper to prevent pipeline crash if Gemini fails or quota exceeds.
    """

    for attempt in range(retries):
        try:
            return agent_fn()
        except Exception as e:
            print(f"[WARN] LLM failed attempt {attempt+1}: {e}")
            time.sleep(1)

    print("[ERROR] Using fallback value")
    return fallback_value