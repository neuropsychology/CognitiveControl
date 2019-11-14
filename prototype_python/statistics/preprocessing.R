library(tidyverse)
library(easystats)

# Example
# folder <- "../data/dd/"

preprocess_ProcessingSpeed <- function(folder){
  data <- read.csv(list.files(folder, "*_ProcessingSpeed.csv", full.names = TRUE))


}
