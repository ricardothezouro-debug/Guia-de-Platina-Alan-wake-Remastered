"""A rota: os seis episódios na ordem, com cada coletável no ponto exato.

Alan Wake é linear e o save é um só, sobrescrito o tempo todo: passou de um
trecho, não dá para voltar (só pelo Seleção de Episódio, refazendo o trecho
inteiro). Por isso a rota lista os coletáveis na ordem em que aparecem, com o
marco que localiza cada um ("depois da cutscene X, antes de descer Y").

Cada coletável tem uma chave estável (`tipo_número`), a mesma usada na aba
Coletáveis: marcar num lugar marca no outro. O número é a ordem de coleta
seguindo esta rota, e é o mesmo que o jogo mostra nas Estatísticas quando
nada fica para trás.

Fotos: capturas do guia de PS5 de Christopher Williams na GameFAQs (créditos
na aba Plano). O texto é nosso.
"""
from __future__ import annotations

IMG = "https://gamefaqs.gamespot.com/a/faqs/17/81217-{}.jpg"

# tipo -> (nome no singular, total no jogo)
KINDS = {
    "page": ("Página do manuscrito", 91),
    "nm": ("Página do Pesadelo", 15),
    "thermos": ("Garrafa de café", 100),
    "chest": ("Baú escondido", 30),
    "can": ("Pirâmide de latas", 12),
    "radio": ("Programa de rádio", 11),
    "tv": ("Programa de TV", 14),
    "sign": ("Placa", 25),
}


def c(kind: str, n: int, where: str, img: int | None = None, title: str = "") -> dict:
    """Um coletável. `title` é o nome que aparece na tela (em inglês)."""
    return {"type": kind, "n": n, "where": where, "img": img, "title": title}


def tip(key: str, text: str, *, tag: str = "dica", trophies: tuple[str, ...] = (),
        img: int | None = None) -> dict:
    """Um aviso no meio da rota. `tag` é "perdível", "troféu" ou "dica"."""
    return {"type": "tip", "key": key, "text": text, "tag": tag,
            "trophies": list(trophies), "img": img}


def sec(title: str, steps: list[dict]) -> dict:
    return {"title": title, "steps": steps}


