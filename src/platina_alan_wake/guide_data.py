"""Dados do guia de platina de Alan Wake Remastered (PS4/PS5, PT-BR).

A rota com os coletáveis está em `route.py`. Aqui ficam o plano, os troféus e
os textos do topo. Os dois são os únicos arquivos específicos do jogo.
"""
from .route import EPISODES, IMG, KINDS

GUIDE_ID = "alan-wake-remastered"

GAME_NAME = "Alan Wake Remastered: Platina"
GAME_SUBTITLE = (
    "Guia PT-BR: duas zeradas, os 298 coletáveis do jogo base na ordem e com "
    "foto, os perdíveis no ponto exato e os 51 troféus."
)
ACCENT = "#F2C14E"  # a luz da lanterna

INTRO = (
    "São 51 troféus no jogo base e DUAS zeradas. A segunda tem que ser no "
    "Pesadelo, que só destrava depois de terminar o jogo uma vez, e é nela que "
    "aparecem as 15 páginas exclusivas dessa dificuldade.\n\n"
    "O jogo é linear e o save é um só, sobrescrito o tempo todo: passou de um "
    "trecho, não volta. Por isso a aba Rota lista cada coletável na ordem em que "
    "ele aparece, com o marco que localiza ele e a foto do lugar. Siga de cima "
    "para baixo e marque conforme pega.\n\n"
    "O que escapar não estraga a platina: todo coletável conta na hora em que "
    "você pega, e o Seleção de Episódio deixa refazer qualquer trecho depois sem "
    "perder o que já tem. As expansões (The Signal e The Writer) têm troféus "
    "num grupo separado e NÃO contam para a platina."
)

HERO_IMAGE = IMG.format(322)

HERO_STATS = [
    {"value": "51", "label": "troféus"},
    {"value": "2", "label": "zeradas"},
    {"value": "298", "label": "coletáveis com foto"},
    {"value": "6", "label": "perdíveis, todos refazíveis"},
]

SECTIONS = [
    {"key": "plan", "num": "01", "nav": "Plano"},
    {"key": "route", "num": "02", "nav": "Rota"},
    {"key": "collect", "num": "03", "nav": "Coletáveis"},
    {"key": "trophies", "num": "04", "nav": "Troféus"},
    {"key": "dlc", "num": "05", "nav": "Expansões"},
]

# ── O plano ────────────────────────────────────────────────────────────────
# Cada etapa tem um id estável, porque vira caixa de marcar.
PLAN = [
    {
        "id": "run1",
        "title": "Zerada 1: Normal, seguindo a Rota inteira",
        "text": (
            "Comece um jogo novo no Normal e siga a aba Rota episódio por episódio. "
            "É aqui que você pega as 91 páginas normais, as 100 garrafas, os 30 "
            "baús, as 12 pirâmides, os 11 rádios, as 14 TVs e as 25 placas, e "
            "resolve os perdíveis no ponto em que aparecem. A maior parte dos "
            "troféus de combate sai sozinha no caminho."
        ),
        "detail": (
            "Por que Normal: o Pesadelo da segunda zerada fica menos brutal e o "
            "Normal já é a dificuldade de Hardboiled Writer. Se preferir explorar "
            "com calma, o Fácil serve igual: zerar no Pesadelo depois libera os "
            "troféus das três dificuldades de uma vez."
        ),
    },
    {
        "id": "cleanup",
        "title": "Limpeza: Seleção de Episódio no Fácil",
        "text": (
            "Três troféus são desafios de trecho e ficam muito mais fáceis sem "
            "parar para coletar: Meet the Deadline (Episódio 3, 30 minutos), An "
            "Idyllic Small Town (Episódio 5, sem morrer) e Gunless Wonder (Episódio "
            "6, sem atirar). Abra o trecho pelo Seleção de Episódio, escolha o "
            "Fácil e só corra. Aproveite para buscar qualquer coletável que tenha "
            "escapado: ele conta na hora."
        ),
        "detail": (
            "Confira as Estatísticas do menu de pausa: os totais de cada episódio "
            "estão no fim de cada card da Rota. Se um número não bate, o card "
            "mostra o que falta naquele trecho."
        ),
    },
    {
        "id": "run2",
        "title": "Zerada 2: Pesadelo, atrás das 15 páginas",
        "text": (
            "Comece um jogo novo no Pesadelo. Agora só importam as 15 páginas "
            "exclusivas (marcadas como “Página do Pesadelo” na Rota) e terminar o "
            "jogo. Os créditos liberam Alan, Wake Up e, de quebra, Hardboiled "
            "Writer e Departure. A última página do Pesadelo libera Collector's "
            "Edition."
        ),
        "detail": (
            "No Pesadelo os Taken aguentam bem mais. Guarde pistola sinalizadora e "
            "granadas de luz para os grupos e os pesados, foque a lanterna (L2) "
            "antes de atirar e não brigue com o que dá para evitar: correr até o "
            "próximo refúgio de luz faz os inimigos sumirem."
        ),
    },
    {
        "id": "dlc",
        "title": "Opcional: as expansões",
        "text": (
            "The Signal e The Writer abrem pelo Seleção de Episódio e têm 17 "
            "troféus num grupo à parte. Eles não contam para a platina. A aba "
            "Expansões resume o que cada um pede, para quem quiser o 100%."
        ),
        "detail": "",
    },
]

