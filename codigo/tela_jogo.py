from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto
import random


def desenha_paredes(mapa):
    # Esta função substitui os caracteres 'X' do mapa por paredes (PAREDE) e os caracteres '_' por espaços em branco (' ').

    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 'X':
                mapa[i][j] = PAREDE
            elif mapa[i][j] == '_':
                mapa[i][j] = ' '

    return mapa


def desenha_tela(janela, estado, altura_tela, largura_tela):

    #Todas as variáveis que você precisa para desenhar a tela estão no dicionário "estado" encontrado no arquivo jogo.py.

    # Define as variáveis locais para facilitar a leitura do código
    jogador = estado['pos_jogador']
    mapa = estado['mapa']
    objetos = estado['objetos']
    mensagem = estado['mensagem']
    vidas = estado['vidas']
    mapa = estado['mapa']
    monstros = estado['monstros']


    # Desenha as paredes do mapa.
    mapa = desenha_paredes(mapa)

    # Calcula a posição central do mapa na tela
    x_central_mapa = (largura_tela - len(mapa[0])) // 2
    y_central_mapa = (altura_tela - len(mapa)) // 2


    # Desenha o fundo da tela e as dimensões do mapa do jogo
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)

    motor.preenche_fundo(janela, PRETO)


    # Desenha o mapa na tela
    for y in range(altura_mapa):
        for x in range(largura_mapa):
            if mapa[y][x] == PAREDE:
                motor.desenha_string(janela, x + x_central_mapa, y + y_central_mapa, mapa[y][x], MARROM_ESCURO, MARROM_MAIS_ESCURO)
            else:
                motor.desenha_string(janela, x + x_central_mapa, y + y_central_mapa, mapa[y][x], VERDE_ESCURO, PRETO)


    # Desenha as vidas do jogador na tela, usando o símbolo de coração
    
    
    if vidas < 5:
        vidas__vermelhas = (CORACAO + ' ') * vidas
        vidas__cinzas = ('🤍') * (5 - vidas)

        vidas_totais = vidas__vermelhas + vidas__cinzas
        motor.desenha_string(janela, 0, 0, vidas_totais, PRETO, BRANCO)
    else:
        vidas_totais = (CORACAO + ' ') * 5
        motor.desenha_string(janela, 0, 0, vidas_totais, PRETO, BRANCO)


    # Desenha o jogador e os objetos na tela
    for objeto in objetos:
        motor.desenha_string(janela, objeto['posicao'][0] + x_central_mapa, objeto['posicao'][1] + y_central_mapa, objeto['tipo'], VERDE_ESCURO, objeto['cor'])

    motor.desenha_string(janela, jogador[0] + x_central_mapa, jogador[1] + y_central_mapa, JOGADOR, VERDE_ESCURO, AZUL) 


    # Desenha os monstros na tela
    for monstro in monstros:
        motor.desenha_string(janela, monstro['posicao'][0] + x_central_mapa, monstro['posicao'][1] + y_central_mapa, monstro['tipo'], VERDE_ESCURO, monstro['cor'])

    # Desenha a mensagem na tela, se houver
    if mensagem != '':
        motor.desenha_string(janela, 0, len(mapa) + 10, mensagem, PRETO, BRANCO)


    # Mostra a janela na tela
    motor.mostra_janela(janela)


def checa_movimento(jogador, paredes, tecla):
    # Esta função verifica se o movimento do jogador é válido, ou seja, se ele não está tentando atravessar uma parede.
    # Retorna True se o movimento for válido e False caso contrário.

    if tecla == motor.SETA_ESQUERDA:
        return [jogador[0] - 1, jogador[1]] not in paredes
    elif tecla == motor.SETA_DIREITA:
        return [jogador[0] + 1, jogador[1]] not in paredes
    elif tecla == motor.SETA_CIMA:
        return [jogador[0], jogador[1] - 1] not in paredes
    elif tecla == motor.SETA_BAIXO:
        return [jogador[0], jogador[1] + 1] not in paredes
    else:
        return False


def interacao_objetos(jogador, objetos, vidas, estado):
    # Esta função verifica se o jogador está na mesma posição de algum objeto e atualiza a quantidade de vidas do jogador com base no tipo do objeto.
    # Retorna a quantidade de vidas atualizada.

    for objeto in objetos:
        if jogador == objeto['posicao']:
            if objeto['tipo'] == CORACAO:
                if vidas < estado['max_vidas']:
                    vidas += 1
                    estado['mensagem'] = 'Você ganhou uma vida!'
                    objetos.remove(objeto)  # Remove o coração do mapa após o jogador pegá-lo
                else:
                    objetos.remove(objeto)  # Remove o coração do mapa, mas não aumenta a quantidade de vidas do jogador

            elif objeto['tipo'] == ESPINHO:
                if vidas > 1:
                    vidas -= 1
                    estado['mensagem'] = 'Você perdeu uma vida!'
                else:
                    estado['tela_atual'] = SAIR

    return vidas


