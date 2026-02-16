import json

from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "tasks.json"


def load_tasks():
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
        return []

    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_tasks(task_list):
    DATA_FILE.write_text(json.dumps(task_list, indent=2), encoding="utf-8")
