import json
from pathlib import Path

def save_project(file_path, image_path, regions):
    data = {
        "image_path": image_path,
        "regions": [r.getRect() for r in regions],  # QRect -> dict 변환 필요
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_project(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["image_path"], data["regions"]
