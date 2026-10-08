from PySide6.QtWidgets import QApplication

from platina_alan_wake import guide_data, module, page, progress


class _NoNetwork:
    """Carregador de imagens que nunca baixa nada: teste não toca a rede."""

    def __init__(self, _parent=None):
        pass

    def load(self, _url, _on_ready, _on_fail=None):
        return None

    def shutdown(self):
        pass


def _page(monkeypatch, done=()):
    QApplication.instance() or QApplication([])
    saved = []
    monkeypatch.setattr(page, "ImageLoader", _NoNetwork)
    monkeypatch.setattr(page, "load_progress", lambda: set(done))
    monkeypatch.setattr(page, "save_progress", lambda value: saved.append(set(value)))
    monkeypatch.setattr(page, "load_ui", lambda: {})
    monkeypatch.setattr(page, "save_ui", lambda _value: None)
    widget = page.GuidePage()
    widget.resize(1100, 860)
    for index in range(len(guide_data.SECTIONS)):
        widget._ensure_built(index)
    return widget, saved


def test_every_tab_builds_and_marks_sync_across_tabs(monkeypatch):
    widget, saved = _page(monkeypatch)
    # o primeiro episódio abre sozinho; os outros só quando o jogador abre
    key = progress.item_key("thermos", 1)
    assert widget._boxes[key], "a garrafa 1 deveria estar na Rota aberta"
    widget._boxes[key][0].setChecked(True)
    assert key in widget._done
    assert saved and key in saved[-1]
    # abrir a coleção de garrafas cria outra caixa para o mesmo item, já marcada
    before = len(widget._boxes[key])
    for button in widget.findChildren(page.QPushButton):
        if button.text().startswith("Ver os 100"):
            button.setChecked(True)
            break
    assert len(widget._boxes[key]) == before + 1
    assert all(box.isChecked() for box in widget._boxes[key])
    widget.close()


def test_filters_hide_marked_items_and_nightmare_pages(monkeypatch):
    widget, _saved = _page(monkeypatch, done={progress.item_key("thermos", 1)})
    rows = {key: row for row, key, _kind in widget._route_rows}
    # isHidden e não isVisible: a aba Rota não é a que está na tela agora
    assert not rows["thermos_1"].isHidden()
    widget._set_filter("hide_done", True)
    assert rows["thermos_1"].isHidden()
    assert not rows["thermos_2"].isHidden()
    widget._set_filter("show_nm", False)
    assert rows["nm_1"].isHidden()
    widget._set_filter("show_nm", True)
    assert not rows["nm_1"].isHidden()
    widget.close()


def test_search_finds_collectibles_by_type_and_number(monkeypatch):
    widget, _saved = _page(monkeypatch)
    widget.global_search.setText("garrafa de cafe 57/100")
    assert widget.results_layout.count() == 1
    widget.global_search.setText("jukebox")
    assert widget.results_layout.count() >= 1
    widget.close()


def test_module_info_reports_trophies():
    info = module.module_info()
    assert info.status.endswith(f"/{len(guide_data.TROPHIES)} troféus")
    assert "Pesadelo" in module.help_text()


class _AlwaysFails(_NoNetwork):
    def load(self, _url, _on_ready, on_fail=None):
        on_fail("HTTP 403")
        return None


def test_failed_photo_shows_retry_and_the_global_button_retries(monkeypatch):
    monkeypatch.setattr(page, "ImageLoader", _AlwaysFails)
    QApplication.instance() or QApplication([])
    monkeypatch.setattr(page, "load_progress", lambda: set())
    monkeypatch.setattr(page, "save_progress", lambda _v: None)
    monkeypatch.setattr(page, "load_ui", lambda: {})
    monkeypatch.setattr(page, "save_ui", lambda _v: None)
    widget = page.GuidePage()
    widget._ensure_built(1)  # Rota, com o Episódio 1 aberto
    assert widget._failed_photos, "foto que falhou precisa entrar na lista"
    retry_buttons = [b for b in widget.findChildren(page.QPushButton)
                     if b.text() == "Tentar de novo"]
    assert retry_buttons
    assert any("HTTP 403" in label.text() for label in widget.findChildren(page.QLabel))

    got = []

    class _Works(_NoNetwork):
        def load(self, _url, on_ready, _on_fail=None):
            from PySide6.QtGui import QPixmap
            pixmap = QPixmap(8, 8)
            pixmap.fill()
            got.append(1)
            on_ready(pixmap)
            return None

    widget._image_loader = _Works()
    failed_before = len(widget._failed_photos)
    widget._retry_failed_photos()
    assert len(got) == failed_before
    assert not widget._failed_photos
    widget.close()
