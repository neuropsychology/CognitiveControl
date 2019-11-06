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
def processing_speed(n_trials=60, testmode = False):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}

    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    if testmode is False:
        n.newpage((24,4,64), auto_refresh=False)
        n.write("One year ago...", color="white", y=2, size=1.5)
        n.refresh()
        n.time.wait(1500)
        n.write("...deep inside the REBEL territory...", color="white", y=0, size=1.2)
        n.refresh()
        n.time.wait(2500)
        display_instructions("""Okay, pilot, here's the mission briefing.\n\nThe commander requires you to destroy all the incoming enemies... Nothing too hard for our best pilot!""", text_end="Press SPACE to continue.")
        display_instructions("""Just destroy them as fast as your can with your famous auto-aiming cannons.\n\nPress DOWN to shoot whenever an enemy appears.""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"], testmode = testmode))
        data[trial].update(
                display_stimulus(side=data[trial]["Stimulus_Side"],
                                 always_right = True,
                                 testmode = testmode)
                )
        data[trial]["Trial_Order"] = trial + 1

    # First
    ITI(1000)
    display_explosion(side = "CENTRE")
    n.refresh()
    n.time.wait(1000)

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)






# Part 2
# -----------------------------------------------------------------------------
def response_selection(n_trials=100, testmode = False):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}

    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    if testmode is False:
        n.newpage((24,4,64), auto_refresh=False)
        n.write("When suddenly...", color="white", y=5, size=1.2)
        n.refresh()
        n.time.wait(2000)
        n.write("...your ship engine EXPLODES!", color="white", y=3.5, size=1.2)
        n.refresh()
        n.time.wait(2500)
        n.newpage("white")
        n.time.wait(1000)
        n.newpage((24,4,64), auto_refresh=True)
        n.time.wait(1000)
        n.write("You wake up in a hospital.", color="white", y=5, size=1.2)
        n.refresh()
        n.time.wait(1500)
        n.write("One year has passed since the accident.", color="white", y=3.5, size=1.2)
        n.refresh()
        n.time.wait(3000)
        display_instructions("""Things have changed, since. You find your dear old ship, and its famous auto-aiming cannons, damaged in a dump.\n\nYou have no choice but to start again, in this new can box they call a ship...\n\nNo more auto-aiming cannons.""", text_end="Press SPACE to continue.", background = (24,4,64))
        display_instructions("""But you're not going to give up! You're going to show everyone that you are the fastest pilot for a reason...\n\nEven if that means manually aiming at the targets!""", text_end="Press SPACE to continue.", background = (24,4,64))
        display_instructions("""Okay, rookie, get ready for action.\n\nPress LEFT or RIGHT depending on where the enemy appears, and be as fast as possible!""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"], testmode = testmode))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"], testmode = testmode))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)







