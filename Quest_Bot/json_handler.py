import json


def load_json(file_path: str) -> dict:
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}