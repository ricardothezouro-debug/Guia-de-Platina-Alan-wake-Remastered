"""Chaves de progresso do guia.

Toda caixa de marcar tem uma chave estável, e o mesmo item usa a mesma chave
em qualquer aba: marcar a garrafa 57 na Rota marca ela na aba Coletáveis e no
resultado da busca. Renomear uma chave apaga o que o jogador marcou, então
nada aqui muda de formato entre versões.
"""
from __future__ import annotations

from . import guide_data


def item_key(kind: str, n: int) -> str:
    return f"{kind}_{n}"


def tip_key(key: str) -> str:
    return f"tip_{key}"


def plan_key(plan_id: str) -> str:
    return f"plan_{plan_id}"


def trophy_key(trophy_id: str) -> str:
    return f"trophy_{trophy_id}"


def dlc_key(trophy_id: str) -> str:
    return f"dlc_{trophy_id}"


def collectibles() -> list[tuple[dict, dict, dict]]:
    """[(episódio, trecho, item)] de todos os coletáveis, na ordem da Rota."""
    out = []
    for episode in guide_data.EPISODES:
        for section in episode["sections"]:
            for step in section["steps"]:
                if step["type"] != "tip":
                    out.append((episode, section, step))
    return out


def collectible_keys(kind: str | None = None) -> list[str]:
    return [item_key(step["type"], step["n"]) for _e, _s, step in collectibles()
            if kind is None or step["type"] == kind]


def episode_keys(episode: dict) -> list[str]:
    """Tudo que é marcável dentro de um episódio: coletáveis e perdíveis."""
    keys = []
    for section in episode["sections"]:
        for step in section["steps"]:
            if step["type"] == "tip":
                if step["tag"] == "perdível":
                    keys.append(tip_key(step["key"]))
            else:
                keys.append(item_key(step["type"], step["n"]))
    return keys


def trophy_keys() -> list[str]:
    return [trophy_key(t["id"]) for t in guide_data.TROPHIES]


def all_keys() -> list[str]:
    """O que entra na barra de progresso: rota, plano e troféus do jogo base.

    Os troféus das expansões ficam de fora de propósito: não contam para a
    platina, e incluí-los faria a barra nunca chegar a 100% para quem só quer
    a platina.
    """
    keys = [plan_key(step["id"]) for step in guide_data.PLAN]
    for episode in guide_data.EPISODES:
        keys += episode_keys(episode)
    return keys + trophy_keys()


def normalize_imported(raw) -> set[str]:
    """Aceita a lista que este guia exporta e um dicionário `{chave: bool}`."""
    if isinstance(raw, dict):
        raw = [key for key, value in raw.items() if value]
    return {str(key) for key in raw}