EPISODES = [
    {
        "id": "ep1",
        "num": 1,
        "title": "Nightmare",
        "pt": "Pesadelo",
        "summary": (
            "Tutorial no sonho, a chegada a Bright Falls e a primeira noite na "
            "madeireira até o posto do Stucky. Tem a primeira metade de um "
            "troféu perdível (a jukebox)."
        ),
        "sections": [
            sec("O sonho: a estrada até o farol", [
                c("thermos", 1,
                  "Assim que ganhar o controle, NÃO siga para o farol. Vá até a ponte "
                  "interditada (placa “Bridge Out”), passe pelos bloqueios e pegue a "
                  "garrafa no asfalto. Depois volte e desça pelo caminho do farol.", 1),
                tip("ep1_dodge",
                    "A esquiva em câmera lenta contra o caroneiro NÃO conta para Float "
                    "Like a Butterfly aqui no tutorial. Ela sai sozinha mais tarde.",
                    trophies=("float_like_a_butterfly",)),
                c("can", 1,
                  "Depois de matar o caroneiro (troféu Follow the Light), revire a "
                  "caçamba de lixo para pegar munição e olhe para a esquerda: a "
                  "pirâmide está ali. Atire nela.", 4),
                c("thermos", 2,
                  "Depois de descer e pegar a pistola sinalizadora na caixa de "
                  "emergência no fim da trilha, procure um abrigo de concreto ao lado "
                  "do caminho e desça nele.", 7),
                c("thermos", 3,
                  "Depois de atravessar correndo a ponte que desmorona com o tornado, "
                  "a garrafa está num banco do outro lado, antes do farol.", 9),
            ]),
            sec("Bright Falls: balsa, lanchonete e a cabana", [
                tip("ep1_jukebox",
                    "1ª metade de Drink 'Em Both Up. Na lanchonete Oh Deer, "
                    "fale com os dois velhos motoqueiros na mesa: um deles pede a faixa "
                    "6, “Coconut”. Use a jukebox ao lado e, quando o braço travar, "
                    "aperte X para dar um tapa nela. A outra metade é no Episódio 5.",
                    tag="perdível", trophies=("drink_em_both_up",), img=10),
                c("thermos", 4,
                  "Ainda na lanchonete, no balcão com as bandejas e os guardanapos.", 12),
                c("thermos", 5,
                  "Ao chegar na ponte para a cabana (Diver's Isle), dê meia-volta e suba "
                  "o caminho inteiro até onde a Alice estacionou: a garrafa está no "
                  "mirante.", 13),
                tip("ep1_generator",
                    "O gerador no galpão depois da cabana libera Let There Be Light: "
                    "aperte X três vezes com a manivela na faixa verde.",
                    tag="troféu", trophies=("let_there_be_light",)),
                c("radio", 1,
                  "Depois do gerador e da cutscene, entre na cabana e saia pela porta "
                  "dos fundos: o rádio está na varanda.", 16),
                c("thermos", 6,
                  "De volta à cabana, no balcão da cozinha (antes de subir a escada "
                  "para o escritório).", 17),
                tip("ep1_birds",
                    "Os pássaros na ponte começam a conta de If It Flies, It Burns "
                    "(1.000 no total). Não precisa farmar agora: o fim do Episódio 2 "
                    "tem uns 250 de uma vez.",
                    trophies=("if_it_flies_it_burns",)),
            ]),
            sec("Acordando no pesadelo: a madeireira", [
                c("page", 1,
                  "Automática: vem na cutscene ao descer a ladeira depois do carro "
                  "batido.", None, "The Title Page of the Manuscript"),
                c("page", 2,
                  "Automática: vem junto com a anterior, na mesma cutscene.", None,
                  "Wake Attacked by a Shadowy Murderer"),
                c("nm", 1,
                  "Só no Pesadelo. Antes de usar a árvore caída para pular a cerca, "
                  "olhe em OUTRA árvore caída logo ao lado.", 394, "Rose is a Fan"),
                c("thermos", 7,
                  "Já no pátio da madeireira (lumber yard), depois da cutscene com o "
                  "Carl Stucky: passe pela empilhadeira. A garrafa está perto da "
                  "caminhonete.", 20),
                c("page", 3,
                  "Dali, vire à direita: no chão, ao lado de uma pilha de toras, antes "
                  "de correr para a cabana.", 21, "Wake Fights a Taken with Light"),
                c("chest", 1,
                  "Depois da cabana que cai no barranco: passe o portão, mate os dois "
                  "Taken e contorne o prédio até os fundos. As marcas amarelas que "
                  "acendem com a lanterna levam ao baú (pistola sinalizadora).", 23),
                c("page", 4,
                  "Chute o gerador para desligar a cerca elétrica, pule-a e mate o "
                  "Taken perto da escavadeira. Desvie à ESQUERDA: a página está "
                  "pregada na parede de uma cabana. Depois volte à escavadeira.", 24,
                  "Rose Daydreams About Wake"),
                c("thermos", 8,
                  "Ao atravessar o rio pelo primeiro tronco, vá primeiro à esquerda: "
                  "a garrafa está numa pedra.", 25),
                c("page", 5,
                  "Volte ao tronco e siga no outro sentido. Ignore os troncos à "
                  "esquerda (o caminho certo, você volta neles) e continue cruzando "
                  "mais troncos: a página está numa laje de concreto.", 26,
                  "Barry's Arrival"),
                c("nm", 2,
                  "Só no Pesadelo. Depois de atravessar pelos troncos que você "
                  "ignorou, nas pedras perto da munição e das pilhas de lítio.", 395,
                  "The Dark Presence Wakes Up"),
                c("chest", 2,
                  "Depois dos dois Taken que jogam machados, suba até a grande pilha "
                  "de madeira. Vá à esquerda até a garra de toras, vire e suba a "
                  "escada até o topo da outra pilha: o baú está num prédio em "
                  "ruínas.", 28),
                c("thermos", 9,
                  "Volte para onde entrou no pátio e siga até a escada caída que "
                  "bloqueia o caminho. Pegue o armário de suprimentos e siga reto: a "
                  "garrafa está numa pedra, à esquerda de uma pilha de toras.", 30),
                c("page", 6,
                  "Mate os três Taken perto da luz verde piscando e ligue o gerador. "
                  "Antes de voltar, entre na cabana ao lado: a página está na mesa (a "
                  "espingarda está na prateleira).", 31, "Wake Attacked By Birds"),
                c("can", 2,
                  "Use a chave no poste para baixar as toras e formar a ponte. Suba "
                  "pela escada da pilha da esquerda e atravesse. Do outro lado, vá à "
                  "direita até a mesa com cadeiras.", 33),
                c("radio", 2,
                  "Entre na cabana à esquerda dessa mesa: o rádio está lá dentro.", 34),
                c("chest", 3,
                  "Saia e dê a volta pelos fundos da cabana: marcas amarelas num "
                  "tronco apontam o baú num prédio em ruínas.", 35),
                c("page", 7,
                  "Volte um pouco e suba a ladeira: no chão, junto de dois postes.", 36,
                  "Wake Finds Pages"),
                c("thermos", 10,
                  "Um pouco mais à frente, numa pedra ao lado do caminho.", 37),
                c("thermos", 11,
                  "Depois de ligar o próximo gerador começa o trecho com inimigos que "
                  "renascem. Saia da luz desviando levemente à direita: a garrafa "
                  "está atrás de uma pedra pontuda.", 41),
                c("page", 8,
                  "Siga na direção do objetivo (há uma placa apontando um refúgio). A "
                  "página está no chão no meio do caminho.", 40, "TV in the Gas Station"),
                c("chest", 4,
                  "Do refúgio de luz, desça: marcas amarelas apontam o baú.", 42),
                c("tv", 1,
                  "Volte à trilha com marcas de pneu e desça a ladeira correndo até a "
                  "cabana no pé dela (os inimigos somem quando você entra). A TV está "
                  "na mesa: ligue e assista ao Night Springs “Quantum Suicide”.", 43),
                c("page", 9,
                  "Use o interruptor da cabana para abrir os portões. Ao sair, a "
                  "página está junto ao portão, antes do chefe.", 44,
                  "Wake Lies to the Sheriff"),
                tip("ep1_stucky",
                    "Chefe Carl Stucky (troféu Nordic Walking). Você perde o "
                    "equipamento no fim do episódio, então gaste sinalizador e "
                    "espingarda sem dó.",
                    tag="troféu", trophies=("nordic_walking",)),
                c("thermos", 12,
                  "Depois do chefe, em cima da esteira de uma das máquinas do pátio.", 45),
            ]),
            sec("O posto de gasolina", [
                c("page", 10,
                  "No pátio do posto, embaixo do carro alegórico do cervo (Deerfest).",
                  47, "Stucky Taken"),
                c("thermos", 13,
                  "Ainda no pátio, no chão junto à placa de preços de combustível.", 48),
                c("thermos", 14,
                  "Antes de entrar no posto, suba a estrada à esquerda até o fim "
                  "(inimigos renascem atrás de você): a garrafa está perto de um "
                  "caminhão. Volte correndo para a luz do posto.", 49),
                c("nm", 3,
                  "Só no Pesadelo. Nos fundos do posto, colada na parede ao lado da "
                  "porta do banheiro feminino.", 397, "Toby the Dog"),
                c("tv", 2,
                  "Ao passar pela oficina para chegar à loja, a TV liga sozinha (é o "
                  "próprio Alan na tela). Conta só de passar.", 50),
                c("sign", 1,
                  "Dentro da loja do posto, examine a placa do 68º Deerfest antes de "
                  "usar o telefone.", 56, "68th Annual Deerfest"),
            ]),
        ],
        "checklist": {"page": 10, "nm": 3, "thermos": 14, "chest": 4, "can": 2,
                      "radio": 2, "tv": 2, "sign": 1},
        "end": "Usar o telefone atrás do balcão encerra o episódio (troféu Bright Falls' Finest).",
    },
    {
        "id": "ep2",
        "num": 2,
        "title": "Taken",
        "pt": "Levada",
        "summary": (
            "A delegacia de dia, o Parque Nacional de Elderwood à noite até o "
            "Lovers' Peak e a volta de carro. É onde saem os troféus de 25 "
            "páginas, 25 garrafas e 5 baús, e o melhor ponto para farmar pássaros."
        ),
        "sections": [
            sec("O apartamento em Nova York", [
                c("thermos", 15,
                  "No escritório da Alice, perto da janela (antes de olhar as capas "
                  "na sua mesa).", 53),
                c("page", 11,
                  "Na mesa do escritório do Alan, ao lado.", 54, "Sudden Stop 1"),
                c("page", 12,
                  "Junto com a anterior, na mesma mesa.", 54, "Sudden Stop 2"),
            ]),
            sec("A delegacia de Bright Falls", [
                c("sign", 2,
                  "Ao sair da sala do médico, vire à esquerda no corredor: os cartazes "
                  "de desaparecidos na parede contam como UMA placa.", 55, "Missing Signs"),
                c("thermos", 16,
                  "Depois de falar com a xerife: volte pelo corredor, vire à esquerda "
                  "e entre na sala à frente. A garrafa está na mesa.", 59),
                c("page", 13,
                  "Na mesma sala, no chão.", 57, "Alice Sees a Shadow"),
                c("page", 14,
                  "No corredor das celas (acenda a luz), na cela aberta do fundo, em "
                  "cima da cama.", 60, "The Dark Presence in the Diner"),
                c("thermos", 17,
                  "Saindo pela porta do fim do corredor, no pátio dos fundos.", 61),
                c("radio", 3,
                  "No mesmo pátio dos fundos, perto da garrafa.", 61),
                c("page", 15,
                  "Chute as tábuas da cerca e examine o carro abandonado. Antes de "
                  "voltar para a delegacia, a página está numa pedra.", 63,
                  "Wake at Lovers' Peak"),
                c("tv", 3,
                  "Ao voltar pelo corredor das celas, a TV liga sozinha. Conta só de "
                  "passar.", 64),
            ]),
            sec("Elderwood: centro de visitantes e a cabana", [
                c("sign", 3,
                  "No centro de visitantes, examine a placa do Buck Toothed Charlie.", 65,
                  "Buck Toothed Charlie"),
                c("thermos", 18,
                  "Enquanto o Barry fala, dê a volta até a copa: a garrafa está lá.", 66),
                c("thermos", 19,
                  "Já na cabana de vocês, desça até a cozinha.", 68),
                c("thermos", 20,
                  "Saia pela porta da cozinha e contorne a cabana até os fundos: ao "
                  "lado da banheira de hidromassagem.", 69),
                c("page", 16,
                  "Volte à frente da cabana e desça a escada: no chão, perto do "
                  "carro.", 70, "Barry Doubts Wake's Sanity"),
            ]),
            sec("A trilha até o Lovers' Peak", [
                c("radio", 4,
                  "Descendo a trilha, entre na primeira cabana à direita: o rádio está "
                  "na mesa.", 71),
                c("tv", 4,
                  "Um pouco depois, segunda cabana: dê a volta e chute a porta dos "
                  "fundos. Assista ao Night Springs “The Man in the Mirror”.", 72),
                c("page", 17,
                  "Na cabine telefônica azul, suba o caminho da direita: a página está "
                  "no gazebo no alto.", 73, "Rose and Rusty"),
                c("page", 18,
                  "De volta à trilha principal, no banco de trás de um carro "
                  "quebrado.", 74, "Rusty Dying"),
                c("thermos", 21,
                  "Quando ouvir os tiros e os gritos do Rusty, NÃO vá direto. No "
                  "prédio à direita, siga pela lateral mais próxima: a garrafa está "
                  "junto de uma árvore.", 75),
                c("thermos", 22,
                  "Volte à trilha, passe o carro abandonado e entre na cabana à "
                  "esquerda.", 76),
                c("page", 19,
                  "Depois de falar com o Rusty, no muro do lado de fora do prédio em "
                  "frente (o escritório dos guardas).", 77,
                  "Rusty Attacked by the Dark Presence"),
                c("page", 20,
                  "Dentro do escritório dos guardas, no chão.", 78,
                  "Wake Reaches a Safe Haven of Light"),
                tip("ep2_rusty",
                    "Matar o Rusty libera Under a Thin Layer of Skin. Tem munição "
                    "infinita no galpão de lenha do canto.",
                    tag="troféu", trophies=("under_a_thin_layer_of_skin",)),
                c("page", 21,
                  "Desça pelo portão por onde vieram os Taken. Na área de piquenique, "
                  "em cima da mesa.", 80, "Rusty's Final Thoughts"),
                c("sign", 4,
                  "Na primeira placa do Lovers' Peak, pegue o caminho da ESQUERDA até "
                  "a caverna: placa da Moonshine Cave.", 81, "Moonshine Cave"),
                c("chest", 5,
                  "Na mesma caverna, siga as setas amarelas: espingarda e baú. Com "
                  "este sai Finders Keepers (5 baús).", 82),
                c("page", 22,
                  "Volte, siga a trilha, enfrente os três Taken e cruze a ponte. Na "
                  "próxima placa do Lovers' Peak, vá à DIREITA até o piquenique: a "
                  "página está no chão.", 83, "Barry Meets Rose"),
                c("sign", 5,
                  "Depois do primeiro Taken pesado, junto ao tronco gigante com túnel: "
                  "placa do Great Old One.", 84, "Great Old One"),
                c("page", 23,
                  "Ligue o gerador do outro lado da ponte. No refúgio, no chão ao lado "
                  "da placa do Lovers' Peak.", 85, "Wake Sees the Torch Symbol"),
                c("thermos", 23,
                  "Do refúgio, olhe à direita: passe a cabine telefônica destruída e "
                  "suba nos troncos. A garrafa está numa pedra.", 86),
                c("thermos", 24,
                  "Passe o arco (Taken pesado com sinalizador). No refúgio seguinte, "
                  "vá no sentido CONTRÁRIO à placa do Lovers' Peak até o piquenique: "
                  "garrafa na mesa.", 87),
                c("sign", 6,
                  "No mesmo piquenique: a placa “Dates from 1846...”.", 88,
                  "Dates from 1846..."),
                c("page", 24,
                  "Volte ao refúgio e pule a cerca (o portão não abre): a página está "
                  "numa pedra.", 89, "Nightingale's Arrival"),
                tip("ep2_flare",
                    "Com o sequestrador: quando a vida estiver baixa, acenda um "
                    "sinalizador de mão (R1) para afastar os Taken. Libera Back! "
                    "Back, I Say! (aqui ou na defesa do mirante).",
                    tag="troféu", trophies=("back_back_i_say",)),
                c("thermos", 25,
                  "Subindo atrás do sequestrador, perto do topo: à direita do mapa do "
                  "parque. Com esta sai Damn Good Cup of Coffee.", 92),
            ]),
            sec("Pela floresta até o moinho", [
                c("page", 25,
                  "Depois de cair do mirante: numa pedra perto dos suprimentos. Com "
                  "esta sai Paging Mr. Wake (25 páginas).", 93, "Alice's Fear of the Dark"),
                c("chest", 6,
                  "Vire-se: desça pelas pedras com marcas amarelas até uma caverna "
                  "rasa.", 94),
                c("can", 3,
                  "Cuidado com as armadilhas de urso. Saia da trilha e siga pela beira "
                  "do penhasco sobre o rio até a área com barris.", 96),
                c("page", 26,
                  "Ali mesmo, numa pedra ao lado de um tronco caído.", 97,
                  "Sarah Thinks About Wake"),
                c("thermos", 26,
                  "Depois do Taken pesado e do gerador nos esconderijos de caça: no "
                  "esconderijo mais perto do gerador, em cima do banco.", 98),
                c("page", 27,
                  "No outro esconderijo, na porta (o rifle de caça está lá dentro).",
                  99, "Wake Hears a Chainsaw"),
                c("chest", 7,
                  "Desça até o avião caído (rocha com marca amarela). Por trás dos "
                  "destroços, suba numa asa e pule para a saliência.", 101),
                c("thermos", 27,
                  "Depois do gerador seguinte, siga a margem do rio até o ponto mais "
                  "alto.", 102),
                c("page", 28,
                  "No moinho: no topo do primeiro lance de escada, NÃO suba mais. "
                  "Atravesse a sala até a sacada: a página está num saco de farinha.",
                  103, "Deputies at the Logging Site"),
                c("page", 29,
                  "Andar seguinte, depois de chutar o contrapeso e atravessar: em "
                  "cima da pilha de sacos.", 104, "Barry in Elderwood"),
                c("thermos", 28,
                  "Na sala depois dos sacos, na mesa do canto.", 105),
                c("page", 30,
                  "Depois do moinho: no prédio com o rifle de caça, suba nas caixas e "
                  "desça do outro lado. A página está em outra caixa (caixas menores "
                  "servem para subir de volta).", 106, "Wake Feels the Dark Presence"),
            ]),
            sec("O camping e a volta de carro", [
                c("thermos", 29,
                  "Antes de entrar no parque de trailers, numa mesa de piquenique.", 107),
                c("page", 31,
                  "Dentro do parque de trailers, vá à esquerda até os chuveiros: no "
                  "chão, perto da lixeira.", 108, "Nightingale Fires at Wake"),
                c("tv", 5,
                  "No banheiro, sala do fundo: ao pegar as chaves da garagem no "
                  "banco, a TV da parede liga sozinha.", 109),
                tip("ep2_car",
                    "Primeiro carro do jogo: Right of Way pede 15 Taken atropelados "
                    "(farol alto com X tira a escuridão, depois é só passar por cima). "
                    "Este trecho é o melhor para adiantar a conta.",
                    tag="troféu", trophies=("right_of_way",)),
                c("thermos", 30,
                  "Saindo do parque, vire à direita e dirija até a estrada bloqueada: "
                  "desça e pegue a garrafa no chão.", 110),
                c("chest", 8,
                  "Volte no sentido contrário. No reboque de toras no meio da "
                  "estrada, desvie à direita até um barraco.", 111),
                c("can", 4,
                  "Atravesse a estrada e o campo até um pequeno camping: pirâmide na "
                  "mesa de piquenique (tem rifle de caça ali).", 112),
                c("thermos", 31,
                  "No caminhão de toras que bloqueia a estrada (emboscada com um "
                  "pesado), desça e entre pela passagem menor da direita: garrafa na "
                  "mesa de piquenique.", 114),
                c("page", 32,
                  "Passe a pilha de toras, vire à direita e desça para o túnel da "
                  "estrada: a página está no chão ao lado de outro caminhão.", 115,
                  "Wake's Despair"),
                c("nm", 4,
                  "Só no Pesadelo. Já a pé, subindo a trilha para a cabana depois do "
                  "telefonema do sequestrador: no chão.", 401,
                  "Wake at the Dark Presence's Mercy"),
                c("chest", 9,
                  "Ao pé da escada da cabana, siga a seta amarela pintada no poço.",
                  117),
                tip("ep2_birdfarm",
                    "Melhor lugar para If It Flies, It Burns: a defesa da varanda tem "
                    "uns 250 pássaros. Se quiser farmar, recarregue o checkpoint e "
                    "repita (a conta é cumulativa).",
                    tag="troféu", trophies=("if_it_flies_it_burns",)),
            ]),
        ],
        "checklist": {"page": 32, "nm": 4, "thermos": 31, "chest": 9, "can": 4,
                      "radio": 4, "tv": 5, "sign": 6},
        "end": "Depois de salvar o Barry dos pássaros, o episódio termina (troféu Park Ranger).",
    },
    {
        "id": "ep3",
        "num": 3,
        "title": "Ransom",
        "pt": "Resgate",
        "summary": (
            "Fuga da polícia até a rádio, a ferrovia com a escavadeira possuída, "
            "a mina de carvão e a subida ao Mirror Peak. Três perdíveis: Heavy "
            "Metal, Iron Horse e o desafio de 30 minutos (Meet the Deadline)."
        ),
        "sections": [
            sec("O parque de trailers da Rose", [
                c("thermos", 32,
                  "Seguindo o Randolph, quando ele para para mostrar o barco caído no "
                  "parque, vá ao trailer da direita: garrafa na mesa de piquenique.", 118),
                c("tv", 6,
                  "Ao acordar no trailer da Rose, a TV liga sozinha.", 119),
                c("thermos", 33,
                  "No cômodo em frente, onde o Barry está desmaiado, no balcão.", 120),
                c("page", 33,
                  "Saindo do trailer, no chão perto da caixa de correio.", 122,
                  "Randolph Calls the Police"),
                c("radio", 5,
                  "Vire à esquerda e passe pelo portão do trailer logo à direita do "
                  "barco: o rádio está nos degraus.", 123),
            ]),
            sec("A fuga da polícia até a rádio", [
                c("page", 34,
                  "Depois de escapar do Nightingale, siga a trilha pela esquerda e "
                  "passe sob a ponte. Já dentro da floresta, no chão.", 125,
                  "The Dark Presence Sleeps"),
                c("page", 35,
                  "Quando a viatura da polícia despenca à sua frente, siga o caminho "
                  "da DIREITA até o fim: na beira da trilha.", 126,
                  "Rose Visited by the Dark Presence"),
                c("thermos", 34,
                  "No mirante à esquerda da trilha (com a luneta), entre na cabana: "
                  "garrafa ao lado do fogão a lenha.", 127),
                c("thermos", 35,
                  "No portão coberto de escuridão, vire à esquerda e suba a ladeira: "
                  "atrás de uma pedra no topo.", 129),
                tip("ep3_poltergeist",
                    "O portão possuído é o primeiro objeto “poltergeist”. They're "
                    "Heeeeeere! pede 20 deles: daqui em diante, destrua com a luz "
                    "todo objeto possuído em vez de só desviar.",
                    trophies=("theyre_heeeeeere",)),
                c("radio", 6,
                  "Depois dos três Taken (bom lugar para Sound and Fury com uma "
                  "granada de luz), no refúgio: rádio em cima de uma caixa.", 130),
                c("page", 36,
                  "Atravesse a ponte à esquerda do refúgio e vire à direita no fim: "
                  "no chão.", 131, "Rose Touched by the Dark Presence"),
                c("chest", 10,
                  "Passando uma pedra grande à direita, siga as marcas amarelas até a "
                  "caverna com um gerador.", 133),
                c("thermos", 36,
                  "Na rádio, antes de entrar, ao lado do carro estacionado.", 134),
                c("radio", 7,
                  "Automático: conta ao entrar no prédio da rádio.", 135),
            ]),
            sec("Da rádio ao pátio ferroviário", [
                c("page", 37,
                  "Depois de pular a janela, desça rumo à caixa d'água: pregada num "
                  "poste da cerca.", 136, "Nightingale in the Radio Station"),
                c("thermos", 37,
                  "Depois do gerador, na bifurcação vá à direita e suba a trilha "
                  "longa. Uns três quartos da subida, no promontório sobre a rádio.",
                  138),
                c("page", 38,
                  "No topo da trilha, na base da torre de rádio.", 137,
                  "Walter Fights Danny"),
                c("page", 39,
                  "Desça, pegue o outro caminho até o carro abandonado. Perto do "
                  "barraco, olhe à direita para algo brilhando: pregada num portão.",
                  139, "Wake Attacked by a Bulldozer"),
                c("can", 5,
                  "Pegar a espingarda no barraco chama vários Taken. Depois, no "
                  "galpão ao lado: pirâmide numa caixa. Com esta sai Carny.", 140),
                c("thermos", 38,
                  "Volte ao barraco da espingarda e pegue o caminho à direita dele: "
                  "no próximo barraco, em cima de um barril.", 141),
                c("page", 40,
                  "Seguindo para a luz ao longe, numa pedra no caminho.", 142,
                  "Sarah Distrusts Nightingale"),
                c("page", 41,
                  "Depois do refúgio e do telefonema da Alice, em cima de um toco.",
                  143, "Wake Attacked by a Possessed Object"),
                c("chest", 11,
                  "Marcas amarelas na pedra ao lado: suba o caminho da esquerda até "
                  "outro barraco.", 144),
                c("nm", 5,
                  "Só no Pesadelo. Depois da ponte ferroviária com os objetos "
                  "voadores, no topo da ladeira vire à DIREITA: num toco.", 402,
                  "Wake and Night Springs"),
                c("page", 42,
                  "No topo da ladeira, siga pela esquerda: numa viga de ferro, antes "
                  "da escada para o refúgio.", 145,
                  "Wake and the Dark Presence in the Lodge"),
                c("thermos", 39,
                  "Pule para o pátio ferroviário, vire à direita e vá até o canto: "
                  "em cima de uns dormentes.", 146),
                c("tv", 7,
                  "No prédio depois do portão (Taken pesado), suba a escada da "
                  "esquerda: TV com o Night Springs “A Family Occasion”.", 147),
                c("page", 43,
                  "Saindo pela porta dessa sala, no corrimão.", 148,
                  "Wake Attacked by the Dark Presence"),
                tip("ep3_bulldozer",
                    "Heavy Metal. A escavadeira possuída pode ser evitada "
                    "correndo para o portão. Para o troféu, DESTRUA a escavadeira: "
                    "mantenha a lanterna focada nela (umas cinco baterias) enquanto "
                    "foge das investidas.",
                    tag="perdível", trophies=("heavy_metal",), img=149),
                c("thermos", 40,
                  "Passando o portão de saída da arena, vire à direita na hora: "
                  "garrafa em cima de um muro.", 150),
            ]),
            sec("Mirror Peak: estrada até a mina de carvão", [
                c("thermos", 41,
                  "De carro, na bifurcação pegue a direita até o fim. Suba a pé até "
                  "a poltrona vermelha no promontório.", 152),
                c("radio", 8,
                  "Siga pela beira do penhasco à esquerda até uma cabana: rádio lá "
                  "dentro.", 153),
                c("radio", 9,
                  "De carro, pare na torre de vigia à direita e suba até a cabana "
                  "do topo.", 154),
                c("page", 44,
                  "Nos prédios da mina à esquerda: entre no mais próximo e suba "
                  "vários lances. Em cima de uma caixa no topo.", 155, "Mott on the Ferry"),
                c("sign", 7,
                  "Na mina (agora museu), ao descer do carro: placa do Bright Falls "
                  "Coal Mine Museum. A placa de trás não conta.", 156,
                  "Bright Falls Coal Mine Museum"),
                c("thermos", 42,
                  "No túnel curto à esquerda da placa.", 158),
                c("page", 45,
                  "A caminho da entrada do museu, no chão.", 157,
                  "Sarah in the Radio Station"),
            ]),
            sec("Mirror Peak: os 30 minutos até o mirante", [
                tip("ep3_deadline",
                    "Refazível: Meet the Deadline. O relógio de 30 minutos "
                    "começa quando você recupera o controle depois da cutscene no "
                    "museu e para quando o Alan avista o mirante. Coletando tudo, "
                    "quase ninguém consegue: faça a coleta agora e refaça este trecho "
                    "depois pelo Seleção de Episódio no Fácil, só correndo.",
                    tag="perdível", trophies=("meet_the_deadline",)),
                c("thermos", 43,
                  "Pule a corrente para o nível de baixo do museu: garrafa numa "
                  "prateleira (o botão verde atrás abre o alçapão).", 159),
                c("page", 46,
                  "Saindo pelo alçapão, em cima de um palete.", 160,
                  "Thomas Zane in Love with Barbara Jagger"),
                c("thermos", 44,
                  "Depois de desligar a energia e subir a escada liberada: no prédio, "
                  "suba a escada de mão. Garrafa numa poltrona.", 161),
                c("page", 47,
                  "Do outro lado da mesma sala, em cima de um palete.", 162,
                  "Wake Touched by the Dark Presence"),
                c("page", 48,
                  "Depois do portão e das duas levas de Taken (use sinalizador), ao "
                  "lado do caminho.", 163, "Wake and Barry in the Cell"),
                c("thermos", 45,
                  "Ao ver uma luz, vá à direita até o refúgio, suba a escada até a "
                  "plataforma de madeira: na ponta dela.", 165),
                c("chest", 12,
                  "Dali, rumo ao prédio branco: as marcas amarelas apontam um túnel "
                  "de mina.", 164),
                c("thermos", 46,
                  "Passe a ponte (troque pela espingarda de bomba). No barraco ao "
                  "longe, à esquerda do prédio abandonado: garrafa na mesa.", 166),
                c("nm", 6,
                  "Só no Pesadelo. No vilarejo minerador, ao chegar no trilho vá à "
                  "ESQUERDA até o fim dele: numa pedra.", 403, "Wake Reads a Page"),
                c("page", 49,
                  "Seguindo pelo trilho (saia do caminho quando o carro vier "
                  "despencando), na beira dos trilhos.", 167, "Wake and Casey"),
                c("sign", 8,
                  "Do outro lado da ponte: placa do Gray Peak Gorge.", 168,
                  "Gray Peak Gorge"),
                c("nm", 7,
                  "Só no Pesadelo. Passe o silo em ruínas à esquerda até a frente do "
                  "prédio arruinado: em cima de umas vigas.", 404,
                  "Doc Examines Barry and Rose"),
                c("thermos", 47,
                  "Contorne a cabana próxima e vire à esquerda até um barraco: "
                  "garrafa em cima de um dormente.", 169),
                tip("ep3_locomotive",
                    "Iron Horse. Depois do túnel, a locomotiva enferrujada "
                    "ataca: destrua a caldeira e depois a cabine com a lanterna "
                    "focada (use as árvores de cobertura). Não passe direto.",
                    tag="perdível", trophies=("iron_horse",)),
                c("thermos", 48,
                  "Atrás do prédio ao lado da locomotiva, numa caixa de madeira.", 170),
                c("tv", 8,
                  "Pegue a chave no telheiro e abra o barraco: a TV liga sozinha ao "
                  "atravessar a sala.", 171),
                c("chest", 13,
                  "Atravesse o pátio, suba duas escadas de mão e vire à esquerda: "
                  "siga as marcas amarelas.", 172),
                c("page", 50,
                  "Na mina de prata, na pedra com escrita amarela pegue o túnel da "
                  "ESQUERDA até o fim (visão). Vire-se: a página está no chão.", 174,
                  "Hunters Taken"),
                c("page", 51,
                  "Volte e pegue o outro túnel, sempre à esquerda, cruze a ponte. Ao "
                  "cair na caverna grande, logo à sua frente.", 175,
                  "Nightingale in the Majestic"),
                c("thermos", 49,
                  "No túnel aberto pelo Taken pesado, mantenha a esquerda: no chão.",
                  176),
                c("page", 52,
                  "Fora da mina, suba a escada da direita até a plataforma com "
                  "mirante.", 181, "Tor Hits Nurse Sinclair"),
                c("can", 6,
                  "Depois do bondinho que quebra: no refúgio, suba à plataforma do "
                  "bondinho. Pirâmide no corrimão.", 182),
                c("sign", 9,
                  "No refúgio seguinte, depois dos quatro Taken: placa do Cauldron "
                  "Lake.", 183, "Cauldron Lake"),
                c("thermos", 50,
                  "Atravesse a ponte de corda (emboscada com um pesado atrás) e vire "
                  "à esquerda: na beira do penhasco.", 184),
                c("chest", 14,
                  "Volte para a trilha e procure a seta amarela numa pedra.", 185),
                c("page", 53,
                  "Ao descer pelos degraus quebrados, numa pedra.", 186,
                  "Mott at Cauldron Lake"),
                c("thermos", 51,
                  "Depois das ruínas (o chão desaba no porão), passe pela fresta na "
                  "parede, desça duas vezes e contorne o prédio: junto a um portão.",
                  187),
                c("page", 54,
                  "Depois de avistar o mirante (aqui sai Meet the Deadline, se deu "
                  "tempo), desça a escada: no pé dela.", 189,
                  "Wake Wakes Up in the Lodge"),
            ]),
        ],
        "checklist": {"page": 54, "nm": 7, "thermos": 51, "chest": 14, "can": 6,
                      "radio": 9, "tv": 8, "sign": 9},
        "end": "O sequestrador morre e o Alan cai no lago (troféu Wheels Within Wheels).",
    },
    {
        "id": "ep4",
        "num": 4,
        "title": "The Truth",
        "pt": "A Verdade",
        "summary": (
            "A clínica do Hartman, o jardim-labirinto e a fazenda dos Anderson. "
            "Três perdíveis em sequência: as fitas do Hartman, a TV do Night "
            "Springs e o show no palco sem ficar com a vida crítica."
        ),
        "sections": [
            sec("A clínica do lago (Cauldron Lake Lodge)", [
                c("sign", 10,
                  "Seguindo o Hartman até a plataforma sobre o lago: placa “In "
                  "Tenebras Cadere” junto ao relógio de sol.", 192, "In Tenebras Cadere"),
                c("thermos", 52,
                  "No salão, do outro lado da lareira, em cima de um balcão.", 190),
                c("sign", 11,
                  "Na parede do fundo do salão: placa “Creator's Dilemma”.", 191,
                  "Creator's Dilemma"),
                c("sign", 12,
                  "No corredor depois da porta que o Hartman abre: placa de boas-"
                  "vindas na parede.", 193, "Welcome to Cauldron Lake Lodge"),
                c("page", 55,
                  "Automática, na cutscene com os irmãos Anderson na sala de jogos.",
                  None, "Thomas Zane's Writing and Assistant"),
                c("tv", 9,
                  "Subindo para os quartos, a TV do patamar liga sozinha.", 194),
                c("thermos", 53,
                  "Dando a volta no patamar, em cima do corrimão.", 195),
                c("page", 56,
                  "Depois da cutscene no seu quarto, no patamar perto da escada.", 196,
                  "Barry in the Lodge"),
                tip("ep4_tapes",
                    "Medical Opinions. Com a chave da enfermeira, abra as "
                    "portas, veja a foto e entre na sala em frente. No gravador da "
                    "mesa, aperte PLAY TRÊS vezes e ouça as três fitas até o fim.",
                    tag="perdível", trophies=("medical_opinions",), img=197),
                c("page", 57,
                  "Na mesma sala do gravador, do outro lado, numa mesa.", 198,
                  "Mott Fails Hartman"),
                c("thermos", 54,
                  "No quarto trancado do Barry, mais adiante no corredor, no "
                  "parapeito da janela.", 199),
                c("page", 58,
                  "Automática ao entrar no escritório do Hartman.", None,
                  "Hartman Watches Wake Fall"),
                tip("ep4_boobtube",
                    "Boob Tube. Na fuga, depois de queimar os ursos de "
                    "madeira com o sinalizador (no Pesadelo pode precisar de dois), "
                    "entre na sala do fim do corredor e LIGUE a TV (Night Springs "
                    "“The Doomed Samaritan”). Não conta como coletável.",
                    tag="perdível", trophies=("boob_tube",), img=200),
                c("page", 59,
                  "Nessa mesma sala, no braço do sofá.", 201, "Hartman's Mission"),
            ]),
            sec("O jardim-labirinto", [
                c("thermos", 55,
                  "Ao sair, o Barry chama: ignore e vá no sentido oposto. Garrafa "
                  "junto ao gradil.", 202),
                c("sign", 13,
                  "A caminho do Barry, na base da estátua: placa “Suspended”.", 203,
                  "Suspended"),
                c("page", 60,
                  "No labirinto: comece pela direita. Depois do Taken, siga para o "
                  "lado de onde ele veio até uma clareira: no chão, junto a uma "
                  "árvore.", 204, "Wake Sees the Old Gods Stage"),
                c("page", 61,
                  "Depois da luta com quatro Taken (um pesado), passe pela abertura e "
                  "siga o caminho: num banco.", 205, "Hartman and the Power Failure"),
                c("thermos", 56,
                  "Depois do enfermeiro com a marreta (chefe), no gazebo dele: no "
                  "chão.", 206),
                c("page", 62,
                  "Atrás do gazebo, no refúgio: entre no galpão. Em cima da pilha de "
                  "sacos.", 207, "Mott in Charge"),
                c("can", 7,
                  "Depois do carrinho de mão possuído e do portão: pirâmide no muro.",
                  208),
                c("page", 63,
                  "Vire-se ali mesmo: no chão.", 209, "Barry Attacked by a Taken"),
                c("chest", 15,
                  "No fundo do jardim, depois dos três Taken: passe pela fresta à "
                  "direita e siga as marcas amarelas até o fim.", 210),
                c("thermos", 57,
                  "Atravesse para o outro lado do lago do jardim e suba ao refúgio: "
                  "garrafa no muro.", 211),
                c("page", 64,
                  "Vire à esquerda e suba os degraus próximos: no muro.", 212,
                  "Hartman Sedates Wake"),
            ]),
            sec("A caminho da fazenda dos Anderson", [
                c("page", 65,
                  "Depois do acidente de carro: ligue o holofote do túnel e vá até o "
                  "fim dele. Pregada no para-choque dos trilhos.", 213,
                  "Walter at the Anderson Farm"),
                c("thermos", 58,
                  "Na plataforma de madeira depois do túnel (desvie dos barris), na "
                  "ponta: em cima de uma caixa.", 214),
                c("page", 66,
                  "No portão bloqueado com a luz quebrada: suba a escada logo depois "
                  "da luz. Na passarela.", 216, "Nightingale Arrests Wake"),
                c("thermos", 59,
                  "No acampamento depois da corrida sem armas (troque pela lanterna "
                  "reforçada): em cima da pilha de lenha.", 218),
                c("page", 67,
                  "Depois do portão possuído, a página desce flutuando da luz forte.",
                  219, "The Dark Presence at Large"),
                c("page", 68,
                  "Passe pelas armadilhas de urso com cuidado. Nas ruínas, ligue o "
                  "gerador: a página está no chão ali perto.", 220,
                  "The Patients Escape the Lodge"),
                c("thermos", 60,
                  "Nos fundos desse prédio, suba a escada (cuidado com a armadilha): "
                  "no parapeito da janela.", 221),
                c("thermos", 61,
                  "No chalé do motorista: cozinha à esquerda, no balcão ao lado da "
                  "pia.", 222),
                c("tv", 10,
                  "No andar de cima, depois de falar com o Walter, entre no outro "
                  "quarto: a TV liga sozinha.", 223),
                c("chest", 16,
                  "Depois do Danny (pesado), pule a janela e desça ao porão.", 224),
                c("page", 69,
                  "Contorne até a varanda: no tapete.", 225,
                  "Hartman Considers Mott and Wake"),
                c("thermos", 62,
                  "De caminhonete, pare no trator enferrujado à direita: no chão ao "
                  "lado dele.", 226),
                c("chest", 17,
                  "Na bifurcação siga reto até a cabana à esquerda.", 228),
                c("radio", 10,
                  "Siga até a torre de vigia à direita e suba ao topo (troque pelo "
                  "rifle de caça).", 229),
                c("thermos", 63,
                  "Volte à bifurcação e vá à esquerda até outro trator enferrujado. "
                  "Pare o carro colado nele: um bando aparece, pegue e fuja.", 227),
                c("chest", 18,
                  "Depois do refúgio e da escavadeira parada, passe a cerca e "
                  "atravesse o campo até o celeiro com marcas amarelas.", 230),
                c("nm", 8,
                  "Só no Pesadelo. Saindo do celeiro, olhe à direita: colada na porta "
                  "da casinha (latrina).", 406, "Hartman During the Missing Week"),
                c("thermos", 64,
                  "Nas arquibancadas em frente ao palco. Pegue ANTES de chegar perto "
                  "(a cutscene dispara) ou depois do show.", 231),
            ]),
            sec("O show e a fazenda", [
                tip("ep4_stage",
                    "Refazível pelo checkpoint: Child of the Elder God. "
                    "Na defesa do palco, não deixe a vida cair na faixa crítica. Se "
                    "cair, recarregue o checkpoint na hora. Pegue a lanterna "
                    "reforçada e use a pistola sinalizadora na primeira onda.",
                    tag="perdível", trophies=("child_of_the_elder_god",)),
                c("thermos", 65,
                  "Depois do show, na cabine de som.", 232),
                c("page", 70,
                  "Atrás do palco, colada na caixa de fusíveis.", 233,
                  "Mulligan Questions Nightingale's Orders"),
                c("page", 71,
                  "Seguindo o Barry: no celeiro à esquerda, entre no campo ao lado, "
                  "passe as máquinas até o fundo. Num reboque enferrujado.", 234,
                  "Nightingale Finds the Manuscript"),
                c("tv", 11,
                  "Dentro do celeiro (depois do interruptor no telhado): TV no meio "
                  "da sala, Night Springs “The Dream of Dreams”.", 236),
                c("thermos", 66,
                  "No mesmo térreo, na mesa do canto.", 237),
                c("page", 72,
                  "Andar de cima, no fundo do celeiro: colada numa pedra rúnica.", 238,
                  "The Anderson Brothers in the 70s"),
                c("sign", 14,
                  "Do outro lado, passando o interruptor do barco: placa do Old Gods "
                  "of Asgard.", 239, "Old Gods of Asgard"),
                c("can", 8,
                  "Saindo pelo buraco do barco viking: pirâmide em cima de um "
                  "carretel de cabo de madeira.", 241),
                c("thermos", 67,
                  "No silo, depois do Taken pesado do segundo andar: na prateleira "
                  "atrás dele.", 242),
                c("radio", 11,
                  "Subindo mais (escada de mão): rádio na mesa junto à janela. Com "
                  "este sai KBF-FM.", 243),
                c("thermos", 68,
                  "Na casa da fazenda, porta logo à direita da entrada: na cadeira.",
                  244),
                c("thermos", 69,
                  "Pela sala de jantar, cozinha à direita: perto da pia.", 245),
                c("page", 73,
                  "Suba a escada da entrada: no patamar.", 246,
                  "The Mystery of the Missing Week"),
            ]),
        ],
        "checklist": {"page": 73, "nm": 8, "thermos": 69, "chest": 18, "can": 8,
                      "radio": 11, "tv": 11, "sign": 14},
        "end": "A caixa de fusíveis e o disco levam à bebedeira e ao sonho (troféu Perchance to Dream).",
    },
    {
        "id": "ep5",
        "num": 5,
        "title": "The Clicker",
        "pt": "O Clicker",
        "summary": (
            "Bright Falls à noite com a xerife até o heliponto (sem morrer, para An "
            "Idyllic Small Town), a segunda metade da jukebox e a usina até a "
            "represa. Tem as comportas do troféu Gatekeeper."
        ),
        "sections": [
            sec("A delegacia e as ruas de Bright Falls", [
                tip("ep5_idyllic",
                    "Refazível: An Idyllic Small Town. Do momento em que "
                    "você acorda na cela até entrar no helicóptero, NÃO pode morrer "
                    "nem recarregar checkpoint. Na dúvida, foque na coleta agora e "
                    "refaça este trecho pelo Seleção de Episódio no Fácil.",
                    tag="perdível", trophies=("an_idyllic_small_town",)),
                c("page", 74,
                  "No chão, do lado de fora da cela.", 251,
                  "Nightingale Reads the Manuscript"),
                c("page", 75,
                  "No canto, junto com a anterior.", 251,
                  "Nightingale Attacked by the Dark Presence"),
                c("thermos", 70,
                  "Na recepção, enquanto a Sarah fala com o Barry: em cima de um "
                  "arquivo.", 249),
                c("thermos", 71,
                  "Depois de escapar do carro alegórico desgovernado e dos Taken: na "
                  "bilheteria.", 252),
                c("chest", 19,
                  "A seta amarela na bilheteria: vá à direita até o fim da rua.", 253),
                c("chest", 20,
                  "Volte e siga com a Sarah. No prédio “Fresh Seafood” à direita, "
                  "passe o portão e contorne até os fundos.", 254),
                c("thermos", 72,
                  "Na lanchonete Oh Deer, atrás do balcão, no chão.", 255),
                tip("ep5_jukebox",
                    "2ª metade de Drink 'Em Both Up. Se você tocou a "
                    "jukebox no Episódio 1, use a MESMA jukebox de novo agora. Se não "
                    "tocou lá, o troféu exige refazer o Episódio 1 pelo Seleção de "
                    "Episódio e depois este trecho.",
                    tag="perdível", trophies=("drink_em_both_up",)),
                c("page", 76,
                  "No corredor do fundo da lanchonete, colada na parede.", 256,
                  "Barry in the Sheriff's Station"),
                c("can", 9,
                  "Depois do refúgio na cancela: atravesse a rua até o trailer de "
                  "cachorro-quente. Pirâmide em cima dele.", 257),
                c("thermos", 73,
                  "Descendo a rua, passando a faixa de Bright Falls: no chão ao lado "
                  "de um banheiro químico.", 258),
                c("thermos", 74,
                  "Depois do Taken com motosserra, passe o portão: na tenda da "
                  "esquerda, em cima da mesa.", 259),
                c("tv", 12,
                  "Na prefeitura, suba a escada da esquerda: Night Springs “Taken in "
                  "His Prime”.", 260),
                c("chest", 21,
                  "Na porta à esquerda da TV (um Taken cai do teto).", 261),
                c("page", 77,
                  "Desça e vá ao salão de reuniões: perto do púlpito.", 262,
                  "The Dark Presence Set Back"),
                c("thermos", 75,
                  "Depois do Taken pesado do saguão, na sala de onde ele saiu: copa à "
                  "direita, no balcão.", 263),
                c("sign", 15,
                  "Com a chave do helicóptero, atravesse a rua e entre no parque: "
                  "placa dos fundadores na base da estátua.", 264, "Founders of Bright Falls"),
                c("thermos", 76,
                  "Na livraria que a Sarah abre: na estante mais perto da janela.", 265),
                c("sign", 16,
                  "Na parede da direita da livraria: placa dos livros do Alex Casey.",
                  266, "Alex Casey Books"),
                c("page", 78,
                  "Ao lado do caixa da livraria.", 267, "Cynthia's Work"),
                c("chest", 22,
                  "Saindo pelos fundos, não siga a Sarah ainda: marcas amarelas levam "
                  "a um galpão.", 268),
                c("thermos", 77,
                  "No parquinho, cavando na caixa de areia à direita.", 269),
                c("page", 79,
                  "Perto da igreja: atrás da van amarela, no chão.", 270,
                  "Barry in the General Store"),
                c("sign", 17,
                  "No mural da igreja: “Church Events, Fall Schedule”.", 271,
                  "Church Events, Fall Schedule"),
                c("page", 80,
                  "Dentro da igreja, no púlpito.", 273, "The Dark Presence Hunts Wake"),
                c("thermos", 78,
                  "No porão da igreja, depois dos dois pesados: no canto mais "
                  "distante.", 274),
                c("page", 81,
                  "Seguindo a Sarah, no alto do segundo lance de escada: numa mesa "
                  "de piquenique.", 275, "Alice Trapped in the Dark"),
                c("thermos", 79,
                  "No heliponto, à esquerda do helicóptero (antes da horda).", 272),
            ]),
            sec("A usina Bright Falls Light and Power", [
                c("thermos", 80,
                  "Depois de cair do helicóptero, saia do galpão e atravesse o pátio: "
                  "num muro baixo.", 276),
                c("thermos", 81,
                  "No armazém, depois de pular as caixas (inimigos sem fim): nos "
                  "fundos, entre os canos de concreto. Dá para voltar e pegar depois "
                  "do refúgio.", 277),
                c("chest", 23,
                  "Do refúgio, suba a ladeira, desça ao pátio e vá à esquerda.", 278),
                c("page", 82,
                  "Você vê a página atrás dos cabos elétricos; contorne pela escada "
                  "da frente e pelos portões (dois pesados) até chegar nela.", 279,
                  "Cynthia on Her Way to the Dam"),
                c("thermos", 82,
                  "Na área cercada de cabos elétricos depois do armário de "
                  "emergência (dois pesados): num palete atrás de você.", 280),
                c("page", 83,
                  "Baixe a plataforma elevatória e suba no telhado: numa poltrona.",
                  281, "Wake's Plan"),
                c("sign", 18,
                  "Na ponte giratória aberta: placa do Lt. William T.G. Randall "
                  "Memorial Bridge.", 282, "Lt. William T.G. Randall Memorial Bridge"),
                c("nm", 9,
                  "Só no Pesadelo. Suba a estrada à esquerda: no asfalto, perto do "
                  "ônibus escolar.", 407, "Children of the Elder God Lyrics 1"),
                c("thermos", 83,
                  "Atravesse a estrada: à direita da cabine de controle da ponte.", 283),
                c("thermos", 84,
                  "Gire a ponte, pule nela e desça na próxima estrada: no prédio à "
                  "esquerda, no sofá.", 284),
                c("tv", 13,
                  "No mesmo prédio: Night Springs “An Absence of Creativity”.", 285),
                c("chest", 24,
                  "Você passa correndo por ele na fuga com o holofote do helicóptero. "
                  "Do refúgio perto da usina, volte, limpe os inimigos e abra.", 286),
                c("thermos", 85,
                  "Depois do carretel de cabo e da horda, no estacionamento: canto "
                  "superior esquerdo, junto à cerca.", 287),
                c("sign", 19,
                  "Ao lado da porta do Generator Hall: placa “Warning”. Leia ANTES de "
                  "entrar (a cutscene dispara na porta).", 288, "Warning"),
                c("thermos", 86,
                  "No cantinho da Cynthia, junto à escrivaninha.", 289),
                c("nm", 10,
                  "Só no Pesadelo. Ela aparece do outro lado da cerca do "
                  "estacionamento. No pátio dos transformadores, mate o Taken fraco e "
                  "siga a cerca para pegá-la.", 408, "The Poet and the Muse Lyrics 4"),
                c("sign", 20,
                  "No refúgio do pátio: placa dos controles das comportas.", 290,
                  "Floodgate controls"),
                tip("ep5_floodgates",
                    "Comportas (Gatekeeper): aperte os interruptores na ordem 1, 2, 3 "
                    "e depois 1 de novo. As três ficam fechadas.",
                    tag="troféu", trophies=("gatekeeper",), img=291),
                c("can", 10,
                  "No interruptor de desligar a energia, depois das comportas: "
                  "pirâmide na parede lateral.", 292),
                c("page", 84,
                  "No caminho para o helicóptero caído, no pé da ladeira: nas pedras.",
                  293, "The Falling Helicopter"),
                c("nm", 11,
                  "Só no Pesadelo. Depois do refúgio, suba na árvore caída da direita "
                  "(a que volta pelo caminho).", 410, "Children of the Elder God Lyrics 2"),
                c("chest", 25,
                  "Depois de ajudar a Sarah e o Barry: marcas amarelas no barraco, "
                  "suba o caminho à esquerda dele.", 294),
                c("thermos", 87,
                  "Chegando à represa, num pedaço de cano de concreto.", 296),
                c("thermos", 88,
                  "Depois do elevador, vá à direita e desça: na beira do penhasco.", 297),
                c("sign", 21,
                  "Vire-se e suba: placa “Notice” na parede, ao lado do botão.", 298,
                  "Notice"),
                c("page", 85,
                  "Depois dos carretéis de cabo possuídos, pule a cerca: numa pedra.",
                  299, "Zane's Shoebox"),
                c("thermos", 89,
                  "Fugindo pela represa, desça a escada em caracol: na prateleira lá "
                  "embaixo.", 300),
            ]),
        ],
        "checklist": {"page": 85, "nm": 11, "thermos": 89, "chest": 25, "can": 10,
                      "radio": 11, "tv": 13, "sign": 21},
        "end": "O Clicker na Sala Bem Iluminada encerra o episódio (troféu The Lady of the Light).",
    },
    {
        "id": "ep6",
        "num": 6,
        "title": "Departure",
        "pt": "Partida",
        "summary": (
            "A estrada até o Cauldron Lake sem disparar arma (Gunless Wonder), o "
            "ferro-velho, o tornado e o Lugar Escuro. Fecha placas, baús, TV, "
            "páginas e garrafas."
        ),
        "sections": [
            sec("Nova York e o começo da estrada", [
                c("tv", 14,
                  "No apartamento, com os óculos escuros e o remédio já pegos: use o "
                  "controle remoto na sala e assista à entrevista. Com esta sai "
                  "Couch Potato.", 302),
                c("thermos", 90,
                  "De volta ao presente, assim que ganhar o controle: vire-se, na "
                  "mesa de piquenique.", 303),
                tip("ep6_gunless",
                    "Refazível: Gunless Wonder. Daqui até chegar no "
                    "tornado, NÃO dispare arma nenhuma (revólver, espingarda, rifle). "
                    "Granada de luz, sinalizador de mão e atropelar com o carro podem. "
                    "Deixe a pistola sinalizadora de lado também: as fontes só "
                    "garantem os outros três. Se atirar sem querer, recarregue o "
                    "checkpoint.",
                    tag="perdível", trophies=("gunless_wonder",)),
                c("sign", 22,
                  "Depois da ponte, entre na área de piquenique à direita: placa do "
                  "Majestic Motel.", 304, "Majestic Motel"),
                c("chest", 26,
                  "Pegue a estrada de madeireira à esquerda até o fim: barraco com o "
                  "baú.", 305),
                c("thermos", 91,
                  "Na casa à esquerda da estrada: na lateral, atrás de uma caixa.", 306),
                c("page", 86,
                  "Depois do túnel bloqueado (vira noite), no meio da estrada.", 307,
                  "The Dark Presence Wants to Stop Wake"),
            ]),
            sec("Majestic Motel e a ponte possuída", [
                c("can", 11,
                  "No Majestic Motel, pirâmide no muro. NÃO ATIRE (Gunless Wonder): "
                  "suba pelo outro lado do muro e derrube as latas na mão.", 308),
                c("sign", 23,
                  "No quarto ao lado da recepção: placa do Majestic Motel na parede.",
                  309, "Majestic Motel"),
                c("thermos", 92,
                  "No banheiro ao lado.", 310),
                c("nm", 12,
                  "Só no Pesadelo. No sofá da recepção.", 413,
                  "The Poet and the Muse Lyrics 1"),
                c("nm", 13,
                  "Só no Pesadelo. Depois da ponte, no celeiro iluminado à esquerda: "
                  "suba e olhe na prateleira do fundo.", 414,
                  "The Poet and the Muse Lyrics 2"),
                c("thermos", 93,
                  "Na casa escura à esquerda da estrada, nos degraus.", 312),
                c("page", 87,
                  "Depois do túnel com os Taken, no refúgio do fim: volte para dentro "
                  "do túnel. Perto da entrada.", 313, "The Trail of the Dark Presence"),
            ]),
            sec("O ferro-velho do Larsen", [
                c("page", 88,
                  "Passe a placa do Larsen's Auto Salvage e vá até o túnel bloqueado: "
                  "num caminhão.", 315, "Sarah and Barry in the Well-Lit Room"),
                c("sign", 24,
                  "Volte até a placa do Larsen: “Monday through Friday” na cerca "
                  "abaixo do outdoor.", 314, "Monday through Friday"),
                c("chest", 27,
                  "No refúgio do ferro-velho, vá à esquerda do prédio e siga as marcas "
                  "amarelas.", 316),
                c("sign", 25,
                  "À esquerda da porta do prédio: “ALL VISITORS...”. Com esta sai "
                  "Bright Falls Aficionado.", 317, "ALL VISITORS..."),
                c("thermos", 94,
                  "Dentro, porta da esquerda (três Taken): na prateleira.", 318),
                c("nm", 14,
                  "Só no Pesadelo. No andar de cima, numa escrivaninha.", 416,
                  "The Poet and the Muse Lyrics 3"),
                c("can", 12,
                  "Na sacada, no corrimão. NÃO ATIRE: pule em frente às latas até "
                  "derrubar (leva algumas tentativas) ou deixe para a run do "
                  "Pesadelo.", 319),
                c("thermos", 95,
                  "Passe o portão de carro; antes da rampa, desça e corra ao pátio à "
                  "direita: num palete.", 320),
                c("page", 89,
                  "Depois das duas rampas, na plataforma com holofote: atrás dela, "
                  "num fogão velho.", 321, "Thomas Zane's Last Dive"),
                c("chest", 28,
                  "No refúgio da ponte caída: dentro do barraco ao lado.", 323),
            ]),
            sec("O tornado", [
                c("thermos", 96,
                  "Quando o tornado desce, entre na loja em ruínas à direita: na "
                  "prateleira.", 325),
                c("page", 90,
                  "Empurre o carrinho de mina da porta (sinalizador de mão para "
                  "segurar os Taken): lá dentro.", 326, "The Dark Place"),
                c("chest", 29,
                  "Depois da descida no carrinho de mina: passe o vagão depois do "
                  "refúgio e desça a ladeira.", 328),
                c("thermos", 97,
                  "Na via elevada, depois de empurrar o carrinho e pular o vão: no "
                  "chão.", 329),
                c("thermos", 98,
                  "Com objetos caindo do céu, dentro de um vagão.", 330),
                c("chest", 30,
                  "No prédio à direita depois de mais dois lances de escada. Com este "
                  "sai Every Nook and Cranny.", 331),
                c("thermos", 99,
                  "No térreo, atrás da torre à esquerda.", 332),
                c("nm", 15,
                  "Só no Pesadelo. Atrás do gerador na plataforma baixa, colada na "
                  "cerca. Com esta sai Collector's Edition.", 417, "Zane's Poem"),
                c("page", 91,
                  "No alto do elevador, no chão. Com esta sai Picking Up After "
                  "Yourself.", 335, "The Way through the Dark Place"),
                tip("ep6_tornado",
                    "Ao se aproximar do tornado sai Gunless Wonder (se não atirou). "
                    "Atire com a pistola sinalizadora no centro dele até acabar "
                    "(troféu Tornado Wrangler).",
                    tag="troféu", trophies=("gunless_wonder", "tornado_wrangler")),
            ]),
            sec("O Lugar Escuro", [
                c("thermos", 100,
                  "Na paisagem de palavras, à esquerda do sofá: ilumine a palavra "
                  "“thermos” até ela virar garrafa. Com esta sai Hypercaffeinated.",
                  338),
            ]),
        ],
        "checklist": {"page": 91, "nm": 15, "thermos": 100, "chest": 30, "can": 12,
                      "radio": 11, "tv": 14, "sign": 25},
        "end": (
            "Os créditos liberam o troféu da dificuldade em que você jogou e os das "
            "menores (Pesadelo dá Alan, Wake Up, Hardboiled Writer e Departure)."
        ),
    },
]
