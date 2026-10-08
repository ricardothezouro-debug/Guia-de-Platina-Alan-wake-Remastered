"""Adaptador de plugin do Streamer Sidekick (categoria: platina)."""
from dataclasses import dataclass

from . import guide_data

MODULE_ID = guide_data.GUIDE_ID


@dataclass(frozen=True)
class ModuleInfo:
    module_id: str
    title: str
    subtitle: str
    status: str
    accent: str


def module_info():
    from .progress import trophy_keys
    from .storage import load_progress

    done_keys = load_progress()
    trophies = trophy_keys()
    done = sum(1 for key in trophies if key in done_keys)
    data = dict(
        module_id=guide_data.GUIDE_ID,
        title=guide_data.GAME_NAME,
        subtitle=guide_data.GAME_SUBTITLE,
        status=f"{done}/{len(trophies)} troféus",
        accent=guide_data.ACCENT,
    )
    try:
        from streamer_sidekick.core.modules import ModuleInfo as SidekickModuleInfo

        return SidekickModuleInfo(**data)
    except Exception:
        return ModuleInfo(**data)


def help_text() -> str:
    from .paths import guide_dir_label

    return (
        "Guia de platina de Alan Wake Remastered (PS4/PS5) em PT-BR.\n\n"
        "A platina custa duas zeradas: a primeira no Normal (ou no Fácil) "
        "seguindo a aba Rota para pegar os coletáveis e resolver os perdíveis, "
        "e a segunda no Pesadelo, que só destrava depois de terminar o jogo uma "
        "vez e é onde aparecem as 15 páginas exclusivas. Zerar no Pesadelo "
        "libera os troféus das três dificuldades.\n\n"
        "A Rota lista cada coletável na ordem em que aparece, com o marco que "
        "localiza ele e a foto do lugar. Marcar um item marca ele em todas as "
        "abas. O que escapar dá para buscar depois pelo Seleção de Episódio: o "
        "jogo guarda o que você já coletou.\n\n"
        "As expansões têm troféus num grupo separado, que não contam para a "
        "platina. A aba Expansões resume o que cada um pede.\n\n"
        f"O progresso fica em {guide_dir_label()}, fora da pasta do plugin, "
        "então sobrevive a atualizações."
    )


def build_page(config=None):
    from .page import GuidePage

    return GuidePage()
