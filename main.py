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
    for i, cartas in enumerate(jogadores_cartas, start=1):
        print(f"Jogador {i}: {cartas}")
    
    print("\n--- Mesa de Pontos ---")
    for i, pontos in enumerate(pontos_por_jogador, start=1):
        print(f"Jogador {i}: {pontos} pontos")
    
    print("\n--- Estado Atual ---")
    for i, cartas_ganhas in enumerate(cartas_ganhas_por_jogador, start=1):
        print(f"Jogador {i}: Cartas ganhas: {cartas_ganhas} ({len(cartas_ganhas)} cartas)")

def iniciar_jogo():
    """
    Função principal para iniciar o jogo, configurando o baralho e o estado inicial.
    """
    print("Bem-vindo ao Jogo de Copas!")
    
    # Preparar baralho e distribuir cartas
    embaralhado = embaralhar_baralho(BARALHO)
    distribuicao = distribuir_cartas(embaralhado)
    jogadores_cartas = [organizar_cartas(jogador) for jogador in distribuicao]

    # Inicializar estado do jogo
    cartas_ganhas_por_jogador = [[] for _ in range(4)]
    pontos_por_jogador = [0, 0, 0, 0]

    # Determinar quem começa a rodada
    primeiro_jogador = iniciar_rodada(jogadores_cartas)
    print(f"Jogador {primeiro_jogador + 1} começa a rodada com o 2♣.\n")

    # Jogar rodadas
    jogar_rodadas(jogadores_cartas, primeiro_jogador, cartas_ganhas_por_jogador, pontos_por_jogador)

    # Exibir estado final da mesa
    mostrar_mesa(jogadores_cartas, cartas_ganhas_por_jogador, pontos_por_jogador)
    print("\nJogo finalizado! Obrigado por jogar.")

def landing_page():
    """
    Página inicial para navegar entre começar o jogo e sair.
    """
    while True:
        limpar_terminal()
        print("=== Bem-vindo ao Jogo de Copas ===")
        print("Escolha uma opção:")
        print("1 - Começar Jogo")
        print("2 - Sair")
        opcao = input("Digite o número da opção: ").strip()

        if opcao == "1":
            iniciar_jogo()
            input("\nPressione Enter para voltar ao menu principal...")
        elif opcao == "2":
            print("\nSaindo do jogo. Até a próxima!")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

# Executa a página inicial
if __name__ == "__main__":
    landing_page()
