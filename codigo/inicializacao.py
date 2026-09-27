from random import randint
from random import choice

import os

from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código



# Gera uma posição aleatória desocupada no mapa, ou seja, uma posição que não esteja na lista de posições ocupadas.

def gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa):

    posicao_gerada = False

    while not posicao_gerada:
        x = randint(1, largura_mapa - 2)
        y = randint(1, altura_mapa - 2)
        posicao = [x, y]

        if posicao not in posicoes_ocupadas:
            posicoes_ocupadas.append(posicao)
            posicao_gerada = True
    
    return posicao


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


def gera_monstros(quantidade, tipo, cor, vidas, probabilidade_ataque, largura_mapa, altura_mapa, posicoes_ocupadas):


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


def coordenadas_paredes(mapa):

    # Esta função retorna uma lista de coordenadas (x, y) das paredes do mapa.
    coordenadas = []
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == 'X':
                coordenadas.append([j, i])  # Adiciona a coordenada (x, y) da parede à lista
    return coordenadas


def coordenadas_monstros(monstros):

    coordenadas = []
    for monstro in monstros:
        coordenadas.append(monstro['posicao'])
    return coordenadas


def coordenadas_objetos(objetos):

    coordenadas = []
    for objeto in objetos:
        coordenadas.append(objeto['posicao'])
    return coordenadas


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
    
    # Cria outros objetos do mapa
    objetos = []
    objetos += gera_objetos(8, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(6, ESPINHO, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas)

    objetos_coordenadas = coordenadas_objetos(objetos)

    #Cria monstros no mapa
    monstros = []
    monstros += gera_monstros(4, MONSTRO, ROXO, 5, 0.3, largura_mapa, altura_mapa, posicoes_ocupadas)

    monstros_coordenadas = coordenadas_monstros(monstros)
    
    return {
        'tela_atual': TELA_JOGO,
        'pos_jogador': pos_jogador,
        'vidas': 2,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos,
        'objetos_coordenadas': objetos_coordenadas,
        'mensagem': '',  # Use esta mensagem para mostrar mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
        'mapa': mapa,
        'paredes_coordenadas': paredes_coordenadas,  # Adiciona a lista de coordenadas das paredes ao estado do jogo
        'monstros': monstros, 
        'monstros_coordenadas': monstros_coordenadas
    }