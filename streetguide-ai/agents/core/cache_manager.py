import os
import json
import hashlib

CACHE_DIR = "agents/cache"

os.makedirs(CACHE_DIR, exist_ok=True)


def get_image_hash(image_path: str):
    """
    Create unique ID for each image
    """
    with open(image_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def get_cache_path(image_hash: str):
    return os.path.join(CACHE_DIR, f"{image_hash}.json")


def load_cache(image_path: str):
    image_hash = get_image_hash(image_path)
    path = get_cache_path(image_hash)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            print("[CACHE] HIT")
            return json.load(f)

    print("[CACHE] MISS")
    return None


def save_cache(image_path: str, data: dict):
    image_hash = get_image_hash(image_path)
    path = get_cache_path(image_hash)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("[CACHE] SAVED")