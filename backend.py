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

def validar_jogada (carta, mao_jogador, carta_lider):
    if not naipe_correto (carta_lider, mao_jogador):
        # Se não puder seguir o naipe, qualquer carta é válida (menos na primeira jogada)
        return True
    # Se puder seguir o naipe, verifica se a carta corresponde
    return carta.endswith(carta_lider[-1])
#validar_jogada

def iniciar_rodada (jogadores_cartas):
    #Determinar quem começa a rodada
    primeiro_jogador = encontrar_primeiro_jogador(jogadores_cartas)
    return primeiro_jogador
#iniciar_rodada

def jogar_rodadas(jogadores_cartas, primeiro_jogador, cartas_ganhas_por_jogador, pontos_por_jogador):
    total_cartas = len(jogadores_cartas[0])  # Número de rodadas igual ao número de cartas por jogador

    for rodada in range(total_cartas):
        cartas_jogadas = []  # Lista para armazenar as cartas jogadas na rodada
        jogador_atual = primeiro_jogador
        carta_lider = None  # Inicialmente não há carta líder

        print(f"\n--- Rodada {rodada + 1} ---")
        
        for turno in range(len(jogadores_cartas)):  # Cada jogador joga uma vez por rodada
            mao_jogador = jogadores_cartas[jogador_atual]  # Mão do jogador atual
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
                    
                    if carta_lider and not validar_jogada(carta_jogada, mao_jogador, carta_lider):
                        print("Jogada inválida! Deve seguir o naipe, se possível.")
                        continue
                    
                    # Se a carta for válida, remove-a e avança
                    jogadores_cartas[jogador_atual].remove(carta_jogada)
                    cartas_jogadas.append(carta_jogada)

                    # Define a carta líder se ainda não houver uma
                    if not carta_lider:
                        carta_lider = carta_jogada
                    
                    break  # Sai do loop quando a carta é válida
            
            # Próximo jogador
            jogador_atual = (jogador_atual + 1) % len(jogadores_cartas)

        # Após todos jogarem, determinar o vencedor da rodada
        vencedor = determinar_vencedor_rodada(cartas_jogadas, primeiro_jogador)
        print(f"\nJogador {vencedor + 1} venceu a rodada com a carta: {cartas_jogadas[vencedor]}")

        # Atualizar cartas ganhas e pontos
        cartas_ganhas_por_jogador[vencedor].extend(cartas_jogadas)

        # Configurar o vencedor como o primeiro jogador da próxima rodada
        primeiro_jogador = vencedor

        # Exibir o estado atual
        print("\nEstado atual:")
        for jogador in range(len(cartas_ganhas_por_jogador)):
            print(f"Jogador {jogador + 1}: Cartas ganhas: {cartas_ganhas_por_jogador[jogador]} = {len(cartas_ganhas_por_jogador[jogador])} pontos")


# =========================================================
#                   Finalizar Rodada
# =========================================================

def determinar_vencedor_rodada (cartas_jogadas, primeiro_jogador):

    naipe_lider = cartas_jogadas [0][-1] # Naipe da primeira carta jogada
    maior_carta = cartas_jogadas [0]
    vencedor = primeiro_jogador

    for i, carta in enumerate (cartas_jogadas):
        if carta [-1] == naipe_lider: # Verifica se segue o naipe lider

            if valor_carta(carta) > valor_carta(maior_carta):
                maior_carta = carta
                vencedor = (primeiro_jogador + 1) % len (cartas_jogadas)
    #for
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
    - Atualiza as cartas ♥ ganhas e calcula pontos.
    """
    # Determina o vencedor da rodada
    vencedor = determinar_vencedor_rodada(cartas_jogadas, primeiro_jogador)

    # Adiciona as cartas jogadas ao vencedor
    cartas_ganhas_por_jogador[vencedor].extend(cartas_jogadas)

    # Atualiza as cartas de ♥ apenas
    cartas_coracoes_por_jogador = {
        jogador: [carta for carta in cartas if carta[-1] == '♥']
        for jogador, cartas in cartas_ganhas_por_jogador.items()
    }

    # Calcula os pontos de cada jogador
    pontos_por_jogador = {
        jogador: calcular_pontos(cartas)
        for jogador, cartas in cartas_ganhas_por_jogador.items()
    }

    return vencedor, cartas_ganhas_por_jogador, cartas_coracoes_por_jogador, pontos_por_jogador
