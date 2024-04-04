import random
import math
import sys
import matplotlib.pyplot as plt

qtd_cidades = 13
qtd_caixeiros = 1

coordenadas = [(500, 500), (708, 500), (707, 977), (43, 228), (140, 11), (899, 625), (389, 990), (205, 603), (878, 977), (24, 237), (218, 557), (362, 217), (504, 939)]



def definir_qtd_cidades_por_caixeiro():
    if qtd_caixeiros > 0:
        cidades_por_caixeiro = [0] * qtd_caixeiros
        iCaixeiros = 0
        for _ in range(qtd_cidades - 1): # a cidade inicial não entra no calculo de divisao de cidades por caixeiro, pois todos os caixeiros passam por ela
            cidades_por_caixeiro[iCaixeiros] += 1
            iCaixeiros += 1
            if iCaixeiros >= qtd_caixeiros:
                iCaixeiros = 0
        return cidades_por_caixeiro
    else:
        return 0

def calcular_distancias (qtd_cidades, coordenadas):
    distancias = [[0 for _ in range(qtd_cidades)] for _ in range(qtd_cidades)]

    for i in range(qtd_cidades):
        for j in range(i + 1, qtd_cidades):
            distancias[i][j] = distancias [j][i] = int(math.sqrt((coordenadas[j][0] - coordenadas[i][0])**2 + (coordenadas[j][1] - coordenadas[i][1])**2))

    return distancias


def calcular_cidade_mais_distante (cidade_inicial, distancias, cidades_nao_visitadas): # retorna o indice da cidade mais distante no vetor de cidades_nao_visitadas
    maior_distancia = -1
    cidade_mais_distante = -1

    for i in range(len(cidades_nao_visitadas)):
        distancia = distancias[cidade_inicial][cidades_nao_visitadas[i]]
        if distancia > maior_distancia:
            maior_distancia = distancia
            cidade_mais_distante = i

    return cidade_mais_distante # se retornar -1 é pq não encontrou a cidade mais distante


def encontrar_cidade_mais_proxima (centroide, coordenadas, cidades_nao_visitadas): # centroide é uma tupla --> coordenada
    menor_distancia = sys.maxsize
    cidade_mais_proxima = -1
    for i in range(len(cidades_nao_visitadas)):
        distancia = int(math.sqrt((coordenadas[cidades_nao_visitadas[i]][0] - centroide[0])**2 + (coordenadas[cidades_nao_visitadas[i]][1] - centroide[1])**2))

        if distancia < menor_distancia:
            menor_distancia = distancia
            cidade_mais_proxima = i 

    return cidade_mais_proxima # retorna o indice da cidade mais próxima no vetor de cidades_nao_visitadas


def calcular_centroide (caminho, coordenadas):
    somaX = 0
    somaY = 0

    qtd_cidades = len(caminho)

    for i in range(1, qtd_cidades): # a cidade inicial não é usada no cálculo do centroide
        somaX += coordenadas[caminho[i]][0]
        somaY += coordenadas[caminho[i]][1]

    centroide = (int(somaX / (qtd_cidades-1)), int(somaY / (qtd_cidades-1)))

    return centroide


def calcular_distancia_caminho (distancias, caminho):
    distancia_total = 0

    for i in range(len(caminho) - 1):
        distancia_total += distancias[caminho[i]][caminho[i+1]]

    distancia_total += distancias[caminho[-1]][caminho[0]]

    return distancia_total


def generate_lines(coordinates, tour):
    lines = list()

    for j in range(len(tour) - 1):
        lines.append([
            coordinates[tour[j]],
            coordinates[tour[j + 1]]
        ])

    lines.append([
        coordinates[tour[-1]], 
        coordinates[tour[0]]
    ])

    return lines

def plot_tour(coordinates, tours):
    plt.clf()
    cores=['r', 'b', 'g', 'y', 'c', 'm']
    iCores = 0

    for tour in tours:
        coordenadasX = []
        coordenadasY = []
        for city in tour:
            x = coordinates[city][0]
            y = coordinates[city][1]
            plt.text(x, y, city, color='red', fontsize=10)
            coordenadasX.append(x)
            coordenadasY.append(y)

        plt.plot(coordenadasX, coordenadasY, cores[iCores], marker='o')
        iCores += 1
        if iCores > 5:
            iCores = 0

    plt.title("Tour")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def achar_caminhos (cidade_inicial, cidades_nao_visitadas, coordenadas, distancias):

    distancia_total = 0
    caminhos = []
    for i in range(qtd_caixeiros):
        caminho = []
        caminho.append(cidade_inicial)
        cidade_mais_distante = calcular_cidade_mais_distante(cidade_inicial, distancias, cidades_nao_visitadas)
        caminho.append(cidades_nao_visitadas.pop(cidade_mais_distante))

        for _ in range(qtd_cidades_por_caixeiro[i] - 1): # -1 porque ele já passou pela cidade mais distante
            centroide = calcular_centroide(caminho, coordenadas)
            cidade_mais_proxima = encontrar_cidade_mais_proxima(centroide, coordenadas, cidades_nao_visitadas)
            caminho.append(cidades_nao_visitadas.pop(cidade_mais_proxima))

        distancia_total += calcular_distancia_caminho(distancias, caminho)
        caminho.append(cidade_inicial)
        caminhos.append(caminho)

    print("distancia total: ", distancia_total)
    
    plot_tour(coordenadas, caminhos)
    

# testes dos métodos já codificados
if qtd_cidades > 0:
    distancias = calcular_distancias(qtd_cidades, coordenadas)
    cidades_nao_visitadas = list(range(qtd_cidades))
    cidade_inicial = 0
    cidades_nao_visitadas.pop(cidade_inicial)
    qtd_cidades_por_caixeiro = definir_qtd_cidades_por_caixeiro()
    achar_caminhos(cidade_inicial, cidades_nao_visitadas, coordenadas, distancias)
else:
    print("distancia total: ", 0)