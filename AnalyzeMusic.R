# Title     : TODO
# Objective : TODO
# Created by: Cormac
# Created on: 5/26/19

Data = read.csv("MusicData.csv") # the data to be read

## Tells you basic info about your data
## Takes a Data$"row name" and returns the mean and standard deviation of the data
basicInfo = function(data){
    return (mean(data), sd(data))
}


