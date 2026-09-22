from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto


def desenha_tela(janela, estado, altura_tela, largura_tela):

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
        motor.desenha_string(janela, 0, len(mapa), vidas_totais, PRETO, BRANCO)
    else:
        vidas_totais = (CORACAO + ' ') * 5
        motor.desenha_string(janela, 0, len(mapa), vidas_totais, PRETO, BRANCO)


    # Desenha o jogador e os objetos na tela
    motor.desenha_string(janela, jogador[0] + x_central_mapa, jogador[1] + y_central_mapa, JOGADOR, VERDE_ESCURO, AZUL) 

    for objeto in objetos:
        motor.desenha_string(janela, objeto['posicao'][0] + x_central_mapa, objeto['posicao'][1] + y_central_mapa, objeto['tipo'], VERDE_ESCURO, objeto['cor'])


    # Desenha a mensagem na tela, se houver
    if mensagem != '':
        motor.desenha_string(janela, 0, len(mapa) + 3, mensagem, PRETO, BRANCO)


    # Mostra a janela na tela
    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla):
    # O seu código deve atualizar o dicionário "estado" com base na tecla apertada pelo jogador
    # Por exemplo, se o jogador apertar a seta para a esquerda (o valor da variável será "ESQUERDA"), 
    # o seu código deve atualizar o dicionário estado['pos_jogador'][0] -= 1

    # Mude o valor da chave 'tela_atual' para mudar de tela
    
    # Começamos apagando a mensagem anterior, pois ela já foi mostrada no frame anterior
    estado['mensagem'] = ''

    # Escreva seu código para atualizar o dicionário "estado" com base na tecla apertada pelo jogador aqui
    # APAGUE ESTA LINHA E ESCREVA SEU CÓDIGO AQUI

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR