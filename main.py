import random
import math
import sys
import matplotlib.collections as mc
import matplotlib.pylab as pl

qtd_cidades = 21
qtd_caixeiros = 6

def definir_qtd_cidades_por_caixeiro():
    cidades_por_caixeiro = [0] * qtd_caixeiros
    iCaixeiros = 0
    for _ in range(qtd_cidades - 1): # a cidade inicial não entra no calculo de divisao de cidades por caixeiro, pois todos os caixeiros passam por ela
        cidades_por_caixeiro[iCaixeiros] += 1
        iCaixeiros += 1
        if iCaixeiros >= qtd_caixeiros:
            iCaixeiros = 0


    return cidades_por_caixeiro

def criar_coordenadas_e_calcular_distancias (qtd_cidades):
    coordenadas = []
    for _ in range(qtd_cidades):
        coordenadas.append((int(random.uniform(0, 100)), int(random.uniform(0, 100))))

    distancias = [[0 for _ in range(qtd_cidades)] for _ in range(qtd_cidades)]

    for i in range(qtd_cidades):
        for j in range(i + 1, qtd_cidades):
            distancias[i][j] = distancias [j][i] = int(math.sqrt((coordenadas[j][0] - coordenadas[i][0])**2 + (coordenadas[j][1] - coordenadas[i][1])**2))

    return coordenadas, distancias


def calcular_cidade_mais_distante (coordenada_cidade_inicial, coordenadas, cidades_nao_visitadas): # retorna o indice da cidade mais distante
    maior_distancia = -1
    cidade_mais_distante = -1

    for i in range(len(cidades_nao_visitadas)):
        distancia = int(math.sqrt((coordenadas[cidades_nao_visitadas[i]][0] - coordenada_cidade_inicial[0])**2 + (coordenadas[cidades_nao_visitadas[i]][1] - coordenada_cidade_inicial[1])**2))

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

    return cidade_mais_proxima # retorna o indice da cidade no vetor de cidades_nao_visitadas


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

def plot_tour(coordinates, tour):
    lc = mc.LineCollection(generate_lines(coordinates, tour), linewidths = 2)

    fig, ax = pl.subplots() # cria como se fosse uma tela em branco
    ax.add_collection(lc)
    ax.autoscale() # ajusta a "folha" para caber o desenho que será feito
    ax.margins(0.1)

    coordinatesX = []
    coordinatesY = []
    j = 0
    for i in coordinates:
        coordinatesX.append(i[0])
        coordinatesY.append(i[1])
        pl.text(i[0], i[1], str(j), color='red', fontsize=10)
        j += 1
    
    pl.scatter(coordinatesX, coordinatesY)
    pl.title("Tour")
    pl.xlabel("X")
    pl.ylabel("Y")
    pl.show()

def achar_caminhos (cidade_inicial, cidades_nao_visitadas, coordenadas, distancias):

    distancia_total = 0
    caminhos = []
    for i in range(qtd_caixeiros):
        caminho = []
        caminho.append(cidade_inicial)
        cidade_mais_distante = calcular_cidade_mais_distante(coordenadas[cidade_inicial], coordenadas, cidades_nao_visitadas)
        caminho.append(cidades_nao_visitadas.pop(cidade_mais_distante))

        for _ in range(qtd_cidades_por_caixeiro[i] - 1): # -1 porque ele já passou pela cidade mais distante
            centroide = calcular_centroide(caminho, coordenadas)
            cidade_mais_proxima = encontrar_cidade_mais_proxima(centroide, coordenadas, cidades_nao_visitadas) # encontrar_cidade_mais_proxima() retoan o número da cidade, nao o índice no vetor de cidades
            print("cidade mais proxima: ", cidades_nao_visitadas[cidade_mais_proxima])
            if cidade_mais_proxima >= 0: # se cidade_mais_proxima retornar -1 significa que não há mais cidades_nao_visitadas
                a = cidades_nao_visitadas.pop(cidade_mais_proxima)
                caminho.append(a)
                print("caminho: ", caminho)
                print("sem 1")

        distancia_total += calcular_distancia_caminho(distancias, caminho)
        caminhos.extend(caminho)

    caminhos.append(cidade_inicial)
    print("caminhos: ", caminhos)
    plot_tour(coordenadas, caminhos)
    print("distancia total: ", distancia_total)


# testes dos métodos já codificados
coordenadas, distancias = criar_coordenadas_e_calcular_distancias(qtd_cidades)
print("coordenadas: ", coordenadas)
print("distancias: ", distancias)

cidades = list(range(qtd_cidades))
print("cidades: ", cidades)
cidade_inicial = 3 #random.choice(cidades)
print("cidade inicial: ", cidade_inicial)
coordenada_cidade_inicial = coordenadas[cidade_inicial - 1]
print("xy cidade inicial: ", coordenada_cidade_inicial)
cidades.pop(cidade_inicial)
print("coordenadas sem cid inicial: ", coordenadas)
print("indice cidade mais distante: ", calcular_cidade_mais_distante(coordenada_cidade_inicial, coordenadas, cidades))
qtd_cidades_por_caixeiro = definir_qtd_cidades_por_caixeiro
achar_caminhos(cidade_inicial, cidades, coordenadas, distancias)

dist = 0
dist += calcular_distancia_caminho(distancias, [3, 0, 1])
dist += calcular_distancia_caminho(distancias, [3, 2, 4])
print("dist: ", dist)

print("cid por cai: ", definir_qtd_cidades_por_caixeiro())