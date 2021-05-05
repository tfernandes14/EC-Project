'''
TODO:
- traçar graficos da evoluçao das populaçoes
- juntar tudo num df
- guardar as iterações em que troca
'''

from random import random, randint, sample
from operator import itemgetter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
from scipy.spatial.distance import hamming
from math import factorial

pd.set_option('display.max_rows', None)


# Simple [Binary] Evolutionary Algorithm
def sea(numb_generations, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method):
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
    hamming_both = np.zeros((numb_generations, 1))

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
            else:
                # print("switch randoms")
                populacao_1 = switch_random(populacao_1, replace_n, size_cromo, fitness_func)
                populacao_2 = switch_random(populacao_2, replace_n, size_cromo, fitness_func)

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
        hamming_both[k] = calculate_hamming_all(populacao_1, populacao_2)

    bleh = np.concatenate((best_fit, avg_fit, hamming_fit, hamming_both, swap_index), axis=1)
    tabela = pd.DataFrame(bleh, columns=["Best Fitness 1", "Best Fitness 2", "Avg Fitness 1", "Avg Fitness 2", "Avg Hamming 1", "Avg Hamming 2", "Avg Hamming Pop", "Swap index"])
    """print(tabela)
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
    plt.show()"""

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
    return evaluate(phenotype(indiv), len(indiv))

def phenotype(indiv):
    fen = [i+1 for i in range(len(indiv)) if indiv[i] == 1]
    return fen


def evaluate(indiv, comp):
    alfa = 1.0
    beta = 1.1
    return alfa * len(indiv) - beta * viola(indiv,comp)

def viola(indiv,comp):
    # Count violations
    v = 0
    for elem in indiv:
        limite = min(elem-1,comp-elem)
        vi = 0
        for j in range(1,limite+1):
            if ((elem - j) in indiv) and ((elem+j) in indiv):
                vi += 1
        v += vi
    return v
"""
if __name__ == '__main__':
    #to test the code with oneMax function
    n_gen = 200
    size_pop = 20
    size_cromo = 200        # Array de zeros e uns
    prob_mut = 0.01
    prob_cross = 0.8
    sel_parents = tour_sel(4)
    recombination = two_points_cross
    mutation = muta_bin
    sel_survivors = sel_survivors_elite(0.03)
    fitness_func = fitness
    freq = 0
    replace_n = int(0.5 * size_pop)
    method = 1   # 1 - Switch indiv / 2 - Switch random
    # sea(numb_generations, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method)
    best_1 = sea(n_gen, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method)
    # display(best_1[0], fenotipo)
    #print(best_1[0])
    #print("----")
    #print(best_1[1])
   """