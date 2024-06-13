import math
import random
from tqdm import tqdm
from tkinter import filedialog
import matplotlib.pyplot as plt
import re
import time

def read_file_and_read_coordinates():
    coordinates = []
    file_name = filedialog.askopenfilename()
    if file_name:
        # verifica se o nome do arquivo condiz com o esperdo e utiliza esse metodo para encontrar o numero de caixeiros posteriormente
        match = re.search(r'mTSP-n(\d+)-m(\d+)', file_name) # primeiro parâmetro é o esperado e o segundo é o nome do arquivo selecionado pelo usuário
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

def split_tour(individual, cities_per_salesman): # individual é um vetor com as rotas de todos os caixeiros juntas
    total_tour = []
    for num_cities in cities_per_salesman:
        tour = [0]
        tour.extend(individual[:num_cities - 1])
        tour.append(0)
        total_tour.append(tour)
        individual = individual[num_cities - 1:]

    return total_tour

def calculate_distances (n_cities, coordinates):
    distances = [[0 for _ in range(n_cities)] for _ in range(n_cities)]

    for i in range(n_cities):
        for j in range(i + 1, n_cities):
            distances[i][j] = distances [j][i] = int(math.sqrt((coordinates[j][0] - coordinates[i][0])**2 + (coordinates[j][1] - coordinates[i][1])**2))

    return distances

def calculate_distance_of_the_tour (distances, tour):
    total_distance = 0

    for i in range(len(tour) - 1):
        total_distance += distances[tour[i]][tour[i+1]]

    total_distance += distances[tour[-1]][tour[0]]

    return total_distance

def calculate_fitness_of_an_individual (distances, individual, cities_per_salesman):
    total_distance = 0

    divided_into_tours = split_tour(individual, cities_per_salesman)

    for tour in divided_into_tours:
        total_distance += calculate_distance_of_the_tour(distances, tour)

    return total_distance

def initialize_population(pop_size, n_cities):
    population = []
    for _ in range(pop_size):
        individual = list(range(n_cities))
        individual.pop(0) # a cidade 0 é comum a todos os caixeiros
        
        random.shuffle(individual) # embaralha os elementos do vetor para criar rotas aleatorias para os caixeiros

        population.append(individual)
    
    return population

def binary_tournament_selection(population, pop_size, distances, cities_per_salesman):
    """ 
        1.Select k individuals from the population and perform a tournament amongst them
        2.Select the best individual from the k individuals
        3. Repeat process 1 and 2 until you have the desired amount of population
    """

    selected_parents = []
    number_of_selected_individuals = pop_size//2 # 50% da população será escolhida de forma aleatoria para ocorrer o torneio

    # são selecionados o dobro de 80% do número de individuos --> dobro pois cada pai gera um filho e 80% da pop será formada por filhos
    for _ in range(int(pop_size * 2 * 0.9)): 
        # 1.Select k individuals from the population and perform a tournament amongst them
        selected_individuals = random.sample(population, number_of_selected_individuals) # seleciona um determinado numero de individuos dentro da populacao

        # 2.Select the best individual from the k individuals --> necessario selecionar 2 individuos (os com menores distancias) para fazer o crossover
        distances_of_tours = []
        for individual in selected_individuals:
            distances_of_tours.append(calculate_fitness_of_an_individual(distances, individual, cities_per_salesman))
        
        first_min_distance = min(distances_of_tours)
        index_of_first_min_distance = distances_of_tours.index(first_min_distance) # também representa o indice do individuo com a menor distancia (indice do vetor selected_individuals)
        distances_of_tours.remove(first_min_distance)

        second_min_distance = min(distances_of_tours)
        index_of_second_min_distance = distances_of_tours.index(second_min_distance) # também representa o indice do individuo com a segunda menor distancia (indice do vetor selected_individuals)
        distances_of_tours.remove(second_min_distance)

        parent_1 = selected_individuals[index_of_first_min_distance]
        parent_2 = selected_individuals[index_of_second_min_distance]

        selected_parents.append((parent_1, parent_2))

    return selected_parents

