
setwd("C:/Users/Ricardo/Desktop/CE_analysis/seed_0")
measures <- c()
pop_size = c(20,100,150,200)
muta = c(0.1, 0.25, 0.5, 0.75, 0.9)
cross = c(0.1, 0.25, 0.5, 0.75, 0.9)

#seed 1
for (n in pop_size){
  for (i in muta){
    for (j in cross){
      fileName <- paste("pop_size",n,"muta",i,"cross",j,"csv", sep = "")
      dataset <- read.table(fileName, header=TRUE, quote="\"")
      
      measures <- add_values(measures, dataset)
    }
  }  
  
}

#other seeds
