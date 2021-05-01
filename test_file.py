from sea import sea, tour_sel, muta_bin, fitness, one_point_cross, two_points_cross, sel_survivors_elite
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

if __name__ == '__main__':
    
    n_gen = 150
    size_pop = 20
    size_cromo = 10
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


    for seed in seeds:
        np.random.seed(seed)
        #test different frequences for replacement
        for i in [0, 0.25, 0.5, 0.75, 1]:
            df = sea(n_gen, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method)
            #write df
            df.to_csv("seed_{}_freq_{}_method_{}_numpop_2.csv".format(
            seed,
            freq,
            method,
            ),
            index=False,
            index_label=False
        )