def crossover (parents, n_cities):
    '''
        1. Select a substring from a parent at random.
        2. Produce a proto-child by copying the substring into the corresponding position of it.
        3. Delete the cities which are already in the substring from the 2nd parent. The resulted sequence of citires contains the cities that the proto-child needs.
        4. Place the cities into the unfixed positions of the proto-child from left to right according to the order of the sequence to produce an offspring.    
    '''
    offspring = [-1] * n_cities

    num_selected_cities = (n_cities - 1) // 2 # -1 pois a cidade 0 nao contra e dividido por 2 para que tenha aproximadamente metade de cada pai
    start_of_selection = random.randint(0, n_cities - 1 - num_selected_cities) # a selecao de cidades pode ir ate num_selected_cities antes de terminar o vetor, senão serão selecionadas cidades fora do vetor, com índices superiores ao do último elemento
    cities_of_first_parent = parents[0][start_of_selection : start_of_selection + num_selected_cities]
    offspring[start_of_selection : start_of_selection + num_selected_cities] = cities_of_first_parent

    second_parent = parents[1]
    for city in second_parent:
        if not city in offspring:
            i = offspring.index(-1) # encontra a posição do primeiro elemento vazio
            offspring[i] = city 

    return offspring

def mutation(individual, n_cities):
    num_mutate_cities = (n_cities - 1) // 2 
    start_of_mutation = random.randint(0, n_cities - 1 - num_mutate_cities) 
    mutate_cities = individual[start_of_mutation : start_of_mutation + num_mutate_cities]
    random.shuffle(mutate_cities)
    individual[start_of_mutation : start_of_mutation + num_mutate_cities] = mutate_cities

    return individual

def order_by_fitness(population, distances, cities_per_salesman):
    population.sort(key= lambda individual : calculate_fitness_of_an_individual(distances, individual, cities_per_salesman))
    return population

def select_elite(population, pop_size):
    elite = []
    for _ in range(int(pop_size * 0.1)):
        elite.append(population.pop())

    return elite
    

def create_new_generation(population, population_size, distances, cities_per_salesman, n_cities):
    ord_population = order_by_fitness(population, distances, cities_per_salesman)

    # 20% da nova população será composta pela elite da geração atual
    new_population = select_elite(ord_population, population_size)

    selected_parents = binary_tournament_selection(population, population_size, distances, cities_per_salesman)

    for parents in selected_parents:
        offspring = crossover(parents, n_cities)
        num = random.random()
        if num >= 0.5:
            new_population.append(mutation(offspring, n_cities))
        else:
            new_population.append(offspring)

    return new_population

    '''
        - 20% da população --> elite | 80% crossover --> aleatoriedade para haver mutação
        - fazer selecao (✓)
        - aplicar crossing over nos selecionados para gerar os filhos (✓)
        - aplicar mutacao aleatoria (✓)
        - adicionar na população os filhos gerados e mutados (✓)
    '''

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

def plot_tour(coordinates, individuo, cities_per_salesman):
    plt.clf()
    colors=['r', 'b', 'g', 'y', 'c', 'm']
    iColors = 0

    tours = split_tour(individuo, cities_per_salesman)

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

coordinates, n_cities, n_salesman = read_file_and_read_coordinates()

distances = calculate_distances(n_cities, coordinates)
cities_per_salesman = calculate_cities_per_salesman(n_salesman, n_cities)
population_size = 100
time_vector = []
population = initialize_population(population_size, n_cities)
for _ in range(100):
    for _ in tqdm(range(3000)):
        population = create_new_generation(population, population_size, distances, cities_per_salesman, n_cities)

    individual = order_by_fitness(population, distances, cities_per_salesman)[0]
    distance = calculate_fitness_of_an_individual(distances, individual, cities_per_salesman)
    inicio = time.time()
    target_genetic_algorithm(population_size, n_generations, n_cities, n_salesman, coordinates, target)
    fim = time.time()
    time_vector.append(fim - inicio)

    time_vector.sort()

print(distance)
