from PySide6.QtCore import QRect
from PySide6.QtGui import QPixmap
from typing import List
import os

def slice_image(pixmap: QPixmap, regions: List[QRect], save_dir: str, prefix: str = "slice") -> List[str]:
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
