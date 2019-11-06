library(tidyverse)
library(easystats)
library(rstanarm)
library(lme4)
library(ggplot2)




########################### PROCESSING SPEED ########################

#####################################################
# Read data

#read_plus <- function(all_files) {
#  read_csv(all_files) %>%
#    mutate(filename = basename(all_files))
#}

df_ProcessingSpeed <-
  list.files(path = "../NumberTrialsCalibration/data/",
             pattern = "*_ProcessingSpeed.csv",
             full.names = TRUE) %>%
  map_df(~read_csv(.)[, -c(7,8)])

#####################################################
# Preprocessing

### Raw data
df_ProcessingSpeed <- df_ProcessingSpeed %>%
  mutate(Right_Bias = ifelse(Stimulus_Side == "RIGHT", "RIGHT", "LEFT")) %>%
  mutate(Previous_Response = ifelse(is.na(Previous_Response), "NO", "YES")) %>%
  mutate(Previous_RT = ifelse(Previous_Response == "YES", Previous_RT, 0)) %>%
  mutate(Error = ifelse(Response != "DOWN", "YES", "NO"))

### Only accurate trials (for RT)

df_ProcessingSpeed_Correct <- df_ProcessingSpeed %>%
  filter(Error == "NO")

### Remve outliers
df_ProcessingSpeed_Clean <- df_ProcessingSpeed_Correct %>%
  mutate(Outlier_Score = as.numeric(check_outliers(RT, method = c("zscore", "iqr")))) %>%
  filter(!Outlier_Score >= 0.5) %>%
  select(- c(Outlier_Score, Error))

### Number of impulsive responses, correct and incorrect responses, outliers
n_impulsive = sum(df_ProcessingSpeed$Previous_Response == "YES")/ nrow(df_ProcessingSpeed)
n_correct = nrow(df_ProcessingSpeed_Correct)/nrow(df_ProcessingSpeed)
n_incorrect = (nrow(df_ProcessingSpeed) - nrow(df_ProcessingSpeed_Correct))/nrow(df_ProcessingSpeed)
n_outliers = (nrow(df_ProcessingSpeed_Correct) - nrow(df_ProcessingSpeed_Clean))/nrow(df_ProcessingSpeed_Correct)



#####################################################
# Stat models
if (length(which(df_ProcessingSpeed_Clean$Previous_Response == "YES"))/nrow(df_ProcessingSpeed_Clean) > 0.2) {
  model_PS <- lm(RT ~ poly(Trial_Order, 2) + poly(ITI, 2) + Right_Bias + Previous_Response + Previous_Response:Previous_RT, data = df_ProcessingSpeed_Clean)
} else {
  model_PS <- lm(RT ~ poly(Trial_Order, 2) + poly(ITI, 2) + Right_Bias, data = df_ProcessingSpeed_Clean)
}

#df_ProcessingSpeed_Clean <-  data.frame(df_ProcessingSpeed_Clean)
#model_PS <- lm(RT ~ poly(Trial_Order, 2) + poly(ITI, 2) + Right_Bias, data = df_ProcessingSpeed_Clean)


## Analyse ITI
PS_ITI_ref <- data.frame(
              "Trial_Order" = rep(1, 1000),
              "ITI" = seq(from = min(df_ProcessingSpeed_Clean$ITI),                                     to = max(df_ProcessingSpeed_Clean$ITI),                                      length.out = 1000),
              "Right_Bias" = rep("LEFT", 1000),
              "Previous_Response" = rep("NO", 1000),
              "Previous_RT" = rep(0, 1000))
PS_ITI_pred =  estimate_response(model_PS, PS_ITI_ref)

PS_ITI_pred = cbind(PS_ITI_ref, PS_ITI_pred [,-c(1:3)])
ITI_min = which.min(PS_ITI_pred$Predicted )


