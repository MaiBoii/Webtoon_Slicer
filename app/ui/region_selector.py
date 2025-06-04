#region_selector.py

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QRect, QPoint, QTimer
from PySide6.QtGui import QPainter, QPen, QMouseEvent, QPaintEvent, QKeyEvent

class RegionSelector(QLabel):
    def __init__(self, on_save_callback=None, parent=None):
        super().__init__(parent)

        self.scale_factor = 1.0 
        self.setFocusPolicy(Qt.StrongFocus) 
        self.on_save_callback = on_save_callback

        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)

        self.start_point = QPoint()
        self.current_rect = QRect()
        self.rects = []  # 선택된 영역들 리스트 

        self.dash_offset = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dash_offset)
        self.timer.start(100) 

    def update_dash_offset(self):
        self.dash_offset = (self.dash_offset + 1) % 10
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            raw_point = event.position().toPoint()
            self.start_point = QPoint(
                int(raw_point.x() / self.scale_factor),
                int(raw_point.y() / self.scale_factor)
            )
            self.current_rect = QRect()
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() & Qt.LeftButton:
            raw_end_point = event.position().toPoint()
            end_point = QPoint(
                int(raw_end_point.x() / self.scale_factor),
                int(raw_end_point.y() / self.scale_factor)
            )
            self.current_rect = QRect(self.start_point, end_point).normalized()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and not self.current_rect.isNull():
            self.rects.append(self.current_rect)
            print(f"Selected rect (raw coords): {self.current_rect}")
            self.current_rect = QRect()
            self.update()


    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.DashLine)
        pen.setDashOffset(self.dash_offset)
        painter.setPen(pen)

        # 현재 드래그 중인 사각형도 확대 보정
        if not self.current_rect.isNull():
            scaled_rect = QRect(
                int(self.current_rect.x() * self.scale_factor),
                int(self.current_rect.y() * self.scale_factor),
                int(self.current_rect.width() * self.scale_factor),
                int(self.current_rect.height() * self.scale_factor),
            )
            painter.drawRect(scaled_rect)

        # 저장된 사각형들도 확대 보정
        for rect in self.rects:
            scaled_rect = QRect(
                int(rect.x() * self.scale_factor),
                int(rect.y() * self.scale_factor),
                int(rect.width() * self.scale_factor),
                int(rect.height() * self.scale_factor),
            )
            painter.drawRect(scaled_rect)


    def keyPressEvent(self, event: QKeyEvent):
        print(f"Key pressed: {event.key()}, Modifiers: {event.modifiers()}")  # 디버깅용
        # Ctrl/Cmd + Z : 실행 취소 단축키
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Z:
            if self.rects:
                self.rects.pop()
                self.update()
            event.accept()
            return
        # Ctrl/Cmd + K : 잘라내기
        elif event.key() == Qt.Key_K:
            print("Ctrl+K detected, calling on_save_callback")  # ✅ 로그 추가
            if self.rects and self.on_save_callback:
                # 현재 위젯의 이미지 가져오기
                if self.pixmap():
                    print("Ctrl+K detected, calling on_save_callback")
                    self.on_save_callback(self.pixmap(), self.rects)
            event.accept()
            return
        super().keyPressEvent(event)

    def get_regions(self):
        return self.rects

    def clear_regions(self):
        self.rects.clear()
        self.update()
