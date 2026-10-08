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
from datetime import datetime
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, QTimer, QUrl
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
_TIMEOUT_MS = 30000  # sem receber nada por 30 s, desiste desta tentativa
_RETRIES = 2  # tentativas extras automáticas antes de mostrar "Tentar de novo"
_RETRY_PAUSE_MS = 2000


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


def _remember_failure(url: str, reason: str) -> None:
    """Guarda as últimas falhas num arquivo na pasta do guia.

    O `log` sozinho não aparece em lugar nenhum dentro do app empacotado; com o
    arquivo dá para saber depois se foi o site (HTTP 403, 429), a rede ou o
    tempo esgotado.
    """
    path = guide_dir() / "fotos_falhas.log"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()[-199:] if path.exists() else []
        lines.append(f"{datetime.now().isoformat(timespec='seconds')}  {reason}  {url}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError:
        pass


class ImageLoader(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._manager = QNetworkAccessManager(self)
        self._queue: list[tuple[str, Path]] = []
        self._running: list[QNetworkReply] = []
        # vários widgets podem pedir a mesma foto (Rota e Coletáveis)
        self._waiting: dict[str, list[tuple[Callable, Callable | None]]] = {}
        self._attempts: dict[str, int] = {}

    def load(self, url: str, on_ready: Callable[[QPixmap], None],
             on_fail: Callable[[str], None] | None = None) -> QPixmap | None:
        """Devolve a foto do cache na hora, ou None e responde depois.

        Responde SEMPRE uma vez: `on_ready(pixmap)` quando a foto chega, ou
        `on_fail(motivo)` depois de esgotar as tentativas. É isso que deixa a
        página mostrar "não carregou" só quando não carregou de verdade.
        """
        cache = _cache_path(url)
        if cache.exists():
            pixmap = QPixmap(str(cache))
            if not pixmap.isNull():
                return pixmap
        if url in self._waiting:
            self._waiting[url].append((on_ready, on_fail))
            return None
        self._waiting[url] = [(on_ready, on_fail)]
        self._attempts[url] = 0
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
            request.setTransferTimeout(_TIMEOUT_MS)
            reply = self._manager.get(request)
            self._running.append(reply)
            reply.finished.connect(lambda reply=reply, url=url, cache=cache:
                                   self._finished(reply, url, cache))

    def _finished(self, reply: QNetworkReply, url: str, cache: Path) -> None:
        # try/finally: se qualquer coisa abaixo der erro, a fila tem que andar.
        # Antes uma exceção aqui pulava o _pump() e as fotos restantes nunca
        # eram pedidas.
        try:
            self._settle(reply, url, cache)
        finally:
            self._pump()

    def _settle(self, reply: QNetworkReply, url: str, cache: Path) -> None:
        if reply in self._running:
            self._running.remove(reply)
        status = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        data = bytes(reply.readAll())
        failed = reply.error() != QNetworkReply.NetworkError.NoError
        error_text = reply.errorString()
        reply.deleteLater()
        if url not in self._waiting:
            return  # cancelado no meio do caminho
        pixmap = QPixmap()
        if not failed and data and pixmap.loadFromData(data):
            try:
                cache.write_bytes(data)
            except OSError as error:
                log.warning("não foi possível guardar %s no cache: %s", url, error)
            self._attempts.pop(url, None)
            for on_ready, _on_fail in self._waiting.pop(url):
                self._call(on_ready, pixmap)
            return
        reason = f"HTTP {status}" if status and status != 200 else (error_text or "resposta vazia")
        attempt = self._attempts.get(url, 0) + 1
        self._attempts[url] = attempt
        if attempt <= _RETRIES:
            # Falha de rede costuma ser passageira: tenta de novo sozinho, com
            # uma pausa que cresce, antes de mostrar o botão para o jogador.
            QTimer.singleShot(_RETRY_PAUSE_MS * attempt, self,
                              lambda url=url, cache=cache: self._requeue(url, cache))
            return
        log.warning("foto não baixada (%s): %s", url, reason)
        _remember_failure(url, reason)
        self._attempts.pop(url, None)
        for _on_ready, on_fail in self._waiting.pop(url):
            if on_fail is not None:
                self._call(on_fail, reason)

    def _requeue(self, url: str, cache: Path) -> None:
        if url in self._waiting:
            self._queue.append((url, cache))
            self._pump()

    @staticmethod
    def _call(callback: Callable, value) -> None:
        try:
            callback(value)
        except Exception:  # widget que já sumiu não pode travar as outras fotos
            log.exception("callback de foto falhou")

    def shutdown(self) -> None:
        """Cancela tudo. Só para quando o app está fechando de verdade."""
        self._queue.clear()
        self._waiting.clear()
        self._attempts.clear()
        for reply in list(self._running):
            try:
                reply.finished.disconnect()
            except (RuntimeError, TypeError):
                pass
            reply.abort()
            reply.deleteLater()
        self._running.clear()