# Regras que valem para o jogo inteiro.
RULES = [
    "Coletável conta na hora em que você pega, mesmo se morrer logo depois.",
    "O Seleção de Episódio guarda tudo o que você já coletou: dá para refazer um "
    "trecho só para buscar o que faltou.",
    "Baús escondidos são indicados por marcas amarelas pintadas que só aparecem "
    "com a luz da lanterna. Viu uma seta amarela, siga.",
    "As TVs que ligam sozinhas contam só de passar perto. As outras, ligue e "
    "assista.",
    "Pirâmide de latas conta derrubando de qualquer jeito. No Episódio 6 derrube "
    "na mão (Gunless Wonder).",
    "Refúgio de luz (poste aceso) cura e faz os inimigos sumirem. Correr até ele "
    "quase sempre é melhor que lutar.",
    "Troque de arma por conta própria: o jogo equipa a pistola sinalizadora ao "
    "pegar, e um tiro dela gasto num Taken sozinho faz falta depois.",
]

# ── Troféus ────────────────────────────────────────────────────────────────
# categoria: história, perdível, desafio, combate, coletável, dificuldade
TROPHIES = [
    {"id": "platinum", "en": "Platinum Trophy", "tier": "platina", "cat": "platina",
     "tip": "Todos os outros 50 troféus do jogo base. Os das expansões não contam."},
    {"id": "follow_the_light", "en": "Follow the Light", "tier": "bronze", "cat": "história",
     "tip": "Matar o caroneiro no sonho do Episódio 1."},
    {"id": "nordic_walking", "en": "Nordic Walking", "tier": "bronze", "cat": "história",
     "tip": "Vencer o Carl Stucky na madeireira, no fim do Episódio 1."},
    {"id": "bright_falls_finest", "en": "Bright Falls' Finest", "tier": "bronze", "cat": "história",
     "tip": "Terminar o Episódio 1 (o telefonema no posto)."},
    {"id": "boob_tube", "en": "Boob Tube", "tier": "bronze", "cat": "perdível",
     "tip": ("Episódio 4, na fuga da clínica: depois de queimar os ursos de madeira, "
             "ligar a TV da sala do fim do corredor (Night Springs “The Doomed "
             "Samaritan”). Não é uma das 14 TVs da coleção.")},
    {"id": "under_a_thin_layer_of_skin", "en": "Under a Thin Layer of Skin", "tier": "bronze",
     "cat": "história", "tip": "Matar o Rusty no Episódio 2."},
    {"id": "park_ranger", "en": "Park Ranger", "tier": "bronze", "cat": "história",
     "tip": "Terminar o Episódio 2."},
    {"id": "heavy_metal", "en": "Heavy Metal", "tier": "bronze", "cat": "perdível",
     "tip": ("Episódio 3, pátio ferroviário: DESTRUIR a escavadeira possuída com a "
             "lanterna focada (umas cinco baterias), em vez de fugir pelo portão.")},
    {"id": "iron_horse", "en": "Iron Horse", "tier": "bronze", "cat": "perdível",
     "tip": ("Episódio 3, vilarejo minerador: destruir a caldeira e depois a cabine "
             "da locomotiva enferrujada com a lanterna focada.")},
    {"id": "wheels_within_wheels", "en": "Wheels Within Wheels", "tier": "bronze",
     "cat": "história", "tip": "Terminar o Episódio 3."},
    {"id": "medical_opinions", "en": "Medical Opinions", "tier": "bronze", "cat": "perdível",
     "tip": ("Episódio 4, a caminho do escritório do Hartman: tocar as TRÊS fitas do "
             "gravador na sala em frente à foto (aperte play três vezes).")},
    {"id": "child_of_the_elder_god", "en": "Child of the Elder God", "tier": "bronze",
     "cat": "perdível",
     "tip": ("Episódio 4, defesa do palco na fazenda: terminar sem a vida entrar na "
             "faixa crítica. Se entrar, recarregue o checkpoint na hora.")},
    {"id": "perchance_to_dream", "en": "Perchance to Dream", "tier": "bronze", "cat": "história",
     "tip": "Terminar o Episódio 4."},
    {"id": "drink_em_both_up", "en": "Drink 'Em Both Up", "tier": "bronze", "cat": "perdível",
     "tip": ("Tocar a jukebox da lanchonete Oh Deer DUAS vezes: no Episódio 1 (a "
             "faixa “Coconut” que o motoqueiro pede, com um tapa quando o braço "
             "trava) e de novo no Episódio 5.")},
    {"id": "gatekeeper", "en": "Gatekeeper", "tier": "bronze", "cat": "história",
     "tip": ("Episódio 5: fechar as comportas e cortar a energia do pátio dos "
             "transformadores. Ordem dos interruptores: 1, 2, 3 e 1 de novo.")},
    {"id": "the_lady_of_the_light", "en": "The Lady of the Light", "tier": "bronze",
     "cat": "história", "tip": "Terminar o Episódio 5."},
    {"id": "tornado_wrangler", "en": "Tornado Wrangler", "tier": "bronze", "cat": "história",
     "tip": "Episódio 6: atirar com a pistola sinalizadora no centro do tornado até ele sumir."},
    {"id": "departure", "en": "Departure", "tier": "bronze", "cat": "dificuldade",
     "tip": "Zerar no Fácil. Também sai zerando no Normal ou no Pesadelo."},
    {"id": "hardboiled_writer", "en": "Hardboiled Writer", "tier": "bronze", "cat": "dificuldade",
     "tip": "Zerar no Normal. Também sai zerando no Pesadelo."},
    {"id": "alan_wake_up", "en": "Alan, Wake Up", "tier": "bronze", "cat": "dificuldade",
     "tip": "Zerar no Pesadelo. A dificuldade só aparece depois de terminar o jogo uma vez."},
    {"id": "if_it_flies_it_burns", "en": "If It Flies, It Burns", "tier": "bronze", "cat": "combate",
     "tip": ("Matar 1.000 pássaros, somando as duas zeradas. O melhor ponto é a "
             "defesa da varanda no fim do Episódio 2: uns 250 de uma vez, e dá para "
             "recarregar o checkpoint e repetir.")},
    {"id": "theyre_heeeeeere", "en": "They're Heeeeeere!", "tier": "bronze", "cat": "combate",
     "tip": ("Destruir 20 objetos possuídos (portões, canos, carretéis, carros) com "
             "a luz. Começam no Episódio 3: destrua em vez de só desviar.")},
    {"id": "the_six_gun_scribe", "en": "The Six-Gun Scribe", "tier": "bronze", "cat": "combate",
     "tip": "100 Taken com o revólver. Sai jogando: é a arma que você mais usa."},
    {"id": "taken_season", "en": "Taken Season", "tier": "bronze", "cat": "combate",
     "tip": ("50 Taken com o rifle de caça. Pegue o rifle sempre que achar (ele "
             "ocupa o lugar da espingarda): os Episódios 4 e 5 têm bastante munição.")},
    {"id": "its_not_just_a_typewriter_brand", "en": "It's Not Just a Typewriter Brand",
     "tier": "bronze", "cat": "combate",
     "tip": "50 Taken com espingarda (a comum ou a de bomba)."},
    {"id": "what_light_through_yonder_window", "en": "What Light Through Yonder Window",
     "tier": "bronze", "cat": "combate",
     "tip": "50 Taken com a pistola sinalizadora. Conta por inimigo, então grupos rendem mais."},
    {"id": "thunder_and_lightning", "en": "Thunder and Lightning", "tier": "bronze", "cat": "combate",
     "tip": "50 Taken com granadas de luz. Aparecem do Episódio 3 em diante."},
    {"id": "collateral_carnage", "en": "Collateral Carnage", "tier": "bronze", "cat": "combate",
     "tip": ("20 Taken mortos de forma indireta: explosão de botijão de gás, "
             "eletricidade, água. Atire nos botijões vermelhos quando houver Taken "
             "perto.")},
    {"id": "come_one_come_all", "en": "Come One, Come All", "tier": "bronze", "cat": "combate",
     "tip": ("4 Taken com um único tiro da pistola sinalizadora. Espere o grupo "
             "chegar junto: a defesa do mirante (Episódio 2) e a do heliponto "
             "(Episódio 5) têm muitos.")},
    {"id": "sound_and_fury", "en": "Sound and Fury", "tier": "bronze", "cat": "combate",
     "tip": ("4 Taken com uma granada de luz. Episódio 3, logo depois de ganhar as "
             "primeiras granadas na viatura.")},
    {"id": "two_for_the_price_of_one", "en": "Two For the Price of One", "tier": "bronze",
     "cat": "combate",
     "tip": "2 Taken com um tiro de espingarda: deixe dois chegarem alinhados e atire de perto."},
    {"id": "back_back_i_say", "en": "Back! Back, I Say!", "tier": "bronze", "cat": "combate",
     "tip": ("Com a vida baixa, acender um sinalizador de mão (R1) com Taken por "
             "perto. A chance garantida é seguindo o sequestrador, no Episódio 2.")},
    {"id": "float_like_a_butterfly", "en": "Float Like a Butterfly", "tier": "bronze",
     "cat": "combate",
     "tip": "Uma esquiva em câmera lenta (L1 + direção na hora do golpe). Não vale no tutorial."},
    {"id": "missed_by_a_mile", "en": "Missed by a Mile", "tier": "bronze", "cat": "combate",
     "tip": "20 esquivas em câmera lenta. Sai jogando."},
    {"id": "energized", "en": "Energized!", "tier": "bronze", "cat": "combate",
     "tip": "Trocar a bateria 100 vezes (△). Use o foco da lanterna (L2) sem medo."},
    {"id": "let_there_be_light", "en": "Let There Be Light", "tier": "bronze", "cat": "história",
     "tip": "Ligar o gerador do galpão da cabana, no Episódio 1."},
    {"id": "carny", "en": "Carny", "tier": "bronze", "cat": "coletável",
     "tip": "Derrubar 5 pirâmides de latas. Pela Rota, sai no Episódio 3."},
    {"id": "meet_the_deadline", "en": "Meet the Deadline", "tier": "bronze", "cat": "desafio",
     "tip": ("Episódio 3: do museu da mina até avistar o mirante do Mirror Peak em "
             "menos de 30 minutos. Faça pelo Seleção de Episódio, no Fácil, sem "
             "coletar nada.")},
    {"id": "an_idyllic_small_town", "en": "An Idyllic Small Town", "tier": "bronze",
     "cat": "desafio",
     "tip": ("Episódio 5: da cela da delegacia até entrar no helicóptero sem morrer "
             "e sem recarregar checkpoint. No Fácil, pelo Seleção de Episódio, é "
             "tranquilo.")},
    {"id": "gunless_wonder", "en": "Gunless Wonder", "tier": "bronze", "cat": "desafio",
     "tip": ("Episódio 6: do começo do trecho na estrada até o tornado sem disparar "
             "arma. Granada de luz, sinalizador de mão e o carro podem.")},
    {"id": "right_of_way", "en": "Right of Way", "tier": "bronze", "cat": "combate",
     "tip": ("Atropelar 15 Taken: farol alto (X) tira a escuridão, depois é só "
             "passar por cima. Comece no primeiro carro, no fim do Episódio 2.")},
    {"id": "finders_keepers", "en": "Finders Keepers", "tier": "bronze", "cat": "coletável",
     "tip": "5 baús escondidos. Pela Rota, sai no Episódio 2."},
    {"id": "every_nook_and_cranny", "en": "Every Nook and Cranny", "tier": "bronze",
     "cat": "coletável", "tip": "Os 30 baús. O último fica no fim do Episódio 6."},
    {"id": "paging_mr_wake", "en": "Paging Mr. Wake", "tier": "prata", "cat": "coletável",
     "tip": "25 páginas do manuscrito. Pela Rota, sai no Episódio 2."},
    {"id": "picking_up_after_yourself", "en": "Picking Up After Yourself", "tier": "prata",
     "cat": "coletável",
     "tip": "As 91 páginas que existem no Fácil e no Normal. A última fica no fim do Episódio 6."},
    {"id": "collectors_edition", "en": "Collector's Edition", "tier": "prata", "cat": "coletável",
     "tip": "As 106 páginas: as 91 normais e as 15 que só aparecem no Pesadelo."},
    {"id": "damn_good_cup_of_coffee", "en": "Damn Good Cup of Coffee", "tier": "prata",
     "cat": "coletável", "tip": "25 garrafas de café. Pela Rota, sai no Episódio 2."},
    {"id": "hypercaffeinated", "en": "Hypercaffeinated", "tier": "prata", "cat": "coletável",
     "tip": "As 100 garrafas. A última é uma palavra no Lugar Escuro, no fim do jogo."},
    {"id": "kbf_fm", "en": "KBF-FM", "tier": "ouro", "cat": "coletável",
     "tip": "Os 11 programas de rádio: ligue cada rádio da Rota. O último fica no Episódio 4."},
    {"id": "couch_potato", "en": "Couch Potato", "tier": "ouro", "cat": "coletável",
     "tip": "Os 14 programas de TV. As que ligam sozinhas contam; o último é no começo do Episódio 6."},
    {"id": "bright_falls_aficionado", "en": "Bright Falls Aficionado", "tier": "ouro",
     "cat": "coletável", "tip": "Examinar as 25 placas. A última fica no ferro-velho do Episódio 6."},
]

