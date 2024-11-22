import os  # Para limpar o terminal
from backend import (
    embaralhar_baralho,
    distribuir_cartas,
    organizar_cartas,
    iniciar_rodada,
    jogar_rodadas
)
from variaveis import BARALHO

def limpar_terminal():
    """Limpa o terminal para manter o jogo organizado."""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_mesa(jogadores_cartas, cartas_ganhas_por_jogador, pontos_por_jogador):
    """
    Exibe as cartas de cada jogador e o estado dos pontos na mesa.
    """
    limpar_terminal()
    print("\n--- Mesa de Jogo ---")
    print(" Jogador 1 | Jogador 2 | Jogador 3 | Jogador 4")
    print("----------------------------------------------")
    for i, cartas in enumerate(jogadores_cartas, start=1):
        print(f"Jogador {i}: {cartas}")
    
    print("\n--- Mesa de Pontos ---")
    print(" Jogador 1 | Jogador 2 | Jogador 3 | Jogador 4")
    print("----------------------------------------------")
    print(f"   {pontos_por_jogador[0]} | {pontos_por_jogador[1]} | {pontos_por_jogador[2]} | {pontos_por_jogador[3]}")
    
    print("\n--- Estado Atual ---")
    for i, cartas_ganhas in enumerate(cartas_ganhas_por_jogador, start=1):
        print(f"Jogador {i}: Cartas ganhas: {cartas_ganhas} = {len(cartas_ganhas)} pontos")

def iniciar_jogo():
    print("Bem-vindo ao Jogo de Copas!")

    embaralhado = embaralhar_baralho(BARALHO)
    distribuicao = distribuir_cartas(embaralhado)

    jogadores_cartas = [organizar_cartas(jogador) for jogador in distribuicao]

    # Inicializar estado do jogo
    cartas_ganhas_por_jogador = [[] for _ in range(4)]
    pontos_por_jogador = [0, 0, 0, 0]

    # Inicializar rodada
    primeiro_jogador = iniciar_rodada(jogadores_cartas)
    print(f"Jogador {primeiro_jogador + 1} começa a rodada.")

    jogar_rodadas(jogadores_cartas, primeiro_jogador, cartas_ganhas_por_jogador, pontos_por_jogador)

    mostrar_mesa(jogadores_cartas, cartas_ganhas_por_jogador, pontos_por_jogador)
    print("Jogo finalizado!")

def landing_page():
    """
    Exibe o menu inicial onde o jogador escolhe iniciar o jogo ou sair.
    """
    while True:
        print("\nEscolha uma opção:")
        print("1 - Começar Jogo")
        print("2 - Sair")
        opcao = input("Digite o número da opção: ")

        if opcao == "1":
            iniciar_jogo()
            break
        elif opcao == "2":
            print("Saindo do jogo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa a página inicial
landing_page()
