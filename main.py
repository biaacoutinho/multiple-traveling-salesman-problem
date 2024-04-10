import random
import math
import sys
import matplotlib.pyplot as plt
from tkinter import filedialog
import re

def read_file_and_read_coordinates():
    coordinates = []
    file_name = filedialog.askopenfilename()
    if file_name:
        # verifica se o nome do arquivo condiz com o esperdo e utiliza esse metodo para encontrar o numero de caixeiros posteriormente
        match = re.search(r'mTSP-n(\d+)-m(\d+)', file_name)
        if match:
            n_salesman = int(match.group(2))
            file = open(file_name, "r")
            lines = file.readlines()
            n_cities = len(lines)
            for line in lines:
                info = line.split()
                coordinates.append((int(info[1]), int(info[2])))
            return coordinates, n_cities, n_salesman
        else:
            print("Nome de arquivo inválido.")
            return -1
    else:
        print("Nenhum arquivo selecionado.")
        return -1

def calculate_cities_per_salesman(n_salesman, n_cities):
    if n_salesman > 0:
        cities_per_salesman = [0] * n_salesman
        iSalesman = 0
        for _ in range(n_cities - 1): # a cidade inicial não entra no calculo de divisao de cidades por caixeiro, pois todos os caixeiros passam por ela
            cities_per_salesman[iSalesman] += 1
            iSalesman += 1
            if iSalesman >= n_salesman:
                iSalesman = 0
        return cities_per_salesman
    else:
        return 0

def calculate_distances (n_cities, coordinates):
    distances = [[0 for _ in range(n_cities)] for _ in range(n_cities)]

    for i in range(n_cities):
        for j in range(i + 1, n_cities):
            distances[i][j] = distances [j][i] = int(math.sqrt((coordinates[j][0] - coordinates[i][0])**2 + (coordinates[j][1] - coordinates[i][1])**2))

    return distances


def calculate_farthest_city (first_city, distances, unvisited_cities): # retorna o indice da cidade mais distante no vetor de cidades_nao_visitadas
    greatest_distance = -1
    farthest_city = -1

    for i in range(len(unvisited_cities)):
        distance = distances[first_city][unvisited_cities[i]]
        if distance > greatest_distance:
            greatest_distance = distance
            farthest_city = i

    return farthest_city # se retornar -1 é pq não encontrou a cidade mais distante


def calculate_nearest_city (centroid, coordinates, unvisited_cities): # centroide é uma tupla --> coordenada
    shortest_distance = sys.maxsize
    nearest_city = -1

    for i in range(len(unvisited_cities)):
        distance = int(math.sqrt((coordinates[unvisited_cities[i]][0] - centroid[0])**2 + (coordinates[unvisited_cities[i]][1] - centroid[1])**2))

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_city = i 

    return nearest_city # retorna o indice da cidade mais próxima no vetor de cidades_nao_visitadas


def calculate_centroid (tour, coordinates):
    sumX = 0
    sumY = 0

    n_cities = len(tour)

    for i in range(1, n_cities): # a cidade inicial não é usada no cálculo do centroide
        sumX += coordinates[tour[i]][0]
        sumY += coordinates[tour[i]][1]

    centroid = (int(sumX / (n_cities-1)), int(sumY / (n_cities-1)))

    return centroid


def calculate_distance_of_the_tour (distances, tour):
    total_distance = 0

    for i in range(len(tour) - 1):
        total_distance += distances[tour[i]][tour[i+1]]

    total_distance += distances[tour[-1]][tour[0]]

    return total_distance


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
    colors=['r', 'b', 'g', 'y', 'c', 'm']
    iColors = 0

    for tour in tours:
        coordinatesX = []
        coordinatesY = []
        for city in tour:
            x = coordinates[city][0]
            y = coordinates[city][1]
            plt.text(x, y, city, color='red', fontsize=10)
            coordinatesX.append(x)
            coordinatesY.append(y)

        plt.plot(coordinatesX, coordinatesY, colors[iColors], marker='o')
        iColors += 1
        if iColors > 5:
            iColors = 0

    plt.title("Tour")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

def find_tours (first_city, unvisited_cities, coordinates, distances, n_salesman, n_cities):
    total_distance = 0
    tours = []
    for i in range(n_salesman):
        tour = []
        tour.append(first_city)
        farthest_city = calculate_farthest_city(first_city, distances, unvisited_cities)
        tour.append(unvisited_cities.pop(farthest_city))

        for _ in range(qtd_cidades_por_caixeiro[i] - 1): # -1 porque ele já passou pela cidade mais distante
            centroid = calculate_centroid(tour, coordinates)
            nearest_city = calculate_nearest_city(centroid, coordinates, unvisited_cities)
            tour.append(unvisited_cities.pop(nearest_city))

        total_distance += calculate_distance_of_the_tour(distances, tour)
        tour.append(first_city)
        tours.append(tour)

    print("distancia total: ", total_distance)
    
    plot_tour(coordinates, tours)
    
# testes dos métodos já codificados
ret = read_file_and_read_coordinates()
coordinates, n_cities, n_salesman =  ret
if coordinates != -1:
    if n_cities > 0:
        distances = calculate_distances(n_cities, coordinates)
        unvisited_cities = list(range(n_cities))
        first_city = 0
        unvisited_cities.pop(first_city)
        qtd_cidades_por_caixeiro = calculate_cities_per_salesman(n_salesman, n_cities)
        find_tours(first_city, unvisited_cities, coordinates, distances, n_salesman, n_cities)
    else:
        print("distancia total: ", 0)
else:
    print("Nenhum arquivo foi selecionado")