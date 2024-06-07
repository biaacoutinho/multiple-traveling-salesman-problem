import math
import random
from tqdm import tqdm

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
    number_of_selected_individuals = pop_size//4 # 25% da população será escolhida de forma aleatoria para ocorrer o torneio

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
    start_of_selection = random.randint(0, n_cities - 1 - num_selected_cities) # a selecao de cidades pode ir atenum_selected_cities antes de terminar o vetor, senão serão selecionadas cidades fora do vetor, com índices superiores ao do último elemento
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

n_salesman = 5
n_cities = 92
coordinates = [
    (500, 500), (354, 968), (582, 631), (411, 807), (153, 112), (505, 398),
    (117, 730), (854, 568), (234, 931), (140, 725), (499, 319), (632, 956),
    (220, 520), (86, 12), (689, 560), (580, 845), (984, 339), (653, 282),
    (615, 278), (840, 501), (967, 289), (804, 22), (795, 741), (263, 847),
    (601, 850), (150, 800), (390, 969), (967, 117), (279, 909), (711, 399),
    (435, 707), (949, 661), (590, 776), (616, 836), (414, 335), (779, 251),
    (34, 986), (567, 90), (420, 780), (811, 535), (868, 563), (487, 937),
    (991, 195), (938, 91), (666, 333), (243, 527), (247, 770), (257, 731),
    (159, 596), (23, 1), (225, 558), (112, 306), (965, 492), (655, 810),
    (545, 178), (467, 143), (704, 298), (902, 210), (111, 303), (842, 978),
    (252, 286), (481, 122), (42, 875), (868, 379), (624, 785), (19, 213),
    (737, 684), (854, 931), (906, 247), (726, 15), (905, 787), (968, 995),
    (293, 355), (592, 311), (94, 584), (337, 619), (902, 561), (82, 710),
    (766, 539), (602, 185), (975, 768), (727, 782), (136, 946), (567, 892),
    (616, 98), (536, 730), (311, 585), (164, 43), (713, 690), (445, 631),
    (840, 935), (257, 761)
]


distances = calculate_distances(n_cities, coordinates)
cities_per_salesman = calculate_cities_per_salesman(n_salesman, n_cities)
population_size = 100

population = initialize_population(population_size, n_cities)
for _ in tqdm(range(50000)):
    population = create_new_generation(population, population_size, distances, cities_per_salesman, n_cities)

individual = order_by_fitness(population, distances, cities_per_salesman)[0]
distance = calculate_fitness_of_an_individual(distances, individual, cities_per_salesman)

print(distance)
 