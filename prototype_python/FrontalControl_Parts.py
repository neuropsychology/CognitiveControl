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
def processing_speed(n_trials=6):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}

    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    n.newpage((74,20,140), auto_refresh=False)
    n.write("One year ago...", color="white", y=5, size=1.5)
    n.refresh()
    n.time.wait(2000)
    n.write("...deep inside the REBEL territory...", color="white", y=3, size=1.2)
    n.refresh()
    n.time.wait(2000)
    n.newpage((74,20,140), auto_refresh=False)
    n.write("The commander requires you to destroy", color="white", y=5, size=1.2)
    n.refresh()
    n.write("all the incomming ennemies.", color="white", y=3.5, size=1.2)
    n.refresh()
    n.time.wait(4000)
    n.write("Nothing is hard for our best pilot!", color="white", y=-3, size=1.2)
    n.refresh()
    n.time.wait(3000)
    #display_instructions("""The commander requires you to destroy all the incomming ennemies.\n\nNothing is hard for our best pilot!""", text_end="Press SPACE to continue.")
    display_instructions("""Just destroy them as fast as your can with your auto-aiming cannons. \n\nPress DOWN to shoot whenever an ennemy appears.""")

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
def response_selection(n_trials=4):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}

    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    n.newpage((74,20,140), auto_refresh=False)
    n.write("When suddenly...", color="white", y=5, size=1.2)
    n.refresh()
    n.time.wait(2000)
    n.write("...you get shot from behind!", color="white", y=3.5, size=1.2)
    n.refresh()
    n.time.wait(2000)
