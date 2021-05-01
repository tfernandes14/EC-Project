from sea import sea, tour_sel, muta_bin, fitness, one_point_cross, two_points_cross, sel_survivors_elite
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

if __name__ == '__main__':
    
    n_gen = 400
    size_pop = 20
    size_cromo = 100
    prob_mut = 0.01
    prob_cross = 0.8
    sel_parents = tour_sel(3)
    recombination = one_point_cross
    mutation = muta_bin
    sel_survivors = sel_survivors_elite(0.02)
    fitness_func = fitness
    freq = 0.6
    replace_n = int(0.2 * size_pop)
    method = 2   # 1 - Switch indiv / 2 - Switch random
    # sea(numb_generations, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method)
    
    random.seed(2021)
    seeds = [random.randint(2,3500) for i in range(30)]


    count = 0

    np.random.seed(seeds[1])
    #test different frequences for replacement
    #pop size
    for pop_size in [20, 100, 150, 200, 250]:
        for muta in [0.1, 0.25, 0.5, 0.75, 0.9]:
            for cross in [0.1, 0.25, 0.5, 0.75, 0.9]:

                df = sea(n_gen, pop_size, size_cromo, muta, cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, 0, replace_n, method)
                #write df
                df.to_csv("seed{}pop_size{}muta{}cross{}.csv".format(
                seed,
                pop_size,
                muta,
                cross,
                ),
                    index=False,
                    index_label=False
                )
                count += 1
                print(count)