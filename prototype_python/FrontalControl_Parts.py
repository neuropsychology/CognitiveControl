import datetime

import numpy as np
import pandas as pd
import neurokit as nk
import neuropsydia as n

from FrontalControl_Core import *
from FrontalControl_Utils import *

# -----------------------------------------------------------------------------
# Part 1
# -----------------------------------------------------------------------------
def processing_speed(n_trials=20):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}

    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    n.newpage((74,20,140), auto_refresh=False)
    n.write("One year ago...", color="white", y=1, size=1.5)
    n.refresh()
    n.time.wait(2000)
    n.write("...deep inside the REBEL territory...", color="white", y=-2, size=1.2)
    n.refresh()
    n.time.wait(2000)
    display_instructions("""The commander requires you to destroy all the incomming ennemies.\n\nNothing hard for our best pilot!\n\nJust destroy them as fast as your can with your auto-aiming cannons by pressing DOWN whenever an ennemy appears.""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(
                display_stimulus(side=data[trial]["Stimulus_Side"],
                                 always_right = True)
                )
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)






# Part 2
# -----------------------------------------------------------------------------
def response_selection(n_trials=20):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}

    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    n.newpage((74,20,140), auto_refresh=False)
    n.write("When suddenly...", color="white", y=1, size=1.2)
    n.refresh()
    n.time.wait(2000)
    n.write("...you get shoot from behind!", color="white", y=-2, size=1.3)
    n.refresh()
    n.time.wait(2000)
#    n.newpage((38,50,56))
    n.newpage("white")
    n.time.wait(2000)
    display_instructions("""You wake up in a hospital. One year has passed since the accident.\n\nSlowly, you discover that everything fell apart. You went from being the best pilot to nothing.\n\nYou soon learn that everybody turned their back on you.""", text_end="Press SPACE to continue.")
    display_instructions("""But you're going to show them!\n\nYou might start at the bottom of the ladder, you still are the fastest pilot of the galaxy!""", text_end="Press SPACE to continue.")
    display_instructions("""You started your career from the scratch.\n\nNo supercannons for now, you must aim and press LEFT or RIGHT depending on where the ennemy appears. Don't forget, you must be as fast as possible!""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"]))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)







# Part 3
# -----------------------------------------------------------------------------
def response_inhibition(n_trials=20, min_SSRT=0, max_SSRT=300, frame = 16.66667):

    def generate_data(n_trials, min_SSRT=0, max_SSRT=300, frame= 16.66667, adaptive=False):
        data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
                "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}

        # SSRT
        ss = np.array(randomize_and_repeat_without_repetition([False, False, False, True], int(n_trials/4)) + [False] * int(n_trials-int(n_trials/4)*4))
        data["Stop_Signal"] = ss
        data["Stop_Signal_RT"] = np.array([np.nan] * int(n_trials))

        if adaptive is False:
#            ssrt = generate_interval_frames(min_SSRT, max_SSRT, int(sum(ss)-int(sum(ss)/4)))
#            data["Stop_Signal_RT"][ss == True] = randomize_without_repetition([0] * int(sum(ss)/3) + list(ssrt))
            ssrt = generate_interval_frames(min_SSRT, max_SSRT, int(sum(ss)))
            data["Stop_Signal_RT"][ss == True] = randomize_without_repetition(list(ssrt))
        else:
            data["Stop_Signal_RT"][ss == True] = np.array([-1]*len(data["Stop_Signal_RT"][ss == True]))

        data = pd.DataFrame.from_dict(data)
        data = data.sample(len(data)).reset_index(drop=True)
        data = data.to_dict(orient="index")
        return(data)


    # First
    ITI(2000)
    display_ennemy()
    n.refresh()
    n.time.wait(150)
    display_ennemy(stop=True)
    n.refresh()
    if testmode is False:
        response, RT = n.response(allow=["RIGHT", "LEFT"], time_max = 1500)
        n.time.wait(1500)
    else:
        response, RT = "RIGHT", np.random.normal(750, 250)


    # Instructions
    display_instructions("""Wait! It seems that some CIVILIANS are present in some of the REBELS' ships.\n\nUnfortunately, our scanner can take some time to detect them.\n\nYour priority is still shoot the incomming ships as FAST as possible, but try avoiding shooting if you see a RED CROSS.\nBut between ourselves... fire at will and do not wait until the scan is complete.""")

    staircase = nk.staircase(signal = generate_interval_frames(0, max_SSRT, int(max_SSRT/frame)),
                             treshold = 0.5,
                             burn=0)

    # Without staircase
    data = generate_data(int(n_trials/2), min_SSRT, max_SSRT, frame)
    for trial in range(0, int(n_trials/2)):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"], stop=data[trial]["Stop_Signal_RT"]))
        if data[trial]["Stop_Signal"] is True:
            if data[trial]['RT'] >= data[trial]["Stop_Signal_RT"]:
                if data[trial]["Response"] == "Time_Max_Exceeded":
                    staircase.add_response(response=0, value=data[trial]["Stop_Signal_RT"])
                else:
                    staircase.add_response(response=1, value=data[trial]["Stop_Signal_RT"])
        data[trial]["Trial_Order"] = trial + 1

    # With staircase
    data_staircase = generate_data(int(n_trials/2), min_SSRT, max_SSRT, adaptive=True)
    for i in list(data_staircase.keys()): # Replace keys
        data_staircase[i + int(n_trials/2)] = data_staircase.pop(i)
    data.update(data_staircase)
    for trial in range(int(n_trials/2), n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        if data[trial]["Stop_Signal_RT"] == -1:
            data[trial]["Stop_Signal_RT"] = staircase.predict_next_value()
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"], stop=data[trial]["Stop_Signal_RT"]))
        if data[trial]["Stop_Signal"] is True:
            if data[trial]['RT'] >= data[trial]["Stop_Signal_RT"]:
                if data[trial]["Response"] == "Time_Max_Exceeded":
                    staircase.add_response(response=0, value=data[trial]["Stop_Signal_RT"])
#                    print('staircase.add_response(response=0, value=%f)' % data[trial]["Stop_Signal_RT"])
                else:
                    staircase.add_response(response=1, value=data[trial]["Stop_Signal_RT"])
#                    print('staircase.add_response(response=1, value=%f)' % data[trial]["Stop_Signal_RT"])
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data, staircase)








# Part 4
# -----------------------------------------------------------------------------
def attention_priming(n_trials=20):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}
    data["Priming_Interval"] = randomize_and_repeat(generate_interval_frames(50, 1000, n_trials/2), 2)
    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    display_instructions("""Well done! You're doing great. We are out the civilian zone, so NO CIVILIANS are to be expected from now on.\n\nFor your next mission, our engineers have improved your scanner, so we can detect from where the ennemies arrive from away!\n\nGive it a try, and show us again how FAST you are.""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(prime(side=data[trial]["Stimulus_Side"], duration=data[trial]["Priming_Interval"]))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"]))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)


# Part 5
# -----------------------------------------------------------------------------
def conflict_resolution(n_trials=20):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}
    data["Priming_Interval"] = randomize_and_repeat(generate_interval_frames(50, 1000, n_trials/2), 2)
    data["Conflict"] = randomize_and_repeat(generate_interval_frames(50, 1000, n_trials/2), 2)
    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    display_instructions("""Bad news! We have been informed the ennemies managed to hack our lateral radars. This means you can only trust your central radar (the central arrow).""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(prime(side=data[trial]["Stimulus_Side"], duration=data[trial]["Priming_Interval"]))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"]))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)