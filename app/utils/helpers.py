import os
from datetime import datetime
from pathlib import Path
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QRect

#디렉토리가 없으면 생성
def ensure_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

#타임스탬프로 파일명 생성
def get_timestamped_filename(base_name="slice", ext=".png"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{ext}"

#스크립트 위치 기준 상대 경로 작성
def resolve_relative_path(path: str) -> str:
    return str(Path(__file__).resolve().parent / path)

# QRect 및 좌표 관련
def rect_to_dict(rect: QRect) -> dict:
    return {
        "x": rect.x(),
        "y": rect.y(),
        "width": rect.width(),
        "height": rect.height()
    }

def dict_to_rect(d: dict) -> QRect:
    return QRect(d["x"], d["y"], d["width"], d["height"])

#  이미지 처리 관련
def scale_pixmap(pixmap: QPixmap, factor: float) -> QPixmap:
    new_size = pixmap.size() * factor
    return pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
