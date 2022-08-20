from PyQt5.QtCore import Qt, QRectF, QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QPainterPath, QPainter, QBrush, QColor, QCursor


class UiStyle(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()
        self.border_width = 8
        # 设置 窗口无边框和背景透明 *必须
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

    def paintEvent(self, event):

        # 圆角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing)  # 抗锯齿
        pat2.setBrush(QColor.fromRgb(226, 221, 215, 255))
        pat2.setPen(Qt.transparent)

        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setBottom(871)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 18)
        pat2.drawRoundedRect(rect, 0, 0)

        # 阴影
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))

        # color = QColor(192, 192, 192, 50)

        # for i in range(10):
        #     i_path = QPainterPath()
        #     i_path.setFillRule(Qt.WindingFill)
        #     ref = QRectF(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2)
        #     # i_path.addRect(ref)
        #     i_path.addRoundedRect(ref, self.border_width, self.border_width)
        #     color.setAlpha(150 - i**0.5*50)
        #     pat.setPen(color)
        #     pat.drawPath(i_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
