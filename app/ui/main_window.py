# main_window.py

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent

from .image_editor import ImageEditorDialog

class DragLabel(QLabel):
    def __init__(self, open_editor_callback, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setText("Drag Image Here\n(드래그하면 편집 창이 열립니다)")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                font-size: 16px;
                min-height: 300px;
            }
        """)
        self.open_editor_callback = open_editor_callback

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            image_path = urls[0].toLocalFile()
            self.open_editor_callback(image_path)
        event.acceptProposedAction()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webtoon Slicer")
        self.setMinimumSize(400, 500)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.drag_label = DragLabel(self.open_editor)

        button_layout = QHBoxLayout()
        self.open_button = QPushButton("Open Image")
        self.close_button = QPushButton("Close Editor")

        self.open_button.clicked.connect(self.open_image)
        self.close_button.clicked.connect(self.close_editor)

        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.close_button)

        main_layout.addWidget(self.drag_label)
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if path:
            self.open_editor(path)

    def open_editor(self, image_path: str):
        editor = ImageEditorDialog(image_path, self)
        editor.exec()

    def close_editor(self):
        QMessageBox.information(self, "Close Editor", "편집기를 닫습니다.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
