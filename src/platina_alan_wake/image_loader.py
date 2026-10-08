"""Carrega imagens por URL com cache em disco, pelo QtNetwork.

Por que não `urllib`: as fotos deste guia vêm da GameFAQs, que recusa (403) a
conexão TLS do Python mesmo com cabeçalhos de navegador; o `curl` e o
QtNetwork passam. O QtNetwork também resolve o problema que o helper de
download do Sidekick existe para resolver, o `CERTIFICATE_VERIFY_FAILED` do
Python no macOS, porque valida o certificado pela loja do próprio sistema.

De quebra não há QThread: os downloads correm no event loop, então fechar o
app no meio de um download não derruba o processo.
"""
from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from .paths import guide_dir

log = logging.getLogger(__name__)

_USER_AGENT = (
    b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    b"(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
# Este guia tem centenas de fotos; sem um teto, abrir um episódio dispararia
# dezenas de downloads de uma vez e martelaria o host.
_MAX_PARALLEL = 6


def _cache_dir() -> Path:
    path = guide_dir() / "img_cache"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _cache_path(url: str) -> Path:
    ext = ".img"
    clean = url.lower().split("?")[0]
    for candidate in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        if clean.endswith(candidate):
            ext = candidate
            break
    return _cache_dir() / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ext)


class ImageLoader(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._manager = QNetworkAccessManager(self)
        self._queue: list[tuple[str, Path]] = []
        self._running: list[QNetworkReply] = []
        # vários widgets podem pedir a mesma foto (Rota e Coletáveis)
        self._waiting: dict[str, list[Callable[[QPixmap], None]]] = {}

    def load(self, url: str, on_ready: Callable[[QPixmap], None]) -> QPixmap | None:
        """Devolve a foto do cache na hora, ou None e chama `on_ready` depois."""
        cache = _cache_path(url)
        if cache.exists():
            pixmap = QPixmap(str(cache))
            if not pixmap.isNull():
                return pixmap
        if url in self._waiting:
            self._waiting[url].append(on_ready)
            return None
        self._waiting[url] = [on_ready]
        self._queue.append((url, cache))
        self._pump()
        return None

    def _pump(self) -> None:
        while self._queue and len(self._running) < _MAX_PARALLEL:
            url, cache = self._queue.pop(0)
            request = QNetworkRequest(QUrl(url))
            request.setRawHeader(b"User-Agent", _USER_AGENT)
            request.setRawHeader(b"Accept", b"image/avif,image/webp,image/*,*/*;q=0.8")
            request.setRawHeader(b"Accept-Language", b"pt-BR,pt;q=0.9,en;q=0.8")
            request.setTransferTimeout(20000)
            reply = self._manager.get(request)
            self._running.append(reply)
            reply.finished.connect(lambda reply=reply, url=url, cache=cache:
                                   self._finished(reply, url, cache))

    def _finished(self, reply: QNetworkReply, url: str, cache: Path) -> None:
        if reply in self._running:
            self._running.remove(reply)
        callbacks = self._waiting.pop(url, [])
        status = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        data = bytes(reply.readAll())
        failed = reply.error() != QNetworkReply.NetworkError.NoError
        error_text = reply.errorString()
        reply.deleteLater()
        pixmap = QPixmap()
        if not failed and data and pixmap.loadFromData(data):
            try:
                cache.write_bytes(data)
            except OSError as error:
                log.warning("não foi possível guardar %s no cache: %s", url, error)
            for callback in callbacks:
                callback(pixmap)
        else:
            # Falha silenciosa aqui viraria "guia sem foto nenhuma" sem explicação.
            log.warning("foto não baixada (%s, HTTP %s): %s", url, status, error_text)
        self._pump()

    def shutdown(self) -> None:
        """Cancela o que estiver na fila ou em andamento."""
        self._queue.clear()
        self._waiting.clear()
        for reply in list(self._running):
            try:
                reply.finished.disconnect()
            except (RuntimeError, TypeError):
                pass
            reply.abort()
            reply.deleteLater()
        self._running.clear()