# Analyze Order
PS_Order_ref <- data.frame(
  "Trial_Order" = seq(from = min(df_ProcessingSpeed_Clean$Trial_Order),                            to = max(df_ProcessingSpeed_Clean$Trial_Order),
                      length.out = 1000),
  #"ITI" = ITI_min,
  "ITI" = PS_ITI_pred$ITI[ITI_min],
  "Right_Bias" = rep("LEFT", 1000),
  "Previous_Response" = rep("NO", 1000),
  "Previous_RT" = rep(0, 1000))
PS_Order_pred =  estimate_response(model_PS, PS_Order_ref)

PS_Order_pred = cbind(PS_Order_ref, PS_Order_pred [,-c(1:3)])
Order_min = which.min(PS_Order_pred$Predicted )


#####################################################
# Plot and Summary
model_parameters(model_PS)

ggplot(PS_ITI_pred, aes(ITI, Predicted)) +
  geom_smooth()

ggplot(PS_Order_pred, aes(Trial_Order, Predicted)) +
  geom_smooth()

PS_results = data.frame(
  "ProcessingSpeed_n_Incorrect" = n_incorrect,
  "ProcessingSpeed_n_Outliers"= n_outliers,
  "ProcessingSpeed_n_Impulsive"= n_impulsive,

  "ProcessingSpeed_RT_Accuracy"= as.numeric(r2(model_PS)[1]), #R2, not adjusted
  "ProcessingSpeed_RT_Learning"= model_parameters(model_PS)$Coefficient[2]/sd(df_ProcessingSpeed_Clean$RT), #coef of Trial Order / sd of RT
  "ProcessingSpeed_RT_Learning_Significant"= model_parameters(model_PS)$p[2], #p-value of Trial Order
  "ProcessingSpeed_RT_Engagement"= model_parameters(model_PS)$Coefficient[4]/ sd(df_ProcessingSpeed_Clean$RT), #coef of ITI/sd of RT
  "ProcessingSpeed_RT_Engagement_Significant"= model_parameters(model_PS)$p[4],#p-value of ITI
  "ProcessingSpeed_RT_RightBias"= model_parameters(model_PS)$Coefficient[6]/sd(df_ProcessingSpeed_Clean$RT),#coef of Right_Bias (Right)/ sd of RT
  "ProcessingSpeed_RightBias_Significant"= model_parameters(model_PS)$p[6],#p-value of Right_Bias

  "ProcessingSpeed_RT_ITI_Optimal"= PS_ITI_pred$ITI[[ITI_min]],
  "ProcessingSpeed_RT"= PS_ITI_pred$Predicted[[ITI_min]],
  #"ProcessingSpeed_RT_SE"= PS_ITI_pred$##["mean_se"][iti_min], => need generate SE
  "ProcessingSpeed_RT_CI_low"= PS_ITI_pred$CI_low[[ITI_min]],
  "ProcessingSpeed_RT_CI_high"= PS_ITI_pred$CI_high[[ITI_min]],

  "ProcessingSpeed_RT_Raw_Mean"= mean(df_ProcessingSpeed_Clean$RT),
  "ProcessingSpeed_RT_Raw_SD"= sd(df_ProcessingSpeed_Clean$RT),

  "ProcessingSpeed_RT_Fatigue"= PS_Order_pred$Trial_Order[[Order_min]])
PS_results <- data.frame(t(PS_results))
names(PS_results)[1] <- "Values"


########################### RESPONSE SELECTION ########################

#####################################################
# Read data

#read_plus <- function(all_files) {
#  read_csv(all_files) %>%
#    mutate(filename = basename(all_files))
#}

df_ResponseSelection <-
  list.files(path = "../NumberTrialsCalibration/data/",
             pattern = "*_ResponseSelection.csv",
             full.names = TRUE) %>%
  map_df(~read_csv(.)[, -c(7,8)])

#####################################################
# Preprocessing

### Raw data
df_ResponseSelection <- df_ResponseSelection %>%
  mutate(Right_Bias = ifelse(Stimulus_Side == "RIGHT", "RIGHT", "LEFT")) %>%
  mutate(Previous_Response = ifelse(is.na(Previous_Response), "NO", "YES")) %>%
  mutate(Previous_RT = ifelse(Previous_Response == "YES", Previous_RT, 0)) %>%
  mutate(Error = ifelse(Response != Stimulus_Side, "YES", "NO")) %>%
  mutate(Error_Previous = lag(Error))

### Only accurate trials (for RT)

df_ResponseSelection_Correct <- df_ResponseSelection %>%
  filter(Error == "NO")

### Remve outliers
df_ResponseSelection_Clean <- df_ResponseSelection_Correct %>%
  mutate(Outlier_Score = as.numeric(check_outliers(RT, method = c("zscore", "iqr")))) %>%
  filter(!Outlier_Score >= 0.5) %>%
  select(- c(Outlier_Score, Error))

### Number of impulsive responses, correct and incorrect responses, outliers
n_impulsive = sum(df_ResponseSelection$Previous_Response == "YES")/ nrow(df_ResponseSelection)
n_correct = nrow(df_ResponseSelection_Correct)/nrow(df_ResponseSelection)
n_incorrect = (nrow(df_ResponseSelection) - nrow(df_ResponseSelection_Correct))/nrow(df_ResponseSelection)
n_outliers = (nrow(df_ResponseSelection_Correct) - nrow(df_ResponseSelection_Clean))/nrow(df_ResponseSelection_Correct)



#####################################################
# Stat models
if (length(which(df_ResponseSelection_Clean$Error_Previous == "YES"))/nrow(df_ResponseSelection_Clean) > 0.2) {
  model_RS <- lm(RT ~ poly(Trial_Order, 2) + poly(ITI, 2) + Right_Bias + Error_Previous, data = df_ResponseSelection_Clean)
} else if (length(which(df_ResponseSelection_Clean$Previous_Response == "YES"))/nrow(df_ResponseSelection_Clean) > 0.2) {
  model_RS <- lm(RT ~ poly(Trial_Order, 2) + poly(ITI, 2) + Right_Bias + Error_Previous + Previous_Response + Previous_Response:Previous_RT , data = df_ResponseSelection_Clean)
} else {
  model_RS <- lm(RT ~ poly(Trial_Order, 2) + poly(ITI, 2) + Right_Bias, data = df_ResponseSelection_Clean)
}

1+1
data <- data.frame(y = c(0,1,2,3,4),
                   x = c(0,1,2,3,4),
                   g1 = c("A","A","A","B","B"),
                   g2 = c("X","Y","X","Y","Y"))
model <- lm(y ~ x * g1 * g2, data = data)
summary(model)
parameters::model_parameters(model)

model <-
#df_ResponseSelection_Clean <-  data.frame(df_ResponseSelection_Clean)
#model_RS <- lm(RT ~ poly(Trial_Order, 2) + poly(ITI, 2) + Right_Bias, data = df_ResponseSelection_Clean)

#=> use Error_Prevous instead of Error

## Analyse ITI
RS_ITI_ref <- data.frame(
  "Trial_Order" = rep(1, 1000),
  "ITI" = seq(from = min(df_ResponseSelection_Clean$ITI),                                     to = max(df_ResponseSelection_Clean$ITI),                                      length.out = 1000),
  "Error_Previous" = rep("NO", 1000),
  "Right_Bias" = rep("LEFT", 1000),
  "Previous_Response" = rep("NO", 1000),
  "Previous_RT" = rep(0, 1000))
RS_ITI_pred =  estimate_response(model_RS, RS_ITI_ref)

#RS_ITI_pred = cbind(RS_ITI_ref, RS_ITI_pred [,-c(1:3)])
ITI_min = which.min(RS_ITI_pred$Predicted )


# Analyze Order
RS_Order_ref <- data.frame(
  "Trial_Order" = seq(from = min(df_ResponseSelection_Clean$Trial_Order),                            to = max(df_ResponseSelection_Clean$Trial_Order),
                      length.out = 1000),
  #"ITI" = ITI_min,
  "ITI" = RS_ITI_pred$ITI[ITI_min],
  "Error_Previous" = rep("NO", 1000),
  "Right_Bias" = rep("LEFT", 1000),
  "Previous_Response" = rep("NO", 1000),
  "Previous_RT" = rep(0, 1000))
RS_Order_pred =  estimate_response(model_RS, RS_Order_ref)

#RS_Order_pred = cbind(RS_Order_ref, RS_Order_pred [,-c(1:3)])
Order_min = which.min(RS_Order_pred$Predicted )


#####################################################
# Plot and Summary
model_parameters(model_RS)

ggplot(RS_ITI_pred, aes(ITI, Predicted)) +
  geom_smooth()

ggplot(RS_Order_pred, aes(Trial_Order, Predicted)) +
  geom_smooth()

RS_results = data.frame(
  "ResponseSelection_n_Incorrect" = n_incorrect,
  "ResponseSelection_n_Outliers"= n_outliers,
  "ResponseSelectiond_n_Impulsive"= n_impulsive,

  "ResponseSelection_RT_Accuracy"= as.numeric(r2(model_RS)[1]), #R2, not adjusted
  "ResponseSelection_RT_Learning"= model_parameters(model_RS)$Coefficient[2]/sd(df_ResponseSelection_Clean$RT), #coef of Trial Order / sd of RT
  "ResponseSelection_RT_Learning_Significant"= model_parameters(model_RS)$p[2], #p-value of Trial Order
  "ResponseSelection_RT_Engagement"= model_parameters(model_RS)$Coefficient[4]/ sd(df_ResponseSelection_Clean$RT), #coef of ITI/sd of RT
  "ResponseSelection_RT_Engagement_Significant"= model_parameters(model_RS)$p[4],#p-value of ITI
  "ResponseSelection_RT_RightBias"= model_parameters(model_RS)$Coefficient[6]/sd(df_ResponseSelection_Clean$RT),#coef of Right_Bias (Right)/ sd of RT
  "ResponseSelection_RightBias_Significant"= model_parameters(model_RS)$p[6],#p-value of Right_Bias

  "ResponseSelection_RT_ITI_Optimal"= RS_ITI_pred$ITI[[ITI_min]],
  "ResponseSelection_RT"= RS_ITI_pred$Predicted[[ITI_min]],
  #"ResponseSelection_RT_SE"= RS_ITI_pred$##["mean_se"][iti_min], => need generate SE
  "ResponseSelection_RT_CI_low"= RS_ITI_pred$CI_low[[ITI_min]],
  "ResponseSelection_RT_CI_high"= RS_ITI_pred$CI_high[[ITI_min]],

  "ResponseSelection_RT_Raw_Mean"= mean(df_ResponseSelection_Clean$RT),
  "ResponseSelection_RT_Raw_SD"= sd(df_ResponseSelection_Clean$RT),

  "ResponseSelection_RT_Fatigue"= RS_Order_pred$Trial_Order[[Order_min]],

  "SSRT_Min"= 16.66667,
  "SSRT_Max" = quantile(RS_Order_pred$Predicted, probs = 0.10))


RS_results <- data.frame(t(RS_results))
names(RS_results)[1] <- "Values"
























## Conlifct Monitoring
df_inhibition = read.csv("data/testJiaLi_ConflictResolution_2.csv", stringsAsFactors = FALSE)[]

df_condition <- df_inhibition %>%
  filter(RT < 1000) %>%
  select(Congruence, RT) %>%
  group_by(Congruence)

t.test(df_condition$RT[df_condition$Congruence == "CONGRUENT"], df_condition$RT[df_condition$Congruence == "INCONGRUENT"])

ggplot(df_condition, aes(Congruence, RT)) + geom_boxplot()

