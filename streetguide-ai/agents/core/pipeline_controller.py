import traceback

def safe_step(step_name, fn, fallback):
    """
    Runs each agent step safely.
    If it fails, returns fallback instead of crashing pipeline.
    """

    try:
        print(f"[PIPELINE] Running: {step_name}")
        result = fn()

        if result is None:
            print(f"[WARN] {step_name} returned None, using fallback")
            return fallback

        return result

    except Exception as e:
        print(f"[ERROR] {step_name} failed: {e}")
        traceback.print_exc()
        return fallback