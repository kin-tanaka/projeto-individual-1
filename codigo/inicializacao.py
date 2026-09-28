from random import randint # Utilizado para sortear uma posição desocupada
from random import choice # Utilizado para selecionar aleatoriamente uma das opções dos mapas

import os # Utilizado para facilitar navegação entre pastas para acessar as opções de mapas

from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil


# Gera uma posição aleatória desocupada no mapa, ou seja, uma posição que não esteja na lista de posições ocupadas.
def gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa):

    # Checa uma lista de posições ocupadas e devolve uma coordenada que não está ocupada.

    posicao_gerada = False

    while not posicao_gerada:
        x = randint(1, largura_mapa - 2)
        y = randint(1, altura_mapa - 2)
        posicao = [x, y]

        if posicao not in posicoes_ocupadas:
            posicoes_ocupadas.append(posicao)
            posicao_gerada = True
    
    return posicao


# Pega uma série de características de um tipo de objeto e gera uma lista de dicionários que possuem essas características.
def gera_objetos(quantidade, tipo, cor, largura_mapa, altura_mapa, posicoes_ocupadas):

    # Parâmetros:
    # quantidade: quantidade de objetos a serem gerados
    # tipo: tipo do objeto a ser gerado. É uma string como '❤'
    # cor: cor do objeto a ser gerado. É uma lista com três elementos, como [255, 0, 0]
    # largura_mapa: largura do mapa do jogo em caracteres
    # altura_mapa: altura do mapa do jogo em caracteres
    # posicoes_ocupadas: lista de posições ocupadas no mapa. Cada posição é uma lista com exatamente dois elementos: a posição x e a posição y.

    objetos = []

    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
        objetos.append({
            'tipo': tipo,
            'posicao': posicao,
            'cor': cor,
        })

    return objetos


# Pega uma série de características de um tipo de monstro e gera uma lista de dicionários que possuem essas características.
def gera_monstros(quantidade, tipo, cor, vidas, probabilidade_ataque, largura_mapa, altura_mapa, posicoes_ocupadas):

    # Parâmetros:
    # quantidade: quantidade de objetos a serem gerados
    # tipo: tipo de monstro a ser gerado. É uma string com o ícone do monstro.
    # cor: cor do objeto a ser gerado. É uma lista com três elementos, como [255, 0, 0]
    # vidas: número de vidas do monstro
    # probabilidade_ataque: número entre 0 e 1 que representa a chance do monstro atacar
    # largura_mapa: largura do mapa do jogo em caracteres
    # altura_mapa: altura do mapa do jogo em caracteres
    # posicoes_ocupadas: lista de posições ocupadas no mapa. Cada posição é uma lista com exatamente dois elementos: a posição x e a posição y.

    monstros = []
    
    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
        monstros.append({
            'tipo': tipo,
            'posicao': posicao,
            'cor': cor,
            'vidas': vidas,
            'probabilidade_ataque': probabilidade_ataque
        })
    
    return monstros

# Gera uma lista de listas (coordenadas) no formato [x, y] das paredes do mapa
def coordenadas_paredes(mapa):

    # Esta função retorna uma lista de coordenadas (x, y) das paredes do mapa.

    coordenadas = []
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 'X':
                coordenadas.append([j, i])  # Adiciona a coordenada (x, y) da parede à lista
    return coordenadas


# Gera uma lista de listas (coordenadas) no formato [x, y] dos monstros no mapa
def coordenadas_monstros(monstros):

    # Gera uma lista com as coordenadas de todos os monstros

    coordenadas = []
    for monstro in monstros:
        coordenadas.append(monstro['posicao'])
    return coordenadas


# Gera uma lista de listas (coordenadas) no formato [x, y] dos objetos no mapa
def coordenadas_objetos(objetos):

    # Gera uma lista com as coordenadas de todos os objetos

    coordenadas = []
    for objeto in objetos:
        coordenadas.append(objeto['posicao'])
    return coordenadas


# Gera um dicionário que possui todas as características iniciais e essenciais para o jogo. O dicionário é chamado 'estado'
def inicializa_estado():

    # Cria uma lista com os mapas da pasta mapa e seleciona aleatóriamente um dos mapas disponíveis para ser o utilizado
    # Após selecionar, cria uma lista que contenha o mapa como uma matriz

    pasta_mapas = 'mapas'
    arquivos = os.listdir(pasta_mapas)
    mapas = []

    for arquivo in arquivos:
        mapas.append(arquivo)

    mapa_escolhido = choice(mapas)
    caminho_mapa = os.path.join(pasta_mapas, mapa_escolhido)
    
    with open(caminho_mapa, 'r') as arquivo:
        linhas = arquivo.readlines()

        mapa = []

        for linha in linhas:
            linha = linha.strip()
            linha = list(linha)
            mapa.append(linha)

    posicoes_ocupadas = []

    paredes_coordenadas = coordenadas_paredes(mapa)
    for posicao in paredes_coordenadas:
        posicoes_ocupadas.append(posicao)

    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
    
    # Você pode colocar o jogador em outro lugar, se preferir
    pos_jogador = [largura_mapa//2, altura_mapa//2]  # Meio do mapa
    posicoes_ocupadas.append(pos_jogador)
    
    # Cria objetos do mapa
    objetos = []
    objetos += gera_objetos(8, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(6, ESPINHO, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas)

    objetos_coordenadas = coordenadas_objetos(objetos)

    # Cria monstros no mapa
    monstros = []
    monstros += gera_monstros(3, MONSTRO_1, ROXO, 5, 0.3, largura_mapa, altura_mapa, posicoes_ocupadas) # Mais vidas e mais agressivos
    monstros += gera_monstros(3, MONSTRO_2, BRANCO, 3, 0.5, largura_mapa, altura_mapa, posicoes_ocupadas) # Menos vidas e muito agressivos
    monstros += gera_monstros(3, MONSTRO_3, AZUL, 2, 0.1, largura_mapa, altura_mapa, posicoes_ocupadas) # Menos vidas e menos agressivos

    monstros_coordenadas = coordenadas_monstros(monstros)
    
    return {
        'tela_atual': TELA_JOGO,
        'pos_jogador': pos_jogador,
        'vidas': 2,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos, # Lista de dicionários que possuem as características de cada objeto.
        'objetos_coordenadas': objetos_coordenadas, # Lista de listas que representam as coordenadas de todos os objetos. 
        'mensagem': '',  # Use esta mensagem para mostrar mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
        'mapa': mapa, # Mapa selecionado
        'paredes_coordenadas': paredes_coordenadas,  # Adiciona a lista de coordenadas das paredes ao estado do jogo
        'monstros': monstros, # Lista de dicionários que possuem as características de cada monstro.
        'monstros_coordenadas': monstros_coordenadas # Lista de listas que representam as coordenadas de todos os monstros. É atualizada no futuro
    }