def interacao_monstros(jogador, monstros, monstros_coordenadas, vidas, estado):

    # Esta função verifica se o jogador está na mesma posição de algum monstro e atualiza a quantidade de vidas do jogador com base no resultado do encontro.
    # Retorna a quantidade de vidas atualizada.

    for monstro in monstros:
        probabilidade_ataque = monstro['probabilidade_ataque']
        resultado_ataque = random.random() < probabilidade_ataque  # Retorna True se random.random() retornar um valor menor que a probabilidade de ataque do monstro.

        if jogador == monstro['posicao']:
            if resultado_ataque:
                if vidas > 1:
                    vidas -= 1
                    estado['mensagem'] = 'Você foi atacado! Perdeu uma vida.'
                else:
                    estado['tela_atual'] = SAIR
            else:
                if monstro['vidas'] > 1:
                    monstro['vidas'] -= 1
                    estado['mensagem'] = 'Você atacou o monstro! Ele perdeu uma vida.'
                else:
                    estado['mensagem'] = 'Você derrotou o monstro!'
                    monstros.remove(monstro) # Remove o monstro do mapa após o jogador derrotá-lo
                    monstros_coordenadas.remove(monstro['posicao']) # Remove a posição do monstro da lista de coordenadas dos monstros

    return vidas


def atualiza_estado(estado, tecla):

    # Define as variáveis locais para facilitar a leitura do código
    jogador = estado['pos_jogador']
    objetos = estado['objetos']
    vidas = estado['vidas']
    paredes = estado['paredes']
    monstros = estado['monstros']
    monstros_coordenadas = estado['monstros_coordenadas']



    # Limpa a mensagem se o jogador não estiver na mesma posição de nenhum objeto
    estado['mensagem'] = ''


    # Checa se o jogador está tentando atravessar uma parede. Se sim, impede o movimento, se não
    # Checa se o jogador está tentando atravessar um monstro. Se sim, impede e tem interação com o monstro, se não
    # Checa se o jogador está interagindo com o objeto e qual, fazendo a devida alteração na vida.

    if tecla == motor.SETA_ESQUERDA:
        nova_posicao = [jogador[0] - 1, jogador[1]]

        if checa_movimento(jogador, paredes, tecla):

            if nova_posicao not in monstros_coordenadas:

                jogador[0] -= 1

                estado['vidas'] = interacao_objetos(jogador, objetos, vidas, estado)

            else:
                estado['vidas'] = interacao_monstros(nova_posicao, monstros, monstros_coordenadas, vidas, estado)

        else:
            estado['mensagem'] = 'Não pode atravessar paredes!'  # Mensagem exibida se o jogador tentar atravessar uma parede

    elif tecla == motor.SETA_DIREITA:
        nova_posicao = [jogador[0] + 1, jogador[1]]

        if checa_movimento(jogador, paredes, tecla):
        
                    if nova_posicao not in monstros_coordenadas:

                        jogador[0] += 1
        
                        estado['vidas'] = interacao_objetos(jogador, objetos, vidas, estado)
        
                    else:
                        estado['vidas'] = interacao_monstros(nova_posicao, monstros, monstros_coordenadas, vidas, estado)

        else:
            estado['mensagem'] = 'Não pode atravessar paredes!'  # Mensagem exibida se o jogador tentar atravessar uma parede
            
    elif tecla == motor.SETA_CIMA:
        nova_posicao = [jogador[0], jogador[1] - 1]

        if checa_movimento(jogador, paredes, tecla):
        
                    if nova_posicao not in monstros_coordenadas:

                        jogador[1] -= 1
        
                        estado['vidas'] = interacao_objetos(jogador, objetos, vidas, estado)
        
                    else:
                        estado['vidas'] = interacao_monstros(nova_posicao, monstros, monstros_coordenadas, vidas, estado)

        else:
            estado['mensagem'] = 'Não pode atravessar paredes!'  # Mensagem exibida se o jogador tentar atravessar uma parede

    elif tecla == motor.SETA_BAIXO:
        nova_posicao = [jogador[0], jogador[1] + 1]

        if checa_movimento(jogador, paredes, tecla):
        
                    if nova_posicao not in monstros_coordenadas:

                        jogador[1] += 1
        
                        estado['vidas'] = interacao_objetos(jogador, objetos, vidas, estado)
        
                    else:
                        estado['vidas'] = interacao_monstros(nova_posicao, monstros, monstros_coordenadas, vidas, estado)

        else:
            estado['mensagem'] = 'Não pode atravessar paredes!'  # Mensagem exibida se o jogador tentar atravessar uma parede

    elif tecla == motor.ESCAPE:
        estado['tela_atual'] = SAIR


    # Muda o valor da chave 'tela_atual' para mudar de tela
    estado['tela_atual']


    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR