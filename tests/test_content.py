from collections import Counter

from platina_alan_wake import guide_data, progress, route


def _steps():
    for episode in route.EPISODES:
        for section in episode["sections"]:
            for step in section["steps"]:
                yield episode, step


def test_trophy_list_matches_the_base_game():
    ids = [t["id"] for t in guide_data.TROPHIES]
    assert len(ids) == 51
    assert len(ids) == len(set(ids))
    assert Counter(t["tier"] for t in guide_data.TROPHIES) == {
        "bronze": 42, "prata": 5, "ouro": 3, "platina": 1,
    }
    assert len(guide_data.DLC_TROPHIES) == 17


def test_every_collectible_appears_once_in_route_order():
    seen: dict[str, list[int]] = {kind: [] for kind in route.KINDS}
    for _episode, step in _steps():
        if step["type"] != "tip":
            seen[step["type"]].append(step["n"])
    for kind, (_name, total) in route.KINDS.items():
        assert seen[kind] == list(range(1, total + 1)), kind
    assert sum(len(v) for v in seen.values()) == 298


def test_episode_checklists_are_cumulative_totals():
    running = Counter()
    for episode in route.EPISODES:
        for section in episode["sections"]:
            for step in section["steps"]:
                if step["type"] != "tip":
                    running[step["type"]] += 1
        assert {k: running[k] for k in episode["checklist"]} == episode["checklist"], episode["id"]


def test_every_collectible_has_a_photo_unless_it_is_automatic():
    for episode, step in _steps():
        if step["type"] == "tip":
            continue
        if step["img"] is None:
            assert step["where"].startswith("Automátic"), (episode["id"], step)
        else:
            assert isinstance(step["img"], int)


def test_tips_point_to_real_trophies_and_keys_are_unique():
    tip_keys = []
    for _episode, step in _steps():
        if step["type"] == "tip":
            tip_keys.append(step["key"])
            assert step["tag"] in ("perdível", "troféu", "dica")
            for trophy_id in step["trophies"]:
                guide_data.trophy_by_id(trophy_id)
    assert len(tip_keys) == len(set(tip_keys))
    for trophy_ids in guide_data.KIND_TROPHIES.values():
        for trophy_id in trophy_ids:
            guide_data.trophy_by_id(trophy_id)


def test_every_missable_trophy_has_a_warning_in_the_route():
    warned = {t for _e, step in _steps() if step["type"] == "tip" and step["tag"] == "perdível"
              for t in step["trophies"]}
    risky = {t["id"] for t in guide_data.TROPHIES if t["cat"] in ("perdível", "desafio")}
    assert risky <= warned


def test_progress_keys_are_unique():
    all_keys = progress.all_keys()
    assert len(all_keys) == len(set(all_keys))


def test_visible_text_has_no_em_dash():
    texts = [guide_data.INTRO, guide_data.DLC_INTRO, guide_data.GAME_SUBTITLE]
    texts += [t["tip"] for t in guide_data.TROPHIES + guide_data.DLC_TROPHIES]
    texts += [p["text"] + p["detail"] + p["title"] for p in guide_data.PLAN]
    texts += guide_data.RULES
    for episode, step in _steps():
        texts.append(step.get("where") or step.get("text"))
    for episode in route.EPISODES:
        texts += [episode["summary"], episode["end"]]
    assert not [t for t in texts if "—" in t]
