"""O carregador de fotos, sem rede: o QNetworkAccessManager é trocado por um falso."""
from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtNetwork import QNetworkReply
from PySide6.QtWidgets import QApplication

from platina_alan_wake import image_loader


def _png() -> bytes:
    pixmap = QPixmap(4, 4)
    pixmap.fill(QColor("#F2C14E"))
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    pixmap.save(buffer, "PNG")
    return bytes(data)


class _Signal:
    def __init__(self):
        self._slots = []

    def connect(self, slot):
        self._slots.append(slot)

    def disconnect(self):
        self._slots.clear()

    def emit(self):
        for slot in list(self._slots):
            slot()


class _Reply:
    def __init__(self, url):
        self.url = url
        self.finished = _Signal()
        self.status, self.data, self.error_code = 200, b"", QNetworkReply.NetworkError.NoError

    def answer(self, status=200, data=b"", error=QNetworkReply.NetworkError.NoError):
        self.status, self.data, self.error_code = status, data, error
        self.finished.emit()

    def attribute(self, _attr):
        return self.status

    def readAll(self):  # noqa: N802 (nome do Qt)
        return self.data

    def error(self):
        return self.error_code

    def errorString(self):  # noqa: N802
        return "falhou"

    def deleteLater(self):  # noqa: N802
        pass

    def abort(self):
        pass


class _Manager:
    def __init__(self):
        self.replies = []

    def get(self, request):
        reply = _Reply(request.url().toString())
        self.replies.append(reply)
        return reply


def _loader(monkeypatch, retries=0):
    QApplication.instance() or QApplication([])
    monkeypatch.setattr(image_loader, "_RETRIES", retries)
    loader = image_loader.ImageLoader()
    loader._manager = _Manager()
    return loader


def test_a_failing_callback_does_not_stall_the_queue(monkeypatch):
    loader = _loader(monkeypatch)
    monkeypatch.setattr(image_loader, "_MAX_PARALLEL", 1)
    got = []

    def explode(_pixmap):
        raise RuntimeError("widget já destruído")

    loader.load("https://exemplo.test/a.png", explode)
    loader.load("https://exemplo.test/b.png", lambda p: got.append(p))
    assert len(loader._manager.replies) == 1  # uma por vez
    loader._manager.replies[0].answer(data=_png())
    # mesmo com o callback da primeira explodindo, a segunda foi pedida
    assert len(loader._manager.replies) == 2
    loader._manager.replies[1].answer(data=_png())
    assert got and not got[0].isNull()


def test_failure_is_reported_once_after_the_automatic_retries(monkeypatch):
    loader = _loader(monkeypatch, retries=2)
    # a pausa entre tentativas vira imediata no teste
    monkeypatch.setattr(image_loader.QTimer, "singleShot",
                        staticmethod(lambda _ms, _ctx, fn: fn()))
    failures, ready = [], []
    loader.load("https://exemplo.test/c.png", ready.append, failures.append)
    for _attempt in range(3):
        loader._manager.replies[-1].answer(status=403)
    assert len(loader._manager.replies) == 3
    assert failures == ["HTTP 403"]
    assert not ready
    assert (image_loader.guide_dir() / "fotos_falhas.log").read_text(encoding="utf-8").count("HTTP 403")


def test_retry_after_failure_downloads_again(monkeypatch):
    loader = _loader(monkeypatch)
    failures, ready = [], []
    url = "https://exemplo.test/d.png"
    loader.load(url, ready.append, failures.append)
    loader._manager.replies[-1].answer(status=0, error=QNetworkReply.NetworkError.TimeoutError)
    assert failures == ["falhou"]
    loader.load(url, ready.append, failures.append)
    loader._manager.replies[-1].answer(data=_png())
    assert len(ready) == 1