#    n.newpage((38,50,56))
    n.newpage("white")
    n.time.wait(2000)
    n.newpage((74,20,140), auto_refresh=False)
    n.write("You wake up in a hospital.", color="white", y=5, size=1.2)
    n.refresh()
    n.time.wait(1500)
    n.write("One year has passed since the accident.", color="white", y=3.5, size=1.2)
    n.refresh()
    n.time.wait(3000)
    n.newpage((74,20,140), auto_refresh=False)
    n.write("Slowly, you discover that your", color="white", y=5, size=1.2)
    n.refresh()
    n.write("supercannon has been damaged.", color="white", y=3.5, size=1.2)
    n.refresh()
    n.time.wait(4000)
    n.write("No more automated aiming.", color="white", y=0.5, size=1.3)
    n.refresh()
    n.time.wait(3000)
    #display_instructions("""You wake up in a hospital. One year has passed since the accident. Slowly, you discover that your supercannon has been damaged. No more automated aiming.""", text_end="Press SPACE to continue.")
    display_instructions("""But you're going to show everyone that you are the best pilot for a reason. \n\n You might have to manually aim at target, but you will still be the fastest pilot of the galaxy!""", text_end="Press SPACE to continue.")
    display_instructions("""For now, you must manualy aim by pressing LEFT or RIGHT depending on where the ennemy appears. \n\nDon't forget, you must be as fast as possible!""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"]))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)







# Part 3
# -----------------------------------------------------------------------------
def response_inhibition(n_trials=40, min_SSRT=0, max_SSRT=300, frame = 16.66667):

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
    n.newpage((74,20,140), auto_refresh=False)
    n.write("Wait! It seems like the the rebels", color="white", y=5, size=1.2)
    n.refresh()
    n.write("have upgraded their ships!", color="white", y=3.5, size=1.2)
    n.refresh()
    n.time.wait(3000)
    n.newpage((74,20,140), auto_refresh=False)
    n.write("If we do not manage to shoot the", color="white", y=5, size=1.2)
    n.refresh()
    n.write("incoming ships as SOON as they appear,", color="white", y=3.5, size=1.2)
    n.refresh()
    n.time.wait(3000)
    n.write("they will be able to gather enough power", color="white", y=2, size=1.2)
    n.refresh()
    n.time.wait(3000)
    n.write("to cause a big enough explosion", color="white", y=0.5, size=1.2)
    n.refresh()
    n.write("to damage our ships when they are shot.", color="white", y=-1, size=1.2)
    n.refresh()
    n.time.wait(4000)
    #display_instructions("""If we do not manage to shoot the incoming ships as SOON as they appear, the rebels' ships will have time to gather enough power and cause a big enough explosion to damage our ships when they are shot""", text_end="Press SPACE to continue.")
    display_instructions("""Therefore, your task is to shoot the incomming ships as FAST as possible. \n\nBut try to avoid shooting if you see a RED CROSS as a RED CROSS signifies that the rebels' ships have gathered enough power and attacking the rebels' ships will harm ours too.""")

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
    n.newpage((74,20,140), auto_refresh=False)
    n.write("Well done! You're doing great!", color="white", y=5, size=1.5)
    n.refresh()
    n.time.wait(2000)
    n.newpage((74,20,140), auto_refresh=False)
    n.write("Our engineers have worked hard over the past months.", color="white", y=5, size=1.2)
    n.refresh()
    n.time.wait(2000)
    n.write("We are now able to prevent the", color="white", y=3.5, size=1.2)
    n.refresh()
    n.write("rebels' ships from gathering power.", color="white", y=2, size=1.2)
    n.refresh()
    n.time.wait(3000)
    n.write("So no more RED CROSS from now on!", color="white", y=0, size=1.2)
    n.refresh()
    n.time.wait(3000)
    #display_instructions("""Our engineers have worked hard over the past months. We are now able to prevent the rebels' ships from gathering power. So no more RED CROSS!""", text_end ="Press SPACE to continue.")
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
    n.newpage((74,20,140), auto_refresh=False)
    n.write("Bad news! We have been informed the ennemies", color="white", y=5, size=1.2)
    n.refresh()
    n.write("have managed to hack our radars.", color="white", y=3.5, size=1.2)
    n.refresh()
    n.time.wait(5000)
    display_instructions("""This means from now on, you can only trust your central radar (the central arrow). Be on your toes and destroy those incoming ships as FAST as you can.""")

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(prime(side=data[trial]["Stimulus_Side"], duration=data[trial]["Priming_Interval"], congruency = "INCONGRUENT"))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"]))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)


# Part 6
# -----------------------------------------------------------------------------
def conflict_resolution_2(n_trials=20):

    # Data creation
    data = {"Stimulus_Side": ["RIGHT"]*int(n_trials/2) + ["LEFT"]* int(n_trials/2),
            "Congruency": ["CONGRUENT"]*int(n_trials/2) + ["INCONGRUENT"]* int(n_trials/2),
            "ITI": list(generate_interval_frames(500, 1500, n_trials/2))*2}
    data["Priming_Interval"] = randomize_and_repeat(generate_interval_frames(50, 1000, n_trials/2), 2)
    #data["Conflict"] = randomize_and_repeat(generate_interval_frames(50, 1000, n_trials/2), 2)
    data = pd.DataFrame.from_dict(data)
    data = data.sample(len(data)).reset_index(drop=True)
    data = data.to_dict(orient="index")

    # Instructions
    #n.newpage((74,20,140), auto_refresh=False)
    #n.write("Bad news! We have been informed the ennemies", color="white", y=5, size=1.2)
    #n.refresh()
    #n.write("have managed to hack our radars.", color="white", y=3.5, size=1.2)
    #n.refresh()
    #n.time.wait(5000)
    display_instructions("""Our talented engineers have been able to partly deal with the rebels' hacking of our radar. \n\nHowever, the solution is still very unstable and therefore, the rebels can still interfere with the radar occasionally. \n\nGo out there and show the rebels that nothing can stop you from destroying them at FAST as ever. """)

    for trial in range(n_trials):
        data[trial].update(ITI(data[trial]["ITI"]))
        data[trial].update(prime(side=data[trial]["Stimulus_Side"], duration=data[trial]["Priming_Interval"], congruency=data[trial]["Congruency"]))
        data[trial].update(display_stimulus(side=data[trial]["Stimulus_Side"]))
        data[trial]["Trial_Order"] = trial + 1

    data = pd.DataFrame.from_dict(data, orient="index")
    return(data)