# -*- coding: utf-8 -*-
"""
@authors: Francisco Guerra, Ricardo Martins, Tiago Fernandes, Ernesto Costa
"""
from sea import sea, tour_sel, muta_bin, fitness, one_point_cross, two_points_cross, sel_survivors_elite, uniform_cross
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import os as os
import sys


if __name__ == '__main__':
    n_gen = 150
    size_pop = 50
    size_cromo = 100
    prob_mut = [0.01, 0.05]
    prob_cross = [0.9, 0.5]
    sel_parents = tour_sel(5)
    recombination = [two_points_cross, uniform_cross]
    mutation = muta_bin
    sel_survivors = sel_survivors_elite(0.02)
    fitness_func = fitness
    
    if len(sys.argv) == 5:
        freq =  float(sys.argv[1])
        replace_n =   float(sys.argv[2])
        method =  int(sys.argv[3])
        seed = int(sys.argv[4])
        random.seed(seed)
        np.random.seed(seed)

        replace = int(size_pop * replace_n)

        print(freq)
        print(replace_n)
        print(method)
        print(seed)
        print(replace)

        filepath = "testing/seed_" + str(seed)
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        random.seed(seed)
        np.random.seed(seed)
        df = sea(n_gen, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace, method)
        df.to_csv("testing\seed_" + str(seed) + "\seed{}freq{}num_replace{}method{}.csv".format(
            seed,
            freq,
            replace_n,
            method,
        ),
            index=False,
            index_label=False
        )

    else:
        seed = 2021
        random.seed(seed)
        np.random.seed(seed)

        filepath = "testing/seed_" + str(seed)
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        df = sea(n_gen, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, 0, 0, 0)
        df.to_csv("testing\seed_" + str(seed) + "\seed{}.csv".format(
            seed,
        ),
            index=False,
            index_label=False
        )
    """
    freq = 0.6
    replace_n = int(0.2 * size_pop)
    method = 2   # 1 - Switch indiv / 2 - Switch random
    #"""
    
    '''random.seed(2021)
    seeds = [random.randint(2, 3500) for i in range(30)]

    for i in range(15, 20):     # 0 - 10 (9) Ricardo, 10 - 20 (19) Tiago, 20 - 30 (29) Guerra
        seed = seeds[i]
        count = 0

        #write df
        filepath = "testing/seed_" + str(i)
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        df = sea(n_gen, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, 0, 0, 0)
        df.to_csv("testing\seed_" + str(i) + "\seed{}.csv".format(
            seed,
        ),
            index=False,
            index_label=False
        )


        for freq in [0.1, 0.25, 0.5, 0.75, 0.9]:
            for replace_n in [0.05, 0.1, 0.25, 0.4, 0.5]:
                replace = int(size_pop * replace_n)
                for method in [1, 2, 3]:
                    random.seed(seed)
                    np.random.seed(seed)
                    df = sea(n_gen, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace, method)
                    df.to_csv("testing\seed_" + str(i) + "\seed{}freq{}num_replace{}method{}.csv".format(
                        seed,
                        freq,
                        replace_n,
                        method,
                    ),
                        index=False,
                        index_label=False
                    )
                    count += 1
                    print(count)
'''
    

    
    
