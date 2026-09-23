from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto


def desenha_tela(janela, estado, altura_tela, largura_tela):

    #Todas as variáveis que você precisa para desenhar a tela estão no dicionário "estado" encontrado no arquivo jogo.py.

    # Define as variáveis locais para facilitar a leitura do código
    jogador = estado['pos_jogador']
    mapa = estado['mapa']
    objetos = estado['objetos']
    mensagem = estado['mensagem']
    vidas = estado['vidas']


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


    # Desenha a mensagem na tela, se houver
    if mensagem != '':
        motor.desenha_string(janela, 0, len(mapa) + 3, mensagem, PRETO, BRANCO)


    # Mostra a janela na tela
    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla):

    # Define as variáveis locais para facilitar a leitura do código
    jogador = estado['pos_jogador']
    objetos = estado['objetos']
    vidas = estado['vidas']


    # Limpa a mensagem se o jogador não estiver na mesma posição de nenhum objeto
    estado['mensagem'] = ''  

        
    #Checa se a movimentação requisitada é valida e atualiza a posição do jogador com base na tecla apertada
    if tecla == motor.SETA_ESQUERDA:

        if jogador[0] > 1:  # Verifica se o jogador não está na borda esquerda do mapa
            jogador[0] -= 1

    elif tecla == motor.SETA_DIREITA:

        if jogador[0] < len(estado['mapa'][0]) - 2:  # Verifica se o jogador não está na borda direita do mapa
            jogador[0] += 1

    elif tecla == motor.SETA_CIMA:

        if jogador[1] > 1:  # Verifica se o jogador não está na borda superior do mapa
            jogador[1] -= 1

    elif tecla == motor.SETA_BAIXO:

        if jogador[1] < len(estado['mapa']) - 2:  # Verifica se o jogador não está na borda inferior do mapa
            jogador[1] += 1

    
    # Checa se o jogador está na mesma posição de algum objeto e atualiza a quantidade de vidas do jogador com base no tipo do objeto
    for objeto in objetos:

        if jogador == objeto['posicao']:

            if objeto['tipo'] == CORACAO:

                if vidas < estado['max_vidas']:
                    estado['vidas'] += 1
                    estado['mensagem'] = 'Você ganhou uma vida!'
                    objetos.remove(objeto)  # Remove o coração do mapa após o jogador pegá-lo
                else:
                    objetos.remove(objeto)  # Remove o coração do mapa, mas não aumenta a quantidade de vidas do jogador


            if objeto['tipo'] == ESPINHO:

                if vidas > 1:
                    estado['vidas'] -= 1
                    estado['mensagem'] = 'Você perdeu uma vida!'

                else:
                    estado['tela_atual'] = SAIR


    # Muda o valor da chave 'tela_atual' para mudar de tela
    estado['tela_atual']


    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR