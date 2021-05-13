

import pandas as pd
import numpy as np

avg_best_combo = []

pop_size = 50

best_avg = 0

for muta in [0.01, 0.025, 0.05]:
    for cross in [0.5, 0.6, 0.7, 0.8, 0.9]:
        for recomb_ind in range(3):
            for sel_parent_ind in range(4):
                filename_1 = "seed3427pop_size"+str(pop_size)+"muta"+str(muta)+"cross"+str(cross)+"recob"+str(recomb_ind)+"sel_parents"+str(sel_parent_ind)
                df_1 = pd.read_csv("seed_0/"+filename_1+".csv")
                
                filename_2 = "seed1657"+"pop_size"+str(pop_size)+"muta"+str(muta)+"cross"+str(cross)+"recob"+str(recomb_ind)+"sel_parents"+str(sel_parent_ind)
                df_2 = pd.read_csv("seed_1/"+filename_2+".csv")
                
                filename_3 = "seed2581"+"pop_size"+str(pop_size)+"muta"+str(muta)+"cross"+str(cross)+"recob"+str(recomb_ind)+"sel_parents"+str(sel_parent_ind)
                df_3 = pd.read_csv("seed_2/"+filename_3+".csv")
                
                filename_4 = "seed2230"+"pop_size"+str(pop_size)+"muta"+str(muta)+"cross"+str(cross)+"recob"+str(recomb_ind)+"sel_parents"+str(sel_parent_ind)
                df_4 = pd.read_csv("seed_3/"+filename_4+".csv")
                
                filename_5 = "seed1135"+"pop_size"+str(pop_size)+"muta"+str(muta)+"cross"+str(cross)+"recob"+str(recomb_ind)+"sel_parents"+str(sel_parent_ind)
                df_5 = pd.read_csv("seed_4/"+filename_5+".csv")
                
                filename_6 = "seed1015"+"pop_size"+str(pop_size)+"muta"+str(muta)+"cross"+str(cross)+"recob"+str(recomb_ind)+"sel_parents"+str(sel_parent_ind)
                df_6 = pd.read_csv("seed_5/"+filename_6+".csv")
        
                mean_1 = (df_1["Best Fitness 1"].max() + df_1["Best Fitness 2"].max())/2
                mean_2 = (df_2["Best Fitness 1"].max() + df_2["Best Fitness 2"].max())/2
                mean_3 = (df_3["Best Fitness 1"].max() + df_3["Best Fitness 2"].max())/2
                mean_4 = (df_4["Best Fitness 1"].max() + df_4["Best Fitness 2"].max())/2
                mean_5 = (df_5["Best Fitness 1"].max() + df_5["Best Fitness 2"].max())/2
                mean_6 = (df_6["Best Fitness 1"].max() + df_6["Best Fitness 2"].max())/2
                
                teste = (mean_1+mean_2+mean_3+mean_4+mean_5+mean_6)/6
                
                if teste > best_avg:
                    best_avg = teste
                    print("prob muta: "+str(muta)+"prob crossover: "+str(cross)+"recomb ind: "+str(recomb_ind)+"sel_parent_id: "+ str(sel_parent_ind))
                
                avg_best_combo.append(teste)
            

