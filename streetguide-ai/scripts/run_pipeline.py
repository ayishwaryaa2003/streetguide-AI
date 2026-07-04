from agents.workflow.sequential_workflow import streetguide_workflow
from agents.core.pipeline_state import default_pipeline_state
from agents.core.cache_manager import load_cache, save_cache


def run_streetguide(image_path):

    # 1. CHECK CACHE FIRST
    cached_result = load_cache(image_path)

    if cached_result:
        return {
            "success": True,
            "cached": True,
            "result": cached_result,
            "message": "Returned from cache (no API calls used)"
        }

    # 2. RUN FULL PIPELINE
    state = default_pipeline_state()

    try:
        print("[PIPELINE] Running full ADK workflow")

        result = streetguide_workflow.run({
            "image_path": image_path,
            "state": state
        })

        # 3. SAVE CACHE AFTER SUCCESS
        save_cache(image_path, result)

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Pipeline failed safely"
        }