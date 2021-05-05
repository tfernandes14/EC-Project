from sea import sea, tour_sel, muta_bin, fitness, one_point_cross, two_points_cross, sel_survivors_elite
import matplotlib.pyplot as plt
import pandas as pd
from sea import sea, tour_sel, muta_bin, fitness, one_point_cross, two_points_cross, sel_survivors_elite
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random

if __name__ == '__main__':
    
    n_gen = 200
    size_pop = 20
    size_cromo = 100
    prob_mut = 0.01
    fitness_func = fitness
    prob_cross = 0.8
    sel_parents = tour_sel(3)
    recombination = one_point_cross
    mutation = muta_bin
    sel_survivors = sel_survivors_elite(0.02)
    freq = 0
    replace_n = 0
    method = 2   # 1 - Switch indiv / 2 - Switch random
    # sea(numb_generations, size_pop, size_cromo, prob_mut, prob_cross, sel_parents, recombination, mutation, sel_survivors, fitness_func, freq, replace_n, method)
    
    random.seed(2021)
    seeds = [random.randint(2,3500) for i in range(30)]

    recomb = [one_point_cross, two_points_cross, uniform_cross]
    sel_parent = [tour_sel(2), tour_sel(3), tour_sel(4), tour_sel(5)]
    count = 0
    np.random.seed(seeds[0])
    #test different frequences for replacement
    #pop size
    for pop_size in [20, 100, 150, 200, 250]:
        for muta in [0.01, 0.025, 0.05, 0.075, 0.1]:
            for cross in [0.5, 0.6, 0.7, 0.8, 0.9]:
                for recomb_ind in range(len(recomb)):
                    for sel_parent_ind in range(len(sel_parent)):

                        df = sea(n_gen, pop_size, size_cromo, muta, cross, sel_parent[sel_parent_ind], recomb[recomb_ind], mutation, sel_survivors, fitness_func, 0, replace_n, method)
                        #write df
                        df.to_csv("seed_0/seed{}pop_size{}muta{}cross{}recob{}sel_parents{}.csv".format(
                        seeds[0],
                        pop_size,
                        muta,
                        cross,
                        recomb_ind,
                        sel_parent_ind,
                        ),
                            index=False,
                            index_label=False
                        )
                        count += 1
                        print(count)