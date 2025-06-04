# image_editor.py
from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QScrollArea, QHBoxLayout, QPushButton, QFileDialog, QMessageBox,QSizePolicy

)
from PySide6.QtCore import Qt,QRect
from PySide6.QtGui import QPixmap, QWheelEvent, QKeyEvent
from .region_selector import RegionSelector
from app.core.slicer import slice_image

class ImageEditorDialog(QDialog):
    def __init__(self, image_path: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Image Editor")
        self.setMinimumSize(600, 800)

        self.scale_factor = 1.0
        self.original_pixmap = QPixmap(image_path)
        self.selector = RegionSelector(on_save_callback=self.save_cropped_regions)

        if self.original_pixmap.isNull():
            self.reject()
            return

        self.image_label = RegionSelector(on_save_callback=self.save_cropped_regions)
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.image_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.image_label.setPixmap(self.original_pixmap)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_label)

        zoom_in_btn = QPushButton("Zoom In (+)")
        zoom_out_btn = QPushButton("Zoom Out (-)")
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_out_btn.clicked.connect(self.zoom_out)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(zoom_in_btn)
        btn_layout.addWidget(zoom_out_btn)
        btn_layout.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        layout.addLayout(btn_layout)

        self.image_label.scale_factor = self.scale_factor
        self.setLayout(layout)
        self.image_label.setFocus()

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def scale_image(self, factor):
        self.scale_factor *= factor
        new_size = self.original_pixmap.size() * self.scale_factor
        scaled_pixmap = self.original_pixmap.scaled(
            new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        self.image_label.scale_factor = self.scale_factor
        self.image_label.update() 


    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.modifiers() & Qt.ControlModifier:
            if event.key() in [Qt.Key_Plus, Qt.Key_Equal]:
                self.zoom_in()
                event.accept()
                return
            elif event.key() == Qt.Key_Minus:
                self.zoom_out()
                event.accept()
                return
        super().keyPressEvent(event)
            
    def save_cropped_regions(self, _unused_pixmap, regions):
        print(f"save_cropped_regions called with {len(regions)} regions")
        if not regions:
            QMessageBox.warning(self, "경고", "선택된 영역이 없습니다.")
            return

        if self.original_pixmap.isNull():
            print("❌ Received null original_pixmap!")
            QMessageBox.critical(self, "오류", "잘못된 이미지입니다.")
            return

        save_dir = QFileDialog.getExistingDirectory(self, "저장 폴더 선택")
        print(f"Selected directory: {save_dir}")
        if not save_dir:
            return

        saved_files = slice_image(self.original_pixmap, regions, save_dir)
        print(f"Saved files: {saved_files}")

        if saved_files:
            QMessageBox.information(self, "완료", f"{len(saved_files)}개의 이미지가 저장되었습니다.")
        else:
            QMessageBox.critical(self, "오류", "이미지 저장에 실패했습니다.")
