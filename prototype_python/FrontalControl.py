import numpy as np
import pandas as pd
import datetime

import neuropsydia as n

from FrontalControl_Utils import *
from FrontalControl_Core import *
from FrontalControl_Parts import *
from FrontalControl_Statistics import *

n.start()

t0 = datetime.datetime.now()

results = {}



df_ProcessingSpeed = processing_speed(n_trials=6)
df_ProcessingSpeed.to_csv("../data/S1_ProcessingSpeed.csv", index=False)
try:
    results.update(process_processing_speed(df_ProcessingSpeed))
except:
    print("Error: Couldn't process Processing Speed (p1) data")




df_ResponseSelection = response_selection(n_trials=4)
df_ResponseSelection.to_csv("../data/S1_ResponseSelection.csv", index=False)
try:
    results.update(process_response_selection(df_ResponseSelection))
except:
    print("Error: Couldn't process Response Selection (p2) data")
    results["SSRT_Min"] = 16.66667
    results["SSRT_Max"] = df_ResponseSelection["RT"].quantile(0.10)






df_ResponseInhibition, staircase = response_inhibition(n_trials=40,
                                            min_SSRT=results["SSRT_Min"],
                                            max_SSRT=results["SSRT_Max"])
df_ResponseInhibition.to_csv("../data/S0_ResponseInhibition.csv", index=False)
try:
    results.update(process_response_selection(df_ResponseInhibition))
except:
    print("Error: Couldn't process Response Inhibition (p3) data")




df_AttentionPriming = attention_priming(n_trials=20)
df_AttentionPriming.to_csv("../data/S0_AttentionPriming.csv", index=False)
#try:
#    results.update(process_attention_priming(df_AttentionPriming))
#except:
#    print("Error: Couldn't process Attention Priming (p4) data")



print("Duration: %0.2f min" %((datetime.datetime.now()-t0).total_seconds()/60))

n.close()