# -*- coding: utf-8 -*-
"""
Created on Tue May 11 01:39:56 2021

@author: Ricardo
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import os as os
from stat_alunos import *


def post_hoc_multiple(size, configs):
    count =  0
    values_p = []
    post_hoc_table = np.zeros((size,size))
    for i in range(size):
        for j in range(i+1,size):
            c, p = wilcoxon(configs[i], configs[j])
            post_hoc_table[i][j] = p
            count += 1
            values_p.append(p)
    print(count)
    #falta a correção de bonferroni

    return post_hoc_table, np.array(values_p)

def draw_shappiro(df):
    plt.figure(1)
    plt.scatter(df["Method"], df["statistic"])
    plt.xlabel("Method")
    plt.ylabel("Statistic value")
    plt.grid(True)
    plt.savefig("statistic.png")
    plt.show()

    plt.figure(2)
    plt.scatter(df["Method"], df["p-value"])
    plt.xlabel("Method")
    plt.ylabel("P-value")
    plt.hlines(0.05, xmin=0, xmax=26, color='green', label="Confidence level 0.05")
    plt.legend()
    plt.grid(True)
    plt.savefig("p_value.png")

random.seed(2021)
seeds = [random.randint(2, 3500) for i in range(30)]

size_pop = 50


setup = 0
configs = np.zeros((27,30))
configs_dist = np.zeros((27,30))

method_1 = []
method_2 = []
method_3 = []

#df = pa.Dataframe()

for freq in [0.1, 0.5, 0.9]:
    for replace_n in [0.1, 0.25, 0.5]:
        replace = int(size_pop * replace_n)
        #for method in [1,2,3]:
        count = 0
        
        for seed in seeds:
        
            filepath_1 = "testing_knapsack_3\seed_"+str(count)+"\seed"+str(seed)+"freq"+str(freq)+"num_replace"+str(replace_n)+"method"+str(1)+".csv" 
            df_1 = pd.read_csv(filepath_1)
            
            filepath_2 = "testing_knapsack_3\seed_"+str(count)+"\seed"+str(seed)+"freq"+str(freq)+"num_replace"+str(replace_n)+"method"+str(2)+".csv" 
            df_2 = pd.read_csv(filepath_2)
            
            filepath_3 = "testing_knapsack_3\seed_"+str(count)+"\seed"+str(seed)+"freq"+str(freq)+"num_replace"+str(replace_n)+"method"+str(3)+".csv" 
            df_3 = pd.read_csv(filepath_3)
        
            
            configs[setup][count] = max(max(df_1["Best Fitness 1"]) , max(df_1["Best Fitness 2"]))
            configs[setup+1][count] = max(max(df_2["Best Fitness 1"]) , max(df_2["Best Fitness 2"]))
            configs[setup+2][count] = max(max(df_3["Best Fitness 1"]) , max(df_3["Best Fitness 2"]))
    
            count += 1
            
        setup += 3
            
            

configs_2 = []
configs_dist_2 = []
labels = ["method" + str(i+1) for i in range(27)]

for j in range(27):
    configs_2.append(configs[j])
    

box_plot(configs_2, labels)
#box_plot(configs_dist_2, labels)


#Test if normal
#Shapiro wilk nas diferenças das medias
alpha = 0.05
non_normal = False 

norm = np.zeros((27,2))
for i in range(len(configs_2)):
    stat, p = test_normal_sw(configs_2[i])
    norm[i][0] = stat
    norm[i][1] = p
    if p < alpha:  
        non_normal = True

df = pd.DataFrame(norm, columns=["statistic", "p-value"])
df["Method"] = [str(i) for i in range(1, 28)]

draw_shappiro(df)

if non_normal==False:
    print("Follows Gaussian Distribution")
else:
    print("Does not follow Gaussian Distribution")

#There are some that dont follow a normal distribution so we need to use non parametric

stat, p = friedman_chi(configs_2)

if p > alpha:
	print('Same distributions (fail to reject H0)')
else:
	print('Different distributions (reject H0)')
