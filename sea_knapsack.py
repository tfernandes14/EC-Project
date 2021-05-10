'''
TODO:
- traçar graficos da evoluçao das populaçoes
- juntar tudo num df
- guardar as iterações em que troca
'''

from random import random, randint, sample, seed
from operator import itemgetter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
from scipy.spatial.distance import hamming
from math import factorial

import time

pd.set_option('display.max_rows', None)

problem = {
    'values': [
        360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147, 78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28, 87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276, 312,
        360, 83, 59, 130, 431, 67, 230, 52, 93, 125, 670, 892, 600, 38, 48, 147, 78, 256, 63, 17, 120, 164, 432, 35, 92, 110, 22, 42, 50, 323, 514, 28, 87, 73, 78, 15, 26, 78, 210, 36, 85, 189, 274, 43, 33, 10, 19, 389, 276, 312
    ],
    'weights': [
        7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0, 42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71, 3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13,
        7, 0, 30, 22, 80, 94, 11, 81, 70, 64, 59, 18, 0, 36, 3, 8, 15, 42, 9, 0, 42, 47, 52, 32, 26, 48, 55, 6, 29, 84, 2, 4, 18, 56, 7, 29, 93, 44, 71, 3, 86, 66, 31, 65, 0, 79, 20, 65, 52, 13
    ],
    'capacity': 1700
}


# Total value: 15116
# Total weight: 1700
# Packed items: [0, 1, 3, 4, 6, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 27, 29, 30, 31, 32, 34, 38, 39, 41, 42, 44, 47, 48, 49, 50, 51, 53, 54, 56, 60, 61, 62, 64, 65, 66, 67, 68, 69, 70, 71, 72, 77, 79, 80, 81, 82, 84, 88, 89, 91, 92, 94, 97, 98, 99]
# Packed_weights: [7, 0, 22, 80, 11, 59, 18, 0, 3, 8, 15, 42, 9, 0, 42, 47, 52, 26, 6, 84, 2, 4, 18, 7, 71, 3, 66, 31, 0, 65, 52, 13, 7, 0, 22, 80, 11, 59, 18, 0, 3, 8, 15, 42, 9, 0, 42, 47, 52, 6, 84, 2, 4, 18, 7, 71, 3, 66, 31, 0, 65, 52, 13]


# Knapsack Evolutionary Algorithm
def sea(numb_generations, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method):
    start = time.time()
    # inicialize population: indiv = (cromo, fit)
    populacao_1 = gera_pop(size_pop, size_cromo)
    populacao_2 = gera_pop(size_pop, size_cromo)

    # evaluate population
    populacao_1 = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao_1]
    populacao_2 = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao_2]

    swap_index = np.zeros((numb_generations, 1))
    best_fit = np.zeros((numb_generations, 2))
    avg_fit = np.zeros((numb_generations, 2))
    hamming_fit = np.zeros((numb_generations, 2))

    for k in range(numb_generations):
        #print("geraçao", k)
        # sparents selection
        mate_pool = sel_parents(populacao_1)
        # Variation
        # ------ Crossover
        progenitores = []
        for i in range(0, size_pop - 1, 2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i + 1]
            filhos = recombination(indiv_1, indiv_2, prob_cross)
            progenitores.extend(filhos)
        # ------ Mutation
        descendentes = []
        for indiv, fit in progenitores:
            novo_indiv = mutation(indiv, prob_mut)
            descendentes.append((novo_indiv, fitness_func(novo_indiv)))
        # New population
        populacao_1 = sel_survivors(populacao_1, descendentes)
        # Evaluate the new population
        populacao_1 = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao_1]

        # parents selection
        mate_pool = sel_parents(populacao_2)
        # Variation
        # ------ Crossover
        progenitores = []
        for i in range(0, size_pop - 1, 2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i + 1]
            filhos = recombination(indiv_1, indiv_2, prob_cross)
            progenitores.extend(filhos)
        # ------ Mutation
        descendentes = []
        for indiv, fit in progenitores:
            novo_indiv = mutation(indiv, prob_mut)
            descendentes.append((novo_indiv, fitness_func(novo_indiv)))
        # New population
        populacao_2 = sel_survivors(populacao_2, descendentes)
        # Evaluate the new population
        populacao_2 = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao_2]

        # Switch individuals between populations
        if random() < freq:
            swap_index[k][0] = 1

            # change individuals
            if method == 1:
                # print("switch_indivs")
                populacao_1, populacao_2 = switch_indivs(populacao_1, populacao_2, replace_n)
            elif method == 2:
                # print("switch randoms")
                populacao_1 = switch_random(populacao_1, replace_n, size_cromo, fitness_func)
                populacao_2 = switch_random(populacao_2, replace_n, size_cromo, fitness_func)
            elif method == 3:
                populacao_1 = switch_indivs_dist(populacao_1, populacao_2, replace_n)

        populacao_1.sort(key=itemgetter(1), reverse=True)     # Descending order
        populacao_2.sort(key=itemgetter(1), reverse=True)     # Descending order

        avg_1 = [ind[1] for ind in populacao_1]
        avg_2 = [ind[1] for ind in populacao_2]
        best_fit[k][0] = populacao_1[0][1]
        best_fit[k][1] = populacao_2[0][1]
        avg_fit[k][0] = np.mean(avg_1)
        avg_fit[k][1] = np.mean(avg_2)
        hamming_fit[k][0] = calculate_hamming(populacao_1, populacao_1)
        hamming_fit[k][1] = calculate_hamming(populacao_2, populacao_2)
    
    # print("====", time.time() - start)
    bleh = np.concatenate((best_fit, avg_fit, hamming_fit, swap_index), axis=1)
    tabela = pd.DataFrame(bleh, columns=["Best Fitness 1", "Best Fitness 2", "Avg Fitness 1", "Avg Fitness 2", "Avg Hamming 1", "Avg Hamming 2", "Swap index"])
    '''print(tabela)
    plt.figure(1)
    plt.title("Fitness values")
    tabela["Best Fitness 1"].plot(label="Best Fitness 1")
    tabela["Avg Fitness 1"].plot(label="Average Fitness 1")
    tabela["Best Fitness 2"].plot(label="Best Fitness 2")
    tabela["Avg Fitness 2"].plot(label="Average Fitness 2")
    plt.legend()

    swap_index = swap_index.T
    indexes = np.where(swap_index == 1)
    # print(indexes[1])
    plt.vlines(indexes[1], -600, 50, color="red")
    plt.show()

    plt.figure(2)
    plt.title("Hamming Distances")
    tabela["Avg Hamming 1"].plot(label="Average Hamming 1")
    tabela["Avg Hamming 2"].plot(label="Average Hamming 2")
    tabela["Avg Hamming Pop"].plot(label="Average Hamming between Populations")
    plt.legend()
    plt.show()'''

    return tabela


