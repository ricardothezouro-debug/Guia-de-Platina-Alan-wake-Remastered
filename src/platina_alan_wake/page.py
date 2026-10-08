"""Página do guia: cinco abas, com a Rota (os seis episódios) no centro."""
from __future__ import annotations

import html
import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFileDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget,
)

from . import guide_data
from . import progress as keys
from .image_loader import ImageLoader
from .paths import guide_dir_label
from .storage import load_progress, load_ui, save_progress, save_ui
from .topbar import InfoCorner, TopBar
from .widgets import ChecklistBox, GuideImage

_SEARCH_LIMIT = 18

# Cores de tier da convenção da aba Platinas (GUIA_DE_PLATINA.md, seção 2).
_TIER_COLORS = {
    "bronze": "#CD7F32", "prata": "#C0C0C0", "ouro": "#FFD700", "platina": "#E5E4E2",
}
# o aviso no meio da rota: vermelho é o que pode escapar
_TAG_COLORS = {"perdível": "#F87171", "troféu": "#7FE7FF", "dica": "#A8B0BC"}
_CAT_COLORS = {
    "história": "#A8B0BC", "perdível": "#F87171", "desafio": "#FF9E64",
    "combate": "#7FE7FF", "coletável": guide_data.ACCENT, "dificuldade": "#C4A7FF",
    "platina": "#E5E4E2",
}
# cada tipo de coletável tem uma cor, para bater o olho na lista
_KIND_COLORS = {
    "page": guide_data.ACCENT, "nm": "#C4A7FF", "thermos": "#E8A25C",
    "chest": "#B9FF43", "can": "#7FE7FF", "radio": "#FF9E64", "tv": "#9AC8FF",
    "sign": "#E7E7E7",
}
_KIND_PLURAL = {
    "page": "Páginas do manuscrito", "nm": "Páginas do Pesadelo",
    "thermos": "Garrafas de café", "chest": "Baús escondidos",
    "can": "Pirâmides de latas", "radio": "Programas de rádio",
    "tv": "Programas de TV", "sign": "Placas",
}

_PROGRESS_QSS = (
    "QProgressBar{background:#0B111A;border:1px solid #273140;border-radius:9px;"
    "min-height:18px;text-align:center;color:#F3F6FF;font-weight:600}"
    "QProgressBar::chunk{border-radius:8px;background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
    "stop:0 #8C6A1F,stop:0.6 %s,stop:1 #FFF1C9)}" % guide_data.ACCENT
)
_NAV_QSS = (
    "QPushButton#NavButton{background:#0D121B;border:1px solid #273140;border-radius:8px;"
    "padding:7px 10px;color:#A8B0BC;text-align:left}"
    "QPushButton#NavButton:hover{border-color:#3C4A5C;color:#F3F6FF}"
    "QPushButton#NavButton:checked{background:#16140C;border-color:%s;color:#F3F6FF;"
    "font-weight:600}" % guide_data.ACCENT
)
_ITEM_QSS = "QFrame#ItemBlock{background:#0B111A;border:1px solid #1E2733;border-radius:8px}"


def _norm(text) -> str:
    stripped = unicodedata.normalize("NFD", str(text or ""))
    return "".join(c for c in stripped if not unicodedata.combining(c)).lower()


def _esc(text) -> str:
    return html.escape(str(text or ""))


def _label(text: str, object_name: str = "", wrap: bool = True) -> QLabel:
    label = QLabel(str(text or ""))
    if object_name:
        label.setObjectName(object_name)
    label.setWordWrap(wrap)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    return label


def _link(text: str, url: str) -> QLabel:
    label = QLabel(f'<a href="{_esc(url)}" style="color:{guide_data.ACCENT}">{_esc(text)}</a>')
    label.setOpenExternalLinks(True)
    label.setWordWrap(True)
    return label


def _card() -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName("NeonPanel")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(14, 12, 14, 12)
    layout.setSpacing(6)
    return frame, layout


def _pill(text: str) -> QLabel:
    label = QLabel(str(text or ""))
    label.setObjectName("StatusPill")
    label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
    return label


def _tag(text: str, color: str) -> QLabel:
    label = QLabel(str(text or "").upper())
    label.setStyleSheet(f"color:{color};font-weight:700;font-size:11px;")
    label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
    return label


