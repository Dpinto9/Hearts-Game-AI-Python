# variaveis.py

# Naipes e valores do baralho
NAIPES = ['♠', '♥', '♦', '♣']
VALORES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Criação do baralho
BARALHO = [f"{valor}{naipe}" for valor in VALORES for naipe in NAIPES]
