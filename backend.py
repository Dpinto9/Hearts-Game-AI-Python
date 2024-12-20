# backend.py
import random
from variaveis import BARALHO, NAIPES, VALORES

def embaralhar_baralho (baralho):
    random.shuffle(baralho)
    return baralho
# embaralhar_baralho

# =========================================================
#                   Inicio de Jogo
# =========================================================

def distribuir_cartas(baralho, jogadores=4):
    cartas_por_jogador = len(baralho) // jogadores #valor inteiro da divisao

    distribuicao = [] 
    for i in range (jogadores):
        inicio = i * cartas_por_jogador 
        fim = inicio + cartas_por_jogador

        distribuicao.append(baralho[inicio:fim])


    return distribuicao
# distribuir_cartas

def organizar_cartas(cartas):
    ordem_valores = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                     '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    # Função para determinar a "posição" da carta
    def posicao_carta(carta):
        valor = carta[:-1] #Elimina o ultimo caracter
        naipe = carta[-1] #Apenas o ultimo caracter
        return (naipe, ordem_valores[valor])

    return sorted(cartas, key=posicao_carta)
#organizar_cartas

def encontrar_primeiro_jogador (jogadores_cartas):
    for i, cartas in enumerate(jogadores_cartas):
        if '2♣' in cartas:
            return i  # Retorna o índice do jogador
#encontrar_primeiro_jogador

# =========================================================
#                   A jogar Rodadas
# =========================================================

def naipe_correto (carta_lider, mao_jogador):
    naipe_lider = carta_lider [-1] 

    return any(carta.endswith(naipe_lider) for carta in mao_jogador) #disponibiliza qualquer carta do mesmo naipe
#naipe_correto

def validar_jogada(carta, mao_jogador, carta_lider, rodada, copas_jogadas):
    if rodada == 0:  # Primeira rodada não permite jogar Copas
        if carta[-1] == '♥':
            print("Você não pode jogar Copas na primeira rodada!")
            return False
    elif carta_lider is None:  # Primeira jogada da rodada
        if carta[-1] == '♥' and not copas_jogadas:  # Não pode iniciar com Copas, exceto se já foi jogado
            print("Você não pode iniciar a rodada com Copas!")
            return False

    # Verifica se pode seguir o naipe líder
    if carta_lider and not carta.endswith(carta_lider[-1]):
        if any(c.endswith(carta_lider[-1]) for c in mao_jogador):
            print("Jogada inválida! Deve seguir o naipe, se possível.")
            return False

    return True
#validar_jogada

def iniciar_rodada (jogadores_cartas):
    #Determinar quem começa a rodada
    primeiro_jogador = encontrar_primeiro_jogador(jogadores_cartas)
    return primeiro_jogador
#iniciar_rodada

def jogar_rodadas(jogadores_cartas, primeiro_jogador, cartas_ganhas_por_jogador, pontos_por_jogador):
    """
    Joga todas as rodadas até que todos os jogadores fiquem sem cartas.
    """
    copas_jogadas = False  # Flag para saber se Copas já foi jogado

    while any(len(mao) > 0 for mao in jogadores_cartas):  # Continua enquanto há cartas nas mãos dos jogadores
        total_cartas = len(jogadores_cartas[0])  # Número de rodadas igual ao número de cartas por jogador

        for rodada in range(total_cartas):
            if all(len(mao) == 0 for mao in jogadores_cartas):  # Se todos os baralhos estiverem vazios, finaliza
                finalizar_jogo(pontos_por_jogador)
                return
            
            cartas_jogadas = []  # Lista para armazenar as cartas jogadas na rodada
            jogador_atual = primeiro_jogador
            carta_lider = None  # Inicialmente não há carta líder

            print(f"\n--- Rodada {rodada + 1} ---")
            
            for turno in range(len(jogadores_cartas)):  # Cada jogador joga uma vez por rodada
                mao_jogador = jogadores_cartas[jogador_atual]  # Mão do jogador atual
                if not mao_jogador:  # Se o jogador não tiver cartas, pula para o próximo
                    jogador_atual = (jogador_atual + 1) % len(jogadores_cartas)
                    continue

                print(f"\nJogador {jogador_atual + 1}, suas cartas: {mao_jogador}")

                if rodada == 0 and turno == 0 and '2♣' in mao_jogador:
                    # Primeira jogada obrigatória com 2♣
                    carta_jogada = '2♣'
                    print(f"Jogador {jogador_atual + 1} jogou: {carta_jogada}")
                    jogadores_cartas[jogador_atual].remove(carta_jogada)
                    cartas_jogadas.append(carta_jogada)
                    carta_lider = carta_jogada
                else:
                    # Jogador escolhe a carta
                    while True:
                        carta_jogada = input(f"Jogador {jogador_atual + 1}, escolha uma carta para jogar: ").strip()
                        
                        if carta_jogada not in mao_jogador:
                            print("Carta inválida! Escolha uma carta que esteja na sua mão.")
                            continue
                        
                        if not validar_jogada(carta_jogada, mao_jogador, carta_lider, rodada, copas_jogadas):
                            continue
                        
                        # Se a carta for válida, remove-a e avança
                        jogadores_cartas[jogador_atual].remove(carta_jogada)
                        cartas_jogadas.append(carta_jogada)

                        # Define a carta líder se ainda não houver uma
                        if not carta_lider:
                            carta_lider = carta_jogada
                        if carta_jogada[-1] == '♥':
                            copas_jogadas = True  # Alguém jogou Copas, portanto, agora é válido seguir o naipe

                        break  # Sai do loop quando a carta é válida
                
                # Próximo jogador
                jogador_atual = (jogador_atual + 1) % len(jogadores_cartas)

            # Após todos jogarem, determinar o vencedor da rodada
            vencedor = determinar_vencedor_rodada(cartas_jogadas, primeiro_jogador)

            # Atualizar cartas ganhas e pontos
            cartas_ganhas_por_jogador[vencedor].extend(cartas_jogadas)

            # Configurar o vencedor como o primeiro jogador da próxima rodada
            primeiro_jogador = vencedor

            # Exibir o estado atual
            print("\nEstado atual:")
            for jogador in range(len(cartas_ganhas_por_jogador)):
                # Filtrar cartas de copas (♥)
                cartas_ganhas = cartas_ganhas_por_jogador[jogador]
                cartas_copas = [carta for carta in cartas_ganhas if '♥' in carta or carta == 'Q♠']

                # Usar calcular_pontos para obter a pontuação correta
                pontos_atual = calcular_pontos(cartas_ganhas)

                print(f"Jogador {jogador + 1}: Cartas ganhas: {cartas_ganhas}, {cartas_copas} = {pontos_atual} pontos")

    # Finalizar o jogo quando todas as cartas forem jogadas
    finalizar_jogo(pontos_por_jogador)
#jogar_rodadas


# =========================================================
#                   Finalizar Rodada
# =========================================================

def determinar_vencedor_rodada(cartas_jogadas, primeiro_jogador):
    print(f"Cartas jogadas: {cartas_jogadas}")
    naipe_lider = cartas_jogadas[0][-1]  # O naipe da primeira carta jogada
    maior_carta = cartas_jogadas[0]
    vencedor = primeiro_jogador

    for i, carta in enumerate(cartas_jogadas):
        print(f"Analisando carta: {carta}")
        if carta[-1] == naipe_lider:  # Apenas considera cartas do naipe líder
            if valor_carta(carta) > valor_carta(maior_carta):  # Compara os valores das cartas
                maior_carta = carta
                vencedor = (primeiro_jogador + i) % len(cartas_jogadas)  # Determina o índice do vencedor
                print(f"Nova maior carta: {maior_carta} por Jogador {vencedor + 1}")

    print(f"Vencedor determinado: Jogador {vencedor + 1} com a carta {maior_carta}")
    return vencedor
#determinar_vencedor_rodada

def calcular_pontos(cartas_ganhas):
    """Calcula a pontuação com base nas cartas ganhas."""
    pontos = 0
    for carta in cartas_ganhas:
        if carta[-1] == '♥':  # Cada coração vale 1 ponto
            pontos += 1
        if carta == 'Q♠':  # Dama de Espadas vale 13 pontos
            pontos += 13
    return pontos
# calcular_pontos

def valor_carta(carta):
    """
    Retorna o valor numérico de uma carta para comparações.
    """
    valores = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
        "7": 7, "8": 8, "9": 9, "10": 10,
        "J": 11, "Q": 12, "K": 13, "A": 14
    }
    # Extrai o valor da carta (primeira parte da string)
    valor = carta[:-1]  # Remove o naipe
    return valores[valor]
#valor_carta

def finalizar_rodada(cartas_jogadas, primeiro_jogador, cartas_ganhas_por_jogador):
    """
    Finaliza a rodada:
    - Determina o vencedor.
    - Atribui as cartas jogadas ao vencedor.
    - Calcula os pontos apenas das cartas ♥ e da Q♠.
    """
    # Determina o vencedor da rodada
    vencedor = determinar_vencedor_rodada(cartas_jogadas, primeiro_jogador)

    # Adiciona as cartas jogadas ao vencedor
    cartas_ganhas_por_jogador[vencedor].extend(cartas_jogadas)

    # Calcula os pontos para cada jogador com base nas cartas ganhas
    pontos_por_jogador = {
        jogador: calcular_pontos(cartas)
        for jogador, cartas in enumerate(cartas_ganhas_por_jogador)
    }

    return vencedor, cartas_ganhas_por_jogador, pontos_por_jogador

# =========================================================
#                   Finalizar Jogo
# =========================================================

def finalizar_jogo(pontos_por_jogador):
    vencedor = min(pontos_por_jogador, key=pontos_por_jogador.get)  # Jogador com menos pontos
    menor_pontuacao = pontos_por_jogador[vencedor]

    print("\n=== Fim do Jogo ===")
    print("Pontuações Finais:")
    for jogador, pontos in pontos_por_jogador.items():
        print(f"Jogador {jogador + 1}: {pontos} pontos")
    
    print(f"\nVencedor: Jogador {vencedor + 1} com {menor_pontuacao} pontos!")
    return vencedor