def _toggle(text_closed: str, text_open: str, body: QWidget, on_open=None) -> QPushButton:
    """Botão de abrir e recolher. `on_open` roda só na primeira abertura."""
    button = QPushButton(text_closed)
    button.setCheckable(True)
    button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
    opened = [False]

    def flip(checked: bool) -> None:
        if checked and not opened[0]:
            opened[0] = True
            if on_open is not None:
                on_open()
        body.setVisible(checked)
        button.setText(text_open if checked else text_closed)

    button.toggled.connect(flip)
    body.hide()
    return button


def _scroll_page(build_content) -> QWidget:
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 10, 0)
    layout.setSpacing(12)
    build_content(layout)
    layout.addStretch(1)

    scroll = QScrollArea()
    scroll.setObjectName("PageScroll")
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setWidget(container)
    return scroll


def _kind_label(step: dict) -> str:
    name, total = guide_data.KINDS[step["type"]]
    return f"{name} {step['n']}/{total}"


def _trophy_names(ids) -> str:
    return ", ".join(guide_data.trophy_by_id(i)["en"] for i in ids)


class GuidePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._done = load_progress()
        ui = load_ui()
        self._hide_done = bool(ui.get("hide_done", False))
        self._show_nm = bool(ui.get("show_nm", True))
        self._image_loader = ImageLoader(self)
        self._boxes: dict[str, list[QCheckBox]] = {}
        self._built: set[int] = set()
        # linhas da Rota que os filtros escondem: (widget, chave, tipo)
        self._route_rows: list[tuple[QWidget, str, str]] = []
        self._episode_pills: list[tuple[QLabel, dict]] = []
        self._kind_pills: list[tuple[QLabel, str]] = []
        self._trophy_rows: list[tuple[QWidget, str, str, str]] = []
        # fotos cujo download falhou: cada item é a função que pede de novo
        self._failed_photos: set = set()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 22, 0)
        outer.setSpacing(12)
        self._build_header()
        self._build_progress()
        self._build_nav()
        self.top = TopBar(
            self, title=self._title_box, header=self._header_box,
            progress=self._progress_box, nav=self._nav_box, bar=self.progress,
            pills=self._progress_pills, load_ui=load_ui, save_ui=save_ui)
        outer.addWidget(self.top.widget)

        self.stack = QStackedWidget()
        self._holders: list[QVBoxLayout] = []
        for _section in guide_data.SECTIONS:
            placeholder = QWidget()
            holder = QVBoxLayout(placeholder)
            holder.setContentsMargins(0, 0, 0, 0)
            holder.addWidget(_label("Carregando…", "Muted"))
            holder.addStretch(1)
            self._holders.append(holder)
            self.stack.addWidget(placeholder)
        self.stack.currentChanged.connect(self._ensure_built)
        outer.addWidget(self.stack, 1)
        # O caminho é montado na hora: cada sistema guarda numa pasta diferente.
        outer.addWidget(InfoCorner(
            f"{guide_data.FOOTER} • progresso salvo em {guide_dir_label()}"))

        self._update_progress()
        # A primeira aba só é montada depois que o event loop girar, para que
        # build_page() retorne na hora (regra do padrão de plugins).
        QTimer.singleShot(0, lambda: self._ensure_built(0))

        # Downloads em andamento precisam acabar antes que o Qt destrua a
        # página, senão o processo aborta ao fechar ou atualizar o plugin.
        app = QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self._image_loader.shutdown)

    def closeEvent(self, event):  # noqa: N802 (assinatura do Qt)
        self._image_loader.shutdown()
        super().closeEvent(event)

    # ------------------------------------------------------------------ topo
    def _build_header(self) -> None:
        """Só as peças do topo de três níveis (ver topbar.py)."""
        self._title_box = QWidget()
        title_row = QHBoxLayout(self._title_box)
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.addWidget(_label(guide_data.GAME_NAME, "PageTitle", wrap=False), 1)

        self._header_box = QWidget()
        box = QVBoxLayout(self._header_box)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(12)
        box.addWidget(_label(guide_data.INTRO, "Muted"))
        stats = QHBoxLayout()
        stats.setSpacing(8)
        for stat in guide_data.HERO_STATS:
            stats.addWidget(_pill(f"{stat['value']}  {stat['label']}"))
        stats.addStretch(1)
        box.addLayout(stats)
        self._build_search(box)
        self._build_toolbar(box)

    def _build_search(self, outer: QVBoxLayout) -> None:
        row = QHBoxLayout()
        row.setSpacing(8)
        self.global_search = QLineEdit()
        self.global_search.setPlaceholderText(
            "Buscar coletável ou troféu… Ex.: garrafa 57, placa, Stucky, jukebox, Pesadelo")
        self.global_search.textChanged.connect(self._global_search)
        clear = QPushButton("Limpar")
        clear.clicked.connect(lambda: self.global_search.setText(""))
        row.addWidget(self.global_search, 1)
        row.addWidget(clear, 0)
        outer.addLayout(row)

        self.results_box = QWidget()
        self.results_layout = QVBoxLayout(self.results_box)
        self.results_layout.setContentsMargins(0, 0, 0, 0)
        self.results_layout.setSpacing(6)
        self.results_box.hide()
        outer.addWidget(self.results_box)

    def _build_toolbar(self, outer: QVBoxLayout) -> None:
        row = QHBoxLayout()
        row.setSpacing(8)
        for text, slot in (("Exportar progresso", self._export),
                           ("Importar progresso", self._import),
                           ("Resetar marcações", self._reset)):
            button = QPushButton(text)
            button.clicked.connect(slot)
            row.addWidget(button)
        row.addStretch(1)
        outer.addLayout(row)

    def _build_progress(self) -> None:
        self._progress_box = QWidget()
        row = QHBoxLayout(self._progress_box)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        self.progress = QProgressBar()
        self.progress.setStyleSheet(_PROGRESS_QSS)
        self.progress.setRange(0, max(1, len(keys.all_keys())))
        self.progress_label = _pill("")
        self.trophy_label = _pill("")
        self.page_label = _pill("")
        self.thermos_label = _pill("")
        for widget in (self.progress_label, self.trophy_label, self.page_label,
                       self.thermos_label):
            row.addWidget(widget, 0)
        row.insertWidget(0, self.progress, 1)
        self._progress_pills = [self.progress_label, self.trophy_label,
                                self.page_label, self.thermos_label]

    def _build_nav(self) -> None:
        holder = QWidget()
        holder.setStyleSheet(_NAV_QSS)
        grid = QGridLayout(holder)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(6)
        self._nav_buttons: list[QPushButton] = []
        for i, section in enumerate(guide_data.SECTIONS):
            button = QPushButton(f"{section['num']}  {section['nav']}")
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.setChecked(i == 0)
            button.clicked.connect(lambda _=False, index=i: self.show_section(index))
            grid.addWidget(button, 0, i)
            self._nav_buttons.append(button)
            grid.setColumnStretch(i, 1)
        self._nav_box = holder

    def show_section(self, index: int) -> None:
        for i, button in enumerate(self._nav_buttons):
            button.setChecked(i == index)
        self.stack.setCurrentIndex(index)

    # -------------------------------------------------------------- progresso
    def _checkbox(self, key: str, text: str) -> ChecklistBox:
        box = ChecklistBox(text)
        box.setChecked(key in self._done)
        box.toggled.connect(lambda checked, k=key: self._on_toggle(k, checked))
        self._boxes.setdefault(key, []).append(box)
        return box

    def _on_toggle(self, key: str, checked: bool) -> None:
        if checked:
            self._done.add(key)
        else:
            self._done.discard(key)
        live = []
        for box in self._boxes.get(key, []):
            try:
                if box.isChecked() != checked:
                    box.blockSignals(True)
                    box.setChecked(checked)
                    box.blockSignals(False)
                live.append(box)
            except RuntimeError:
                continue  # resultado de busca já descartado
        self._boxes[key] = live
        save_progress(self._done)
        self._update_progress()
        if self._hide_done:
            self._apply_route_filters()

    def _count(self, key_list: list[str]) -> int:
        return sum(1 for key in key_list if key in self._done)

    def _update_progress(self) -> None:
        all_keys = keys.all_keys()
        done = self._count(all_keys)
        percent = round(done / len(all_keys) * 100) if all_keys else 0
        self.progress.setValue(done)
        self.progress_label.setText(f"{done}/{len(all_keys)}  •  {percent}%")
        trophies = keys.trophy_keys()
        self.trophy_label.setText(f"{self._count(trophies)}/{len(trophies)} troféus")
        pages = keys.collectible_keys("page") + keys.collectible_keys("nm")
        self.page_label.setText(f"{self._count(pages)}/{len(pages)} páginas")
        thermos = keys.collectible_keys("thermos")
        self.thermos_label.setText(f"{self._count(thermos)}/{len(thermos)} garrafas")
        for pill, episode in self._episode_pills:
            episode_keys = keys.episode_keys(episode)
            pill.setText(f"{self._count(episode_keys)}/{len(episode_keys)}")
        for pill, kind in self._kind_pills:
            kind_keys = keys.collectible_keys(kind)
            pill.setText(f"{self._count(kind_keys)}/{len(kind_keys)}")
        if hasattr(self, "top"):
            self.top.sync()

    def _refresh_boxes(self) -> None:
        for key, boxes in self._boxes.items():
            checked = key in self._done
            for box in boxes:
                try:
                    box.blockSignals(True)
                    box.setChecked(checked)
                    box.blockSignals(False)
                except RuntimeError:
                    continue
        self._update_progress()
        self._apply_route_filters()

    # ------------------------------------------------------ exportar/importar
    def _export(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar progresso", "alan-wake-platina-progresso.json", "JSON (*.json)")
        if not path:
            return
        payload = {
            "guide": guide_data.GUIDE_ID, "version": 1,
            "exportedAt": datetime.now(timezone.utc).isoformat(),
            "state": {key: True for key in sorted(self._done)},
        }
        try:
            Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
        except OSError as error:
            QMessageBox.warning(self, "Exportar", f"Não foi possível salvar: {error}")

    def _import(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Importar progresso", "", "JSON (*.json)")
        if not path:
            return
        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            QMessageBox.warning(self, "Importar", "Arquivo JSON inválido.")
            return
        state = raw.get("state", raw) if isinstance(raw, dict) else raw
        self._done = keys.normalize_imported(state)
        save_progress(self._done)
        self._refresh_boxes()

    def _reset(self) -> None:
        if QMessageBox.question(self, "Resetar marcações",
                                "Apagar todas as marcações deste guia?") != \
                QMessageBox.StandardButton.Yes:
            return
        self._done = set()
        save_progress(self._done)
        self._refresh_boxes()

    # ------------------------------------------------------------------ fotos
    def _photo(self, image_id: int | None, caption: str) -> QWidget:
        """A foto de um passo, com "Tentar de novo" se o download falhar.

        O aviso de falha só aparece quando o carregador desiste de verdade
        (depois das tentativas automáticas), nunca por cronômetro: antes um
        timer de 26 s marcava como indisponível foto que ainda estava na fila.
        """
        box = QWidget()
        column = QVBoxLayout(box)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(4)
        image = GuideImage(560, 316)
        image.setObjectName("Muted")
        column.addWidget(image)
        if image_id is None:
            return box
        url = guide_data.IMG.format(image_id)
        image.setToolTip(caption)

        failed_row = QWidget()
        row = QHBoxLayout(failed_row)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        reason_label = _label("", "Muted")
        retry = QPushButton("Tentar de novo")
        retry.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        row.addWidget(reason_label, 1)
        row.addWidget(retry)
        row.addWidget(_link("Abrir no navegador", url))
        failed_row.hide()
        column.addWidget(failed_row)

        def show(pixmap) -> None:
            failed_row.hide()
            image.show()
            image.set_source(pixmap)
            self._failed_photos.discard(request)

        def fail(reason: str) -> None:
            image.hide()  # sem foto, o espaço dela vira só uma faixa vazia
            reason_label.setText(f"A foto não carregou ({reason}).")
            failed_row.show()
            self._failed_photos.add(request)

        def request() -> None:
            failed_row.hide()
            image.show()
            image.setText("Carregando foto…")
            cached = self._image_loader.load(url, show, fail)
            if cached is not None:
                show(cached)

        retry.clicked.connect(request)
        request()
        return box

    def _retry_failed_photos(self) -> None:
        """O botão do topo da Rota: pede de novo todas as fotos que falharam."""
        for request in list(self._failed_photos):
            self._failed_photos.discard(request)
            try:
                request()
            except RuntimeError:
                continue

    # ------------------------------------------------------- construção lazy
    def _ensure_built(self, index: int) -> None:
        if index in self._built or index < 0:
            return
        self._built.add(index)
        holder = self._holders[index]
        while holder.count():
            item = holder.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        builder = getattr(self, f"_build_{guide_data.SECTIONS[index]['key']}")
        holder.addWidget(_scroll_page(builder))
        self._update_progress()

    # ------------------------------------------------------------- aba Plano
    def _build_plan(self, layout: QVBoxLayout) -> None:
        layout.addWidget(_label("Duas zeradas, nesta ordem", "SectionTitle"))
        for step in guide_data.PLAN:
            frame, box = _card()
            box.addWidget(self._checkbox(keys.plan_key(step["id"]), f"<b>{_esc(step['title'])}</b>"))
            box.addWidget(_label(step["text"]))
            if step["detail"]:
                box.addWidget(_label(step["detail"], "Muted"))
            layout.addWidget(frame)

        frame, box = _card()
        box.addWidget(_label("Os perdíveis, de relance", "SectionTitle"))
        box.addWidget(_label(
            "Nenhum troféu fica perdido de vez: o Seleção de Episódio refaz qualquer "
            "trecho. Mesmo assim, resolver no ponto certo poupa horas de replay.", "Muted"))
        for trophy in guide_data.TROPHIES:
            if trophy["cat"] in ("perdível", "desafio"):
                color = _CAT_COLORS[trophy["cat"]]
                box.addWidget(_label(
                    f"<span style='color:{color};font-weight:700'>{_esc(trophy['cat'].upper())}"
                    f"</span>  <b>{_esc(trophy['en'])}</b>: {_esc(trophy['tip'])}"))
        layout.addWidget(frame)

        frame, box = _card()
        box.addWidget(_label("Regras que valem para o jogo todo", "SectionTitle"))
        for rule in guide_data.RULES:
            box.addWidget(_label(f"• {_esc(rule)}"))
        layout.addWidget(frame)

        frame, box = _card()
        box.addWidget(_label("Fontes", "SectionTitle"))
        box.addWidget(_label(
            "As fotos são capturas do guia de PS5 da GameFAQs, exibidas a partir do "
            "site dele. Os textos deste guia são próprios.", "Muted"))
        for text, url in guide_data.SOURCES:
            box.addWidget(_link(text, url))
        layout.addWidget(frame)

    # -------------------------------------------------------------- aba Rota
    def _build_route(self, layout: QVBoxLayout) -> None:
        intro, box = _card()
        box.addWidget(_label(
            "Abra o episódio que você vai jogar e siga de cima para baixo. Cada "
            "coletável traz o marco que localiza ele e a foto do lugar. Os avisos "
            "em vermelho são os perdíveis: resolva antes de seguir.", "Muted"))
        filters = QHBoxLayout()
        filters.setSpacing(16)
        hide = QCheckBox("Esconder o que já marquei")
        hide.setChecked(self._hide_done)
        hide.toggled.connect(lambda checked: self._set_filter("hide_done", checked))
        show_nm = QCheckBox("Mostrar as páginas do Pesadelo")
        show_nm.setChecked(self._show_nm)
        show_nm.toggled.connect(lambda checked: self._set_filter("show_nm", checked))
        filters.addWidget(hide)
        filters.addWidget(show_nm)
        reload_photos = QPushButton("Recarregar fotos que falharam")
        reload_photos.clicked.connect(self._retry_failed_photos)
        filters.addStretch(1)
        filters.addWidget(reload_photos)
        box.addLayout(filters)
        layout.addWidget(intro)

        first_pending = next(
            (episode for episode in guide_data.EPISODES
             if self._count(keys.episode_keys(episode)) < len(keys.episode_keys(episode))),
            guide_data.EPISODES[0])
        for episode in guide_data.EPISODES:
            layout.addWidget(self._episode_card(episode, open_now=episode is first_pending))

    def _set_filter(self, name: str, value: bool) -> None:
        if name == "hide_done":
            self._hide_done = value
        else:
            self._show_nm = value
        ui = load_ui()
        ui[name] = value
        save_ui(ui)
        self._apply_route_filters()

    def _apply_route_filters(self) -> None:
        live = []
        for widget, key, kind in self._route_rows:
            try:
                hidden = (self._hide_done and key in self._done) or \
                    (kind == "nm" and not self._show_nm)
                widget.setVisible(not hidden)
                live.append((widget, key, kind))
            except RuntimeError:
                continue
        self._route_rows = live

    def _episode_card(self, episode: dict, open_now: bool) -> QFrame:
        frame, box = _card()
        head = QHBoxLayout()
        head.setSpacing(10)
        head.addWidget(_label(f"EPISÓDIO {episode['num']}", "Kicker", wrap=False))
        head.addWidget(_label(f"<b>{_esc(episode['title'])}</b>", "CardTitle"), 1)
        pill = _pill("")
        pill.setToolTip("Coletáveis e perdíveis marcados neste episódio")
        self._episode_pills.append((pill, episode))
        head.addWidget(pill)
        box.addLayout(head)
        box.addWidget(_label(episode["summary"], "Muted"))

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(0, 6, 0, 0)
        body_layout.setSpacing(10)
        button = _toggle("Abrir episódio ▼", "Recolher episódio ▲", body,
                         on_open=lambda: self._fill_episode(episode, body_layout))
        box.addWidget(button)
        box.addWidget(body)
        if open_now:
            button.setChecked(True)
        return frame

    def _fill_episode(self, episode: dict, layout: QVBoxLayout) -> None:
        for section in episode["sections"]:
            layout.addWidget(_label(section["title"], "SectionTitle"))
            for step in section["steps"]:
                if step["type"] == "tip":
                    layout.addWidget(self._tip_block(step))
                else:
                    row = self._item_block(step, with_photo=True)
                    layout.addWidget(row)
                    self._route_rows.append(
                        (row, keys.item_key(step["type"], step["n"]), step["type"]))
        layout.addWidget(self._checklist_block(episode))
        self._apply_route_filters()
        self._update_progress()

    def _item_block(self, step: dict, with_photo: bool, episode: dict | None = None) -> QFrame:
        frame = QFrame()
        frame.setObjectName("ItemBlock")
        frame.setStyleSheet(_ITEM_QSS)
        box = QVBoxLayout(frame)
        box.setContentsMargins(10, 8, 10, 10)
        box.setSpacing(4)
        color = _KIND_COLORS[step["type"]]
        title = f"<span style='color:{color};font-weight:700'>{_esc(_kind_label(step))}</span>"
        if step["title"]:
            title += f"  <span style='color:#C7D0DD'>{_esc(step['title'])}</span>"
        if episode is not None:
            title += f"  <span style='color:#7D8796'>· Episódio {episode['num']}</span>"
        box.addWidget(self._checkbox(keys.item_key(step["type"], step["n"]), title))
        where = _label(step["where"], "Muted")
        where.setContentsMargins(30, 0, 0, 0)
        box.addWidget(where)
        if step["img"] is not None:
            if with_photo:
                holder = QWidget()
                holder_layout = QVBoxLayout(holder)
                holder_layout.setContentsMargins(30, 4, 0, 0)
                holder_layout.addWidget(self._photo(step["img"], step["where"]))
                box.addWidget(holder)
            else:
                holder = QWidget()
                holder_layout = QVBoxLayout(holder)
                holder_layout.setContentsMargins(30, 4, 0, 0)
                button = _toggle("Ver foto ▼", "Esconder foto ▲", holder,
                                 on_open=lambda: holder_layout.addWidget(
                                     self._photo(step["img"], step["where"])))
                row = QHBoxLayout()
                row.setContentsMargins(30, 0, 0, 0)
                row.addWidget(button)
                row.addStretch(1)
                box.addLayout(row)
                box.addWidget(holder)
        return frame

    def _tip_block(self, step: dict) -> QFrame:
        color = _TAG_COLORS[step["tag"]]
        frame = QFrame()
        frame.setObjectName("NeonPanel")
        frame.setStyleSheet(
            "QFrame#NeonPanel{background:#0D121B;border:1px solid #273140;"
            "border-left:3px solid %s;border-radius:10px}" % color)
        box = QVBoxLayout(frame)
        box.setContentsMargins(14, 10, 14, 10)
        box.setSpacing(5)
        head = QHBoxLayout()
        head.addWidget(_tag(step["tag"], color))
        if step["trophies"]:
            head.addWidget(_label(_trophy_names(step["trophies"]), "Muted", wrap=True), 1)
        else:
            head.addStretch(1)
        box.addLayout(head)
        box.addWidget(_label(step["text"]))
        if step["img"] is not None:
            box.addWidget(self._photo(step["img"], step["text"]))
        if step["tag"] == "perdível":
            box.addWidget(self._checkbox(keys.tip_key(step["key"]), "Resolvido"))
        return frame

    def _checklist_block(self, episode: dict) -> QFrame:
        frame, box = _card()
        box.addWidget(_label("Fim do episódio: confira as Estatísticas", "SectionTitle"))
        totals = episode["checklist"]
        lines = []
        for kind, (name, total) in guide_data.KINDS.items():
            if kind == "nm":
                continue
            value = totals[kind]
            if kind == "page":
                lines.append(f"Páginas: {value}/91 (no Pesadelo, {value + totals['nm']}/106)")
            else:
                lines.append(f"{_KIND_PLURAL[kind]}: {value}/{total}")
        box.addWidget(_label(
            "Antes do episódio seguinte, o menu de pausa deve mostrar estes totais "
            "(acumulados desde o Episódio 1). Se algum número não bater, volte nesta "
            "lista com “Esconder o que já marquei” ligado.", "Muted"))
        box.addWidget(_label("<br>".join(_esc(line) for line in lines)))
        box.addWidget(_label(episode["end"], "Muted"))
        return frame

    # -------------------------------------------------------- aba Coletáveis
    def _build_collect(self, layout: QVBoxLayout) -> None:
        intro, box = _card()
        box.addWidget(_label(
            "Os mesmos itens da Rota, agrupados por tipo. Marcar aqui marca lá. Use "
            "para conferir o que falta de cada coleção; a foto abre sob demanda.",
            "Muted"))
        layout.addWidget(intro)
        by_kind: dict[str, list[tuple[dict, dict]]] = {kind: [] for kind in guide_data.KINDS}
        for episode, _section, step in keys.collectibles():
            by_kind[step["type"]].append((episode, step))
        for kind, items in by_kind.items():
            frame, box = _card()
            head = QHBoxLayout()
            head.addWidget(_label(
                f"<span style='color:{_KIND_COLORS[kind]}'>■</span> <b>{_esc(_KIND_PLURAL[kind])}</b>",
                "SectionTitle"), 1)
            pill = _pill("")
            self._kind_pills.append((pill, kind))
            head.addWidget(pill)
            box.addLayout(head)
            box.addWidget(_label(
                "Troféus: " + _trophy_names(guide_data.KIND_TROPHIES[kind]), "Muted"))
            body = QWidget()
            body_layout = QVBoxLayout(body)
            body_layout.setContentsMargins(0, 4, 0, 0)
            body_layout.setSpacing(6)

            def fill(items=items, body_layout=body_layout) -> None:
                for episode, step in items:
                    body_layout.addWidget(self._item_block(step, with_photo=False, episode=episode))

            box.addWidget(_toggle(f"Ver os {len(items)} ▼", "Recolher ▲", body, on_open=fill))
            box.addWidget(body)
            layout.addWidget(frame)

    # ----------------------------------------------------------- aba Troféus
    def _build_trophies(self, layout: QVBoxLayout) -> None:
        controls = QHBoxLayout()
        controls.setSpacing(8)
        self.trophy_search = QLineEdit()
        self.trophy_search.setPlaceholderText("Buscar troféu ou condição…")
        self.trophy_filter = QComboBox()
        self.trophy_filter.addItem("Todas as categorias", "")
        for category in ("perdível", "desafio", "coletável", "combate", "história",
                         "dificuldade"):
            self.trophy_filter.addItem(category.capitalize(), category)
        self.trophy_hide = QCheckBox("Esconder os que já tenho")
        controls.addWidget(self.trophy_search, 1)
        controls.addWidget(self.trophy_filter)
        controls.addWidget(self.trophy_hide)
        layout.addLayout(controls)
        for trophy in guide_data.TROPHIES:
            frame, box = _card()
            key = keys.trophy_key(trophy["id"])
            box.addWidget(self._checkbox(key, f"<b>{_esc(trophy['en'])}</b>"))
            tags = QHBoxLayout()
            tags.setContentsMargins(30, 0, 0, 0)
            tags.addWidget(_tag(trophy["tier"], _TIER_COLORS[trophy["tier"]]))
            if trophy["cat"] != trophy["tier"]:
                tags.addWidget(_tag(trophy["cat"], _CAT_COLORS[trophy["cat"]]))
            tags.addStretch(1)
            box.addLayout(tags)
            tip = _label(trophy["tip"], "Muted")
            tip.setContentsMargins(30, 0, 0, 0)
            box.addWidget(tip)
            haystack = _norm(f"{trophy['en']} {trophy['tip']} {trophy['cat']}")
            self._trophy_rows.append((frame, haystack, trophy["cat"], key))
            layout.addWidget(frame)
        self.trophy_search.textChanged.connect(self._filter_trophies)
        self.trophy_filter.currentIndexChanged.connect(self._filter_trophies)
        self.trophy_hide.toggled.connect(self._filter_trophies)

    def _filter_trophies(self) -> None:
        query = _norm(self.trophy_search.text()).strip()
        category = self.trophy_filter.currentData() or ""
        hide = self.trophy_hide.isChecked()
        for frame, haystack, cat, key in self._trophy_rows:
            visible = (not query or query in haystack) and (not category or cat == category) \
                and not (hide and key in self._done)
            frame.setVisible(visible)

    # --------------------------------------------------------- aba Expansões
    def _build_dlc(self, layout: QVBoxLayout) -> None:
        intro, box = _card()
        box.addWidget(_label("Fora da platina", "SectionTitle"))
        box.addWidget(_label(guide_data.DLC_INTRO, "Muted"))
        layout.addWidget(intro)
        for dlc in ("The Signal", "The Writer"):
            frame, box = _card()
            box.addWidget(_label(dlc, "SectionTitle"))
            for trophy in guide_data.DLC_TROPHIES:
                if trophy["dlc"] != dlc:
                    continue
                box.addWidget(self._checkbox(keys.dlc_key(trophy["id"]),
                                             f"<b>{_esc(trophy['en'])}</b>"))
                tip = _label(trophy["tip"], "Muted")
                tip.setContentsMargins(30, 0, 0, 6)
                box.addWidget(tip)
            layout.addWidget(frame)

    # ------------------------------------------------------------- busca geral
    def _global_search(self) -> None:
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        query = _norm(self.global_search.text()).strip()
        if len(query) < 2:
            self.results_box.hide()
            return
        widgets: list[QWidget] = []
        for episode, section, step in keys.collectibles():
            text = (f"{_kind_label(step)} {step['title']} {step['where']} "
                    f"{section['title']} episodio {episode['num']} {episode['title']}")
            if query in _norm(text):
                widgets.append(self._item_block(step, with_photo=False, episode=episode))
            if len(widgets) >= _SEARCH_LIMIT:
                break
        for trophy in guide_data.TROPHIES:
            if len(widgets) >= _SEARCH_LIMIT:
                break
            if query in _norm(f"{trophy['en']} {trophy['tip']} trofeu"):
                frame, box = _card()
                box.addWidget(self._checkbox(keys.trophy_key(trophy["id"]),
                                             f"<b>Troféu: {_esc(trophy['en'])}</b>"))
                box.addWidget(_label(trophy["tip"], "Muted"))
                widgets.append(frame)
        if not widgets:
            widgets.append(_label(
                "Nada encontrado. Tente o tipo e o número (garrafa 57), um lugar ou "
                "o nome do troféu.", "Muted"))
        for widget in widgets:
            self.results_layout.addWidget(widget)
        self.results_box.show()
