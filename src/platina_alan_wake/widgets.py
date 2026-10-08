"""Componentes que respeitam a largura disponível no guia."""
from PySide6.QtCore import QPointF, QSize, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QCheckBox, QLabel, QSizePolicy, QStyle, QStyleOptionButton, QVBoxLayout,
)

from . import guide_data


class ChecklistBox(QCheckBox):
    """Caixa de marcar com texto que quebra linha.

    O QCheckBox comum não quebra o texto: numa coluna estreita a frase é cortada.
    Aqui o texto mora num QLabel com quebra, e o clique em qualquer ponto da
    linha marca a caixa.
    """

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.setAccessibleName(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.caption = QLabel(text, self)
        self.caption.setWordWrap(True)
        self.caption.setTextFormat(Qt.TextFormat.RichText)
        self.caption.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 3, 4, 3)
        layout.addWidget(self.caption)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def sizeHint(self):
        return self.layout().sizeHint()

    def minimumSizeHint(self):
        return QSize(100, self.layout().minimumSize().height())

    def hitButton(self, pos):
        return self.rect().contains(pos)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isChecked():
            option = QStyleOptionButton()
            self.initStyleOption(option)
            rect = self.style().subElementRect(
                QStyle.SubElement.SE_CheckBoxIndicator, option, self)
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor(guide_data.ACCENT), 2.2))
            painter.drawLine(QPointF(rect.left() + 4, rect.center().y()),
                             QPointF(rect.left() + 8, rect.bottom() - 4))
            painter.drawLine(QPointF(rect.left() + 8, rect.bottom() - 4),
                             QPointF(rect.right() - 3, rect.top() + 4))


class GuideImage(QLabel):
    """Imagem que se ajusta à largura disponível e informa a altura real.

    Implementa heightForWidth, que é como o Qt pergunta "de quanta altura você
    precisa nesta largura". Sem isso o layout reserva menos espaço do que a
    figura ocupa e ela invade o texto seguinte.
    """

    def __init__(self, max_width: int = 640, max_height: int = 360, parent=None):
        super().__init__(parent)
        self._source = QPixmap()
        self._max_width = max_width
        self._max_height = max_height
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        policy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.setMinimumWidth(0)

    def set_source(self, pixmap: QPixmap) -> None:
        self._source = pixmap
        self.setText("")
        self._fit()
        self.updateGeometry()

    def _scaled_size(self, width: int) -> QSize:
        if self._source.isNull():
            return QSize(0, 0)
        usable = max(80, min(width, self._max_width))
        return self._source.size().scaled(
            usable, self._max_height, Qt.AspectRatioMode.KeepAspectRatio)

    def _fit(self) -> None:
        if self._source.isNull():
            return
        target = self._scaled_size(self.width())
        self.setPixmap(self._source.scaled(
            target, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation))
        self.setMinimumHeight(target.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._fit()

    def hasHeightForWidth(self):
        return not self._source.isNull()

    def heightForWidth(self, width):
        return self._scaled_size(width).height()

    def sizeHint(self):
        if self._source.isNull():
            return super().sizeHint()
        width = self.width() or self._max_width
        return QSize(self._max_width, self._scaled_size(width).height())

    def minimumSizeHint(self):
        return QSize(0, 0) if self._source.isNull() else QSize(0, 60)