def switch_indivs(pop_1, pop_2, n):
    copy_pop_1 = copy.deepcopy(pop_1)
    copy_pop_2 = copy.deepcopy(pop_2)
    aux = copy_pop_2[len(pop_2) - n:]
    copy_pop_2[len(pop_2) - n:] = copy_pop_1[len(pop_1) - n:]
    copy_pop_1[len(pop_1) - n:] = aux
    return copy_pop_1, copy_pop_2


def switch_random(pop, n, size_cromo, fitness_func):
    new_pop = gera_pop(n, size_cromo)
    new_pop = [(indiv[0], fitness_func(indiv[0])) for indiv in new_pop]
    pop[len(pop) - n:] = new_pop
    
    return copy.deepcopy(pop)


def switch_indivs_dist(pop1, pop2, n):
    copy_pop1 = copy.deepcopy(pop1)
    copy_pop2 = copy.deepcopy(pop2)
    
    indexes = []
    for i in range(n):
        index = 0
        mini = pop1[0][1]
        for k in range(1, len(pop1)):
            if mini >= pop1[k][1]:
                mini = pop1[k][1]
                index = k

        dists = [hamming(pop1[index][0], pop2[j][0]) for j in range(len(copy_pop2))]
        index_change = dists.index(max(dists))
        indexes.append(index_change)

        aux = copy_pop2[index_change]
        copy_pop1[index] = aux

        copy_pop2.pop(index_change)

    return copy_pop1


def calculate_hamming(pop_1, pop_2):
    res = []# np.zeros((factorial(len(pop_1))) / (factorial(len(pop_1) - 2) * factorial(2)))
    # print(res.shape)
    for i in range(len(pop_1)):
        for j in range(i + 1, len(pop_1)):
            res.append(hamming(pop_1[i][0], pop_2[j][0]))
    return np.mean(res)#, res


def calculate_hamming_all(pop_1, pop_2):
    combs = (factorial(len(pop_1))) / (factorial(len(pop_1) - 2) * factorial(2))
    res = []
    for i in range(len(pop_1)):
        for j in range(i, len(pop_2)):
            res.append(hamming(pop_1[i][0], pop_2[j][0]))
    return sum(res) / combs


# Initialize population
def gera_pop(size_pop, size_cromo):
   return [(gera_indiv(size_cromo), 0) for i in range(size_pop)]

def gera_indiv(size_cromo):
    # random initialization
    indiv = [randint(0, 1) for i in range(size_cromo)]
    return indiv

# Variation operators: Binary mutation
def muta_bin(indiv, prob_muta):
    # Mutation by gene
    cromo = indiv[:]
    for i in range(len(indiv)):
        cromo[i] = muta_bin_gene(cromo[i], prob_muta)
    return cromo

def muta_bin_gene(gene, prob_muta):
    g = gene
    value = random()
    if value < prob_muta:
        g ^= 1
    return g