# Troféus que a Rota liga a cada tipo de coletável (para a aba Coletáveis).
KIND_TROPHIES = {
    "page": ["paging_mr_wake", "picking_up_after_yourself", "collectors_edition"],
    "nm": ["collectors_edition"],
    "thermos": ["damn_good_cup_of_coffee", "hypercaffeinated"],
    "chest": ["finders_keepers", "every_nook_and_cranny"],
    "can": ["carny"],
    "radio": ["kbf_fm"],
    "tv": ["couch_potato"],
    "sign": ["bright_falls_aficionado"],
}

# ── Expansões (fora da platina) ────────────────────────────────────────────
DLC_INTRO = (
    "As duas expansões vêm junto no Remastered e abrem pelo Seleção de "
    "Episódio. Os troféus delas ficam em grupos separados da lista e não contam "
    "para a platina. Dois deles pedem terminar sem morrer, então jogue as duas "
    "no Fácil."
)

DLC_TROPHIES = [
    {"id": "a_friend_in_need", "en": "A Friend in Need", "dlc": "The Signal",
     "tip": ("No porão da igreja, depois de pegar a página que aparece, ilumine a "
             "palavra “friend” para o Barry surgir.")},
    {"id": "a_friend_indeed", "en": "A Friend Indeed", "dlc": "The Signal",
     "tip": "Terminar The Signal."},
    {"id": "fast_and_furious", "en": "Fast and Furious", "dlc": "The Signal",
     "tip": ("Depois do apartamento com o Zane, limpar o caminho até o cais (o barco "
             "que cai do céu) em menos de 1 minuto e 30 segundos. Guarde munição da "
             "pistola sinalizadora para esse trecho.")},
    {"id": "words_will_never_harm_you", "en": "Words Will Never Harm You", "dlc": "The Signal",
     "tip": "No porão da igreja, ilumine as 100 portas de fornalha com a palavra “blast”."},
    {"id": "run_on_sentence", "en": "Run-On Sentence", "dlc": "The Signal",
     "tip": "Terminar The Signal sem morrer e sem recarregar checkpoint."},
    {"id": "license_revoked", "en": "License Revoked", "dlc": "The Signal",
     "tip": "Atravessar a serraria inteira sem entrar em nenhum veículo."},
    {"id": "tick_tock", "en": "Tick Tock", "dlc": "The Signal",
     "tip": "Achar os 10 despertadores escondidos."},
    {"id": "cardboard_companions", "en": "Cardboard Companions", "dlc": "The Signal",
     "tip": "Achar os 6 recortes de papelão."},
    {"id": "ding", "en": "Ding!", "dlc": "The Writer",
     "tip": "Terminar o trecho da roda-gigante e pegar o elevador no fim."},
    {"id": "kill_your_darlings", "en": "Kill Your Darlings", "dlc": "The Writer",
     "tip": "Vencer o Hartman, os irmãos Anderson e o Barry antes da cabana. Automático."},
    {"id": "go_gentle_into_that_good_light", "en": "Go Gentle Into That Good Light",
     "dlc": "The Writer",
     "tip": "Quando o Zane diz que não pode seguir com você, não atire até chegar ao farol."},
    {"id": "no_punctuation", "en": "No Punctuation", "dlc": "The Writer",
     "tip": "Terminar The Writer sem morrer e sem recarregar checkpoint."},
    {"id": "iron_will", "en": "Iron Will", "dlc": "The Writer",
     "tip": "Na luta final contra o Hartman, os Anderson e o Barry, não deixe a vida ficar crítica."},
    {"id": "whirlwind", "en": "Whirlwind", "dlc": "The Writer",
     "tip": ("No tornado depois da cabana giratória, ilumine as palavras “bridge” e "
             "“path” e passe em menos de 60 segundos.")},
    {"id": "licensed_properties", "en": "Licensed Properties", "dlc": "The Writer",
     "tip": "Achar os 10 videogames do Night Springs."},
    {"id": "creative_space", "en": "Creative Space", "dlc": "The Writer",
     "tip": ("No avião caído a caminho do farol, entre pela passagem estreita perto "
             "de uma asa e vá até a máquina de escrever gigante.")},
    {"id": "heartbreaker", "en": "Heartbreaker", "dlc": "The Writer",
     "tip": ("Ouça a conversa do Hartman com o Alan maluco e toque a fita que "
             "aparece até o fim. O troféu sai ao deixar o escritório.")},
]

