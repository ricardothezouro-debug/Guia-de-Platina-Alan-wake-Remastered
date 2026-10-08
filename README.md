# Alan Wake Remastered: Platina

Guia de platina em PT-BR de Alan Wake Remastered (PS4/PS5) para o
[Streamer Sidekick](https://github.com/ricardothezouro-debug/streamer_sidekick).
Instala pela aba **Platinas** do app e também roda sozinho.

## O que tem

- **Plano**: as duas zeradas (Normal seguindo a rota, depois Pesadelo atrás das
  15 páginas exclusivas), a limpeza pelo Seleção de Episódio e os perdíveis de
  relance.
- **Rota**: os seis episódios na ordem, com os 298 coletáveis do jogo base no
  ponto exato ("depois da cutscene com o Stucky, passe a empilhadeira") e a foto
  de cada um. Os perdíveis aparecem antes do ponto em que podem escapar. No fim
  de cada episódio, os totais que as Estatísticas do jogo devem mostrar.
- **Coletáveis**: os mesmos itens agrupados por tipo (91 páginas, 15 páginas do
  Pesadelo, 100 garrafas, 30 baús, 12 pirâmides, 11 rádios, 14 TVs, 25 placas).
- **Troféus**: os 51 do jogo base, com tier, categoria e como pegar.
- **Expansões**: os 17 troféus de The Signal e The Writer, que ficam num grupo
  separado e não contam para a platina.

Marcar um item marca ele em todas as abas. O progresso fica na pasta de dados do
Streamer Sidekick, fora da pasta do plugin.

## Rodar sozinho

```bash
pip install -r requirements.txt
PYTHONPATH=src python -m platina_alan_wake
```

No Windows (cmd): `set PYTHONPATH=src && python -m platina_alan_wake`.

## Testes

```bash
QT_QPA_PLATFORM=offscreen python -m pytest -q
```

Os testes isolam a pasta de dados numa pasta temporária e não acessam a rede.

## Fotos

As fotos são capturas do guia de PS5 de Christopher Williams na GameFAQs e são
exibidas a partir do site dele, com crédito na aba Plano. Elas são baixadas pelo
QtNetwork e guardadas em cache: a GameFAQs recusa a conexão TLS do `urllib` do
Python mesmo com cabeçalhos de navegador. Os textos deste guia são próprios.

## Fontes

- Ordem e fotos dos coletáveis: [GameFAQs, guia de PS5](https://gamefaqs.gamespot.com/ps5/330504-alan-wake-remastered/faqs/81217)
- Lista de troféus, tiers e grupos das expansões: [Exophase](https://www.exophase.com/game/alan-wake-remastered-psn/trophies/)
- Dificuldades do Remastered e troféus que acumulam: [Alan Wake Wiki](https://alanwake.fandom.com/wiki/Hardboiled_Writer)