# Variation Operators :Crossover
def one_point_cross(indiv_1, indiv_2, prob_cross):
    value = random()
    if value < prob_cross:
        cromo_1 = indiv_1[0]
        cromo_2 = indiv_2[0]
        pos = randint(0, len(cromo_1))
        f1 = cromo_1[0:pos] + cromo_2[pos:]
        f2 = cromo_2[0:pos] + cromo_1[pos:]
        return ((f1, 0), (f2, 0))
    else:
        return (indiv_1, indiv_2)

def two_points_cross(indiv_1, indiv_2, prob_cross):
    value = random()
    if value < prob_cross:
        cromo_1 = indiv_1[0]
        cromo_2 = indiv_2[0]
        pc = sample(range(len(cromo_1)), 2)
        pc.sort()
        pc1,pc2 = pc
        f1= cromo_1[:pc1] + cromo_2[pc1:pc2] + cromo_1[pc2:]
        f2= cromo_2[:pc1] + cromo_1[pc1:pc2] + cromo_2[pc2:]
        return ((f1,0), (f2,0))
    else:
        return (indiv_1,indiv_2)

def uniform_cross(indiv_1, indiv_2, prob_cross):
    value = random()
    if value < prob_cross:
        cromo_1 = indiv_1[0]
        cromo_2 = indiv_2[0]
        f1=[]
        f2=[]
        for i in range(0, len(cromo_1)):
            if random() < 0.5:
                f1.append(cromo_1[i])
                f2.append(cromo_2[i])
            else:
                f1.append(cromo_2[i])
                f2.append(cromo_1[i])
        return ((f1, 0),(f2, 0))
    else:
        return (indiv_1, indiv_2)

# Parents Selection: tournament
def tour_sel(t_size):
    def tournament(pop):
        size_pop = len(pop)
        mate_pool = []
        for i in range(size_pop):
            winner = one_tour(pop, t_size)
            mate_pool.append(winner)
        return mate_pool
    return tournament

def one_tour(population, size):
    """Maximization Problem. Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]


# Survivals Selection: elitism
def sel_survivors_elite(elite):
    def elitism(parents, offspring):
        size = len(parents)
        comp_elite = int(size * elite)
        offspring.sort(key=itemgetter(1), reverse=True)
        parents.sort(key=itemgetter(1), reverse=True)
        new_population = parents[:comp_elite] + offspring[:size - comp_elite]
        return new_population
    return elitism


# Auxiliary
def display(indiv, phenotype):
    print('Chromo: %s\nFitness: %s' % (phenotype(indiv[0]), indiv[1]))

def best_pop(populacao):
    populacao.sort(key=itemgetter(1), reverse=True)
    return populacao[0]

def average_pop(populacao):
    return sum([fit for cromo, fit in populacao]) / len(populacao)

# -------------------  Problem Specific Definitions  ------------
# -------------------  One max problem --------------------------

def fitness(indiv):
    return evaluate_zero(phenotype(indiv))

# problem = {'values': [60, 100, 120, 50], 'weights': [10, 20, 30, 5], 'capacity': 50}
# [([0, 1, 0, 0, 1], 10), ([0, 1, 0, 0, 0], 0)]
def phenotype(indiv):
    res = []
    for id in range(len(indiv)):
        # print(id, problem['weights'][id], problem['values'][id])
        if indiv[id] == 1:
            res.append([id, problem['weights'][id], problem['values'][id]])
    return res


def evaluate_zero(feno):
    total_weight = sum([weight for id_, weight, value in feno])
    if total_weight > problem["capacity"]:
        return 0
    return sum([value for id, weight, value in feno])


def list_items(problem):
    weight_value_list = list(zip(problem['weights'], problem['values']))
    return [[id_, w, v, v/w] for id_, (w, v) in enumerate(weight_value_list)]


def decode_int(indiv, problem):
    capacity = problem["capacity"]
    l_items = list_items(problem)
    sum_weights = 0
    res = []
    for i in range(len(indiv)):
        j = indiv[i]
        id_, w, v, r = l_items.pop(j)
        if sum_weights + w <= capacity:
            sum_weights += w
            res.append([id_, w, v, r])
        else:
            return res
    return res

'''if __name__ == '__main__':
    #to test the code with oneMax function
    np.random.seed(0)
    seed(0)
    n_gen = 200
    size_pop = 10
    size_cromo = len(problem["values"])        # Array de zeros e uns
    prob_mut = 0.01
    prob_cross = 0.8
    sel_parents = tour_sel(4)
    recombination = two_points_cross
    mutation = muta_bin
    sel_survivors = sel_survivors_elite(0.03)
    fitness_func = fitness
    freq = 0.6
    replace_n = int(0.5 * size_pop)
    method = 3   # 1 - Switch indiv / 2 - Switch random / 3 - switch indivs dist
    # sea(numb_generations, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method)
    best_1 = sea(n_gen, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method)
    # print(best_1)
    # display(best_1[0], fenotipo)
    #print(best_1[0])
    #print("----")
    #print(best_1[1])'''