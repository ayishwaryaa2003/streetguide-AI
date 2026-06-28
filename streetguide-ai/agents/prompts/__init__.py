from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load_prompt(filename: str) -> str:
    """
    Load a prompt from the prompts directory.

    Args:
        filename: Name of the markdown file.

    Returns:
        Prompt content as a string.
    """
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")