# Part 3
# -----------------------------------------------------------------------------
def response_inhibition(n_trials=200, min_SSRT=0, max_SSRT=300, frame = 16.66667, testmode = False):

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
    display_enemy()
    n.refresh()
    n.time.wait(150)
    display_enemy(stop=True)
    n.refresh()
    if testmode is False:
        response, RT = n.response(allow=["RIGHT", "LEFT"], time_max = 1500)
        n.time.wait(1500)
    else:
        response, RT = "RIGHT", np.random.normal(750, 250)


    # Instructions
    n.newpage((24,4,64), auto_refresh=False)
    n.write("Wait! What's that?!", color="white", y=5, size=1.2)
    n.refresh()
    n.time.wait(2000)
    display_instructions("""Bad news, rookie, it seems like the rebels have upgraded some of their ships!\n\nIf we do not manage to shoot as SOON as the ennemy appears, they'll have time to activate counter-measures that will return our bullets and damage our ship.""", text_end="Press SPACE to continue.")
    display_instructions("""Shoot the incoming ships as FAST as possible, before a RED CROSS appears.\n\nDo not shoot at the RED CROSS, or it will harm us too!""")

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
                else:
                    staircase.add_response(response=1, value=data[trial]["Stop_Signal_RT"])
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
    n.newpage((24,4,64), auto_refresh=False)
    n.write("Well done! You're doing great!", color="white", y=5, size=1.5)
    n.refresh()
    n.time.wait(2000)
    display_instructions("""Our engineers have worked hard over the past months. We are now able to prevent the rebels' ships from gathering power. \n\nSo no more RED CROSS!""", text_end ="Press SPACE to continue.")
    display_instructions("""For your next mission, our engineers have also improved your radar. We can now predict the position of the rebels' ships even before they emerge!\n\nThis new technology is going to help you improve your speed significantly.\n\nGive it a try, and show us again how FAST you are.""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(prime(side=data[trial]["Stimulus_Side"], duration=data[trial]["Priming_Interval"]))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"]))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)


# Part 5
# -----------------------------------------------------------------------------
#def conflict_resolution(n_trials=20):
#
#    # Data creation
#    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
#            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}
#    data["Priming_Interval"] = randomize_and_repeat(generate_interval_frames(50, 1000, n_trials/2), 2)
#    data["Congruence"] = randomize_and_repeat(generate_interval_frames(50, 1000, n_trials/2), 2)
#    data = pd.DataFrame.from_dict(data)
#    data = data.sample(len(data)).reset_index(drop=True)
#    data = data.to_dict(orient="index")
#
#    # Instructions
#    n.newpage((74,20,140), auto_refresh=False)
#    n.write("Bad news! We have been informed the ennemies", color="white", y=5, size=1.2)
#    n.refresh()
#    n.write("have managed to hack our radars.", color="white", y=3.5, size=1.2)
#    n.refresh()
#    n.time.wait(5000)
#    display_instructions("""This means from now on, you can only trust your central radar (the central arrow). Be on your toes and destroy those incoming ships as FAST as you can.""")
#
#    for trial in range(n_trials):
#        data[trial].update(ITI(data[trial]["ITI"]))
#        data[trial].update(prime(side=data[trial]["Stimulus_Side"], duration=data[trial]["Priming_Interval"], congruence = "INCONGRUENT"))
#        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"]))
#        data[trial]["Trial_Order"] = trial + 1
#
#    data = pd.DataFrame.from_dict(data, orient="index")
#    return(data)


# Part 6
# -----------------------------------------------------------------------------
def conflict_resolution(n_trials=200):

    # Congruent practice
    # Instructions
    display_instructions("""Impressive job, pilot!\n\nWe are winning this war! But the rebels are smart. This time, they have disguised themselves as CIVILIANS.\n\nThankfully, our engineers have developed a radar that will point toward the enemy ship.""", text_end ="Press SPACE to continue.")
    display_instructions("""Shoot LEFT and RIGHT according to the radar arrows that will appear in the centre.\n\nRemember to be as fast as possible!""", text_end ="Press SPACE to continue.")
    for practice_trial in range(7):
        ITI([1000, 1250, 1000, 1500, 1000, 1250, 1500][practice_trial])
        prime(side=["RIGHT", "LEFT", "RIGHT", "RIGHT", "LEFT", "LEFT", "RIGHT"][practice_trial], congruence="CONGRUENT", duration = 0)
        display_stimulus(side=["RIGHT", "LEFT", "RIGHT", "RIGHT", "LEFT", "LEFT", "RIGHT"][practice_trial], allies = True)



    # Data creation
    data = {"Conflict": [False]*int(n_trials/2) + [True]* int(n_trials/2),
            "Stimulus_Side": ["RIGHT", "LEFT"]*int(n_trials/2) ,
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}
    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    display_instructions("""You're doing great!\n\nUnfortunately, it seems that they found a way a way of hacking our lateral radar antennas. You can only trust and rely on the CENTRAL arrow to know the direction to shoot at.""", text_end ="Press SPACE to continue.")
    display_instructions("""Shoot LEFT and RIGHT according to the CENTRAL radar arrow.\n\nRemember to be as fast as possible!""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(prime(side=data[trial]["Stimulus_Side"], conflict=data[trial]["Conflict"], duration = 0))

        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"], allies = True))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)