SOURCES = [
    ("Fotos e ordem dos coletáveis: guia de PS5 de Christopher Williams na GameFAQs",
     "https://gamefaqs.gamespot.com/ps5/330504-alan-wake-remastered/faqs/81217"),
    ("Lista de troféus, tiers e grupos das expansões: Exophase",
     "https://www.exophase.com/game/alan-wake-remastered-psn/trophies/"),
    ("Dificuldades do Remastered e troféus que acumulam: Alan Wake Wiki",
     "https://alanwake.fandom.com/wiki/Hardboiled_Writer"),
    ("Contagem de pássaros (1.000): Alan Wake Wiki",
     "https://alanwake.fandom.com/wiki/If_It_Flies,_It_Burns"),
]

FOOTER = "Alan Wake Remastered (PS4/PS5): Platina PT-BR • guia não oficial"


def trophy_by_id(trophy_id: str) -> dict:
    for trophy in TROPHIES + DLC_TROPHIES:
        if trophy["id"] == trophy_id:
            return trophy
    raise KeyError(trophy_id)


__all__ = [
    "EPISODES", "IMG", "KINDS", "GUIDE_ID", "GAME_NAME", "GAME_SUBTITLE", "ACCENT",
    "INTRO", "HERO_IMAGE", "HERO_STATS", "SECTIONS", "PLAN", "RULES", "TROPHIES",
    "KIND_TROPHIES", "DLC_INTRO", "DLC_TROPHIES", "SOURCES", "FOOTER", "trophy_by_id",
]
