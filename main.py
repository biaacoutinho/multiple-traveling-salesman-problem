import random
import math

qtd_cidades = 10
qtd_caixeiros = 5
qtd_cidades_por_caixeiro = int(qtd_cidades / qtd_caixeiros)


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
    maior_distancia = 0
    cidade_mais_distante = -1

    for i in range(len(coordenadas)):
        distancia = int(math.sqrt((coordenadas[cidades_nao_visitadas[i]][0] - coordenada_cidade_inicial[0])**2 + (coordenadas[cidades_nao_visitadas[i]][1] - coordenada_cidade_inicial[1])**2))

        if distancia > maior_distancia:
            maior_distancia = distancia
            cidade_mais_distante = i

    print("maior distancia: ", maior_distancia)
    return cidade_mais_distante # se retornar -1 é pq não encontrou a cidade mais distante


def encontrar_cidade_mais_proxima (centroide, coordenadas, cidades_nao_visitadas): # centroide é uma tupla --> coordenada
    menor_distancia = 1000000000
    cidade_mais_proxima = -1

    for i in range(len(cidades_nao_visitadas)):
        distancia = int(math.sqrt((coordenadas[cidades_nao_visitadas[i]][0] - centroide[0])**2 + (coordenadas[cidades_nao_visitadas[i]][1] - centroide[1])**2))

    if distancia < menor_distancia:
        menor_distancia = distancia
        cidade_mais_proxima = cidades_nao_visitadas[i]

    return cidade_mais_proxima


def calcular_centroide (coordenadas):
    somaX = 0
    somaY = 0

    qtd_coordenadas = len(coordenadas)

    for i in range(qtd_coordenadas):
        somaX += coordenadas[i][0]
        somaY += coordenadas[i][1]

    centroide = tuple((somaX / qtd_coordenadas), (somaY / qtd_coordenadas))

    return centroide


# testes dos métodos já codificados
coordenadas, distancias = criar_coordenadas_e_calcular_distancias(qtd_cidades)
print("coordenadas: ", coordenadas)
print("distancias: ", distancias)

cidades = list(range(qtd_cidades))
print("cidades: ", cidades)
cidade_inicial = random.choice(cidades)
print("cidade inicial: ", cidade_inicial)
coordenada_cidade_inicial = coordenadas[cidade_inicial - 1]
print("xy cidade inicial: ", coordenada_cidade_inicial)
coordenadas.pop((cidade_inicial - 1))
print("coordenadas sem cid inicial: ", coordenadas)
print("indice cidade mais distante: ", calcular_cidade_mais_distante(coordenada_cidade_inicial, coordenadas, cidades))