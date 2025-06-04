from PySide6.QtCore import QRect
from PySide6.QtGui import QPixmap
from typing import List
import os

def slice_image(pixmap: QPixmap, regions: List[QRect], save_dir: str, prefix: str = "slice") -> List[str]:
    """
    지정된 사각형 영역들로부터 이미지를 잘라내고 저장함.

    Args:
        pixmap: 원본 이미지 QPixmap
        regions: 잘라낼 QRect 리스트 (이미지 내 위치)
        save_dir: 저장할 디렉토리 경로
        prefix: 저장 파일 접두사

    Returns:
        저장된 파일 경로 리스트
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    saved_files = []
    for i, rect in enumerate(regions, start=1):
        cropped = pixmap.copy(rect)
        file_path = os.path.join(save_dir, f"{prefix}_{i:03d}.png")
        cropped.save(file_path)
        saved_files.append(file_path)
    print(f"Saved: {file_path}")
    return saved_files
