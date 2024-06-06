import math
import random

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
        tour = individual[:num_cities]
        total_tour.append(tour)
        individual = individual[num_cities:]

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

def calculate_distance_of_an_individual (distances, individual, cities_per_salesman):
    total_distance = 0

    divided_into_tours = split_tour(individual, cities_per_salesman)

    for tour in divided_into_tours:
        total_distance += calculate_distance_of_the_tour(distances, tour)

    return total_distance

def calculate_fitness (population, distances):
    population_costs = []
    for individual in population:
        distance = calculate_distance_of_an_individual(distances, individual)
        fitness = 1 / distance   
        population_costs.append(fitness) 

    return population_costs

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
    number_of_selected_individuals = pop_size/4

    for _ in range(pop_size/2):
        # 1.Select k individuals from the population and perform a tournament amongst them
        selected_individuals = random.sample(population, number_of_selected_individuals) # seleciona um determinado numero de individuos dentro da populacao

        # 2.Select the best individual from the k individuals --> necessario selecionar 2 individuos (os com menores distancias) para fazer o crossover
        distances_of_tours = []
        for individual in selected_individuals:
            distances_of_tours.append(calculate_distance_of_an_individual(distances, individual, cities_per_salesman))
        
        first_min_distance = min(distances_of_tours)
        index_of_first_min_distance = distances_of_tours.index(first_min_distance) # também representa o indice do individuo com a menor distancia (indice do vetor selected_individuals)
        distances_of_tours.remove(first_min_distance)

        second_min_distance = min(distances_of_tours)
        index_of_second_min_distance = distances_of_tours.index(second_min_distance) # também representa o indice do individuo com a segunda menor distancia (indice do vetor selected_individuals)
        distances_of_tours.remove(second_min_distance)

        parent_1 = selected_individuals[index_of_first_min_distance]
        parent_2 = selected_individuals[index_of_second_min_distance]

        selected_parents.append(parent_1, parent_2)

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
    start_of_selection = random.randint(0, n_cities - 1 - num_selected_cities) # a selecao de cidades pode ir atenum_selected_cities antes de terminar o vetor, senão serão selecionadas cidades fora do vetor, com índices superiores ao do último elemento
    cities_of_first_parent = parents[0][start_of_selection : start_of_selection + num_selected_cities]
    offspring[start_of_selection : start_of_selection + num_selected_cities] = cities_of_first_parent

    second_parent = parents[1]
    for city in second_parent:
        if not city in offspring:
            i = offspring.index(-1) # encontra a posição do primeiro elemento vazio
            offspring[i] = city 

    return offspring


def create_new_generation(population, population_size, distances, cities_per_salesman):
    new_population = []
    selected_parents = binary_tournament_selection(population, population_size, distances, cities_per_salesman)

    # metade da populacao é selecionada --> como cada dois pais geram 1 filho, serão gerados 1/4 da nova geração

    for parents in selected_parents:
        offspring = crossover(parents)
        new_population.append(offspring)
    '''
        - fazer selecao (✓)
        - aplicar crossing over selecionados nos selecionados para gerar os filhos (✓)
        - aplicar mutacao nos selecionados
        - substituir a populacao pelos pais selecionados e filhos mutados e recombinados
    '''

n_salesman = 3
n_cities = 32
coordinates = [(500, 500), (826, 465), (359, 783), (563, 182), (547, 438), (569, 676), 
               (989, 416), (648, 750), (694, 978), (493, 969), (175, 89), (104, 130), 
               (257, 848), (791, 249), (952, 204), (34, 654), (89, 503), (548, 964), 
               (492, 34), (749, 592), (536, 875), (373, 708), (385, 260), (560, 751), (304, 516), 
               (741, 368), (59, 131), (154, 681), (425, 456), (885, 783), (30, 415), (61, 25)]

distances = calculate_distances(n_cities, coordinates)
cities_per_salesman = calculate_cities_per_salesman(n_salesman, n_cities)
population_size = 50

population = initialize_population(population_size, cities_per_salesman, n_cities)
create_new_generation(population, population_size, distances, n_cities)