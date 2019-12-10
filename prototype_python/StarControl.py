import os
import numpy as np
import pandas as pd
import datetime

import neuropsydia as n

from StarControl_Utils import *
from StarControl_Core import *
from StarControl_Parts import *
from StarControl_Statistics import *


# Parameters
testmode = False
staircase = False
n_trials = {"P1": 60, "P2": 80, "P3": 160, "P4": 160}
#n_trials = {"P1": 6, "P2": 6, "P3": 30, "P4": 6}

# Initialization
n.start()
t0 = datetime.datetime.now()
results = {}

# Identification
if testmode is True:
    participant = "test"
else:
    n.newpage((74,20,140))
    n.write("STAR CONTROL", y = 1.5, color = "white", size = 3)
    participant = n.ask("ID: ", x = -1, y = -3, color = "white", background = (74,20,140), size = 1.5)

# Create data folder
path = './data/' + participant + "/"
if os.path.exists(path) is False:
    os.mkdir(path)


# Instructions (can be activated to increase the pressure in the context of experiments with students)
n.instructions("This is a game designed to measure how fast your are, as speed has been shown to a reliable index of intellectual ability and mental agility.\n\nThe task is repetitive and long on purpose, as the ability of maintaining speed until the end is also an indicator of cognitive altertness and aptitude.\n\nHence, throughout the game, we would like you to try responding as fast as possible.", size=0.8, end_text="Press ENTER to start the game.")

# Part 1
# -----------------------------------------------------------------------------
start_time = datetime.datetime.now()
df_ProcessingSpeed = processing_speed(n_trials=n_trials["P1"], testmode = testmode)
save_data(df_ProcessingSpeed, start_time, participant, task = "Processing_Speed", path = path + participant + "_ProcessingSpeed")


# Part 2
# -----------------------------------------------------------------------------
start_time = datetime.datetime.now()
df_ResponseSelection = response_selection(n_trials=n_trials["P2"], testmode = testmode)
save_data(df_ResponseSelection, start_time, participant, task = "Response_Selection", path =path + participant + "_ResponseSelection")



# Part 3
# -----------------------------------------------------------------------------
results["SSRT_Min"] = 0
#results["SSRT_Max"] = convert_to_frames(df_ResponseSelection["RT"].quantile(0.10))
results["SSRT_Max"] = convert_to_frames(df_ResponseSelection["RT"].median())


start_time = datetime.datetime.now()
df_ResponseInhibition = response_inhibition(n_trials=n_trials["P3"],
                                            min_SSRT=results["SSRT_Min"],
                                            max_SSRT=results["SSRT_Max"],
                                            testmode = testmode)
save_data(df_ResponseInhibition, start_time, participant, task = "Response_Inhibition", path = path + participant + "_ResponseInhibition")



# Part 4
# -----------------------------------------------------------------------------
start_time = datetime.datetime.now()
df_ConflictResolution = conflict_resolution(n_trials=n_trials["P4"],
                                            testmode = testmode)
save_data(df_ConflictResolution, start_time, participant, task = "Conflict_Resolution", path = path + participant + "_ConflictResolution")


## Part 5
## -----------------------------------------------------------------------------
#start_time = datetime.datetime.now()
#df_AttentionPriming = attention_priming(n_trials=20)
#save_data(df_AttentionPriming, start_time, participant, task = "Attention_Priming", path = path + participant + "_AttentionPriming")


n.instructions("Thank you!", end_text="Press ENTER to quit.")
n.close()