import datetime

import numpy as np
import pandas as pd
import neuropsydia as n

from StarControl_Utils import *


# =============================================================================
# Parameters
# =============================================================================
testmode = False




# =============================================================================
# CORE
# =============================================================================
def display_background():
    n.newpage((38,50,56), auto_refresh=False)

def display_explosion(side="RIGHT"):
    if side == "RIGHT":
        n.image("assets/explosion.png", x=5, y=6.5, size=5)
    elif side == "LEFT":
        n.image("assets/explosion.png", x=-5, y=6.5, size=5)
    elif side == "CENTRE":
        n.image("assets/explosion.png", x=0, y=-8, size=7)

def display_enemy(side="RIGHT", stop=False, allies = False):
    if side == "RIGHT":
        if allies is False:
            if stop is True:
                n.image("assets/enemy_stop.png", x=5, y=6.5, size=3)
            else:
                n.image("assets/enemy.png", x=5, y=6.5, size=3)
        if allies is True:
            n.image("assets/enemy.png", x=5, y=6.5, size=3)
            n.image("assets/enemy.png", x=-5, y=6.5, size=3)
    elif side == "LEFT":
        if allies is False:
            if stop is True:
                n.image("assets/enemy_stop.png", x=-5, y=6.5, size=3)
            else:
                n.image("assets/enemy.png", x=-5, y=6.5, size=3)
        if allies is True:
            n.image("assets/enemy.png", x=5, y=6.5, size=3)
            n.image("assets/enemy.png", x=-5, y=6.5, size=3)

def display_ship():
    n.image("assets/spaceship.png", x=0, y=-8, size=3)

def display_fire(side="RIGHT"):
    if side == "RIGHT":
        n.image("assets/fire.png", x=0.65, y=-7.75)
    elif side == "LEFT":
        n.image("assets/fire.png", x=-0.65, y=-7.75)

def display_instructions(text="text instructions", text_end="Shoot to start the mission.", background = (13,71,161)):
    n.newpage(background, auto_refresh=False)
    n.write("\n\n\n" + text, color="white", long_text = True)
    n.write(text_end, color="white", y=-9)
    n.refresh()
    n.response(allow=["DOWN", "RIGHT", "LEFT", "SPACE"])

def display_cue(side="RIGHT", conflict=False):
    if side == "RIGHT":
        if conflict is False:
            angle = 0
            angle_sides = 0
        elif conflict is True:
            angle = 0
            angle_sides = 180
    else:
        if conflict is False:
            angle = 180
            angle_sides = 180
        elif conflict is True:
            angle = 180
            angle_sides = 0

    n.image("assets/arrow_green.png", x=-2, y=6.5, size=1.75, rotate=angle_sides)
    n.image("assets/arrow_green.png", x=-1, y=6.5, size=1.75, rotate=angle_sides)
    n.image("assets/arrow_green.png", x=0, y=6.5, size=1.75, rotate=angle)
    n.image("assets/arrow_green.png", x=1, y=6.5, size=1.75, rotate=angle_sides)
    n.image("assets/arrow_green.png", x=2, y=6.5, size=1.75, rotate=angle_sides)
    n.refresh()












# =============================================================================
# BASIC
# =============================================================================
def ITI(duration=1000, testmode = False):
    display_background()
    display_ship()
    n.refresh()
    time = datetime.datetime.now()
    response = np.nan
    RT = np.nan
    if testmode is False:
        while(datetime.datetime.now() - time).total_seconds()*1000 < duration:
            current_response = n.response(time_max = duration - (datetime.datetime.now() - time).total_seconds()*1000, get_RT=False)
            if(current_response != "Time_Max_Exceeded"):
                response = str(current_response)
                RT = datetime.datetime.now()
    if isinstance(RT, datetime.datetime):
        return({"Previous_Response": response,
                "Previous_RT": -1*(datetime.datetime.now() - RT).total_seconds()*1000})
    else:
        return({"Previous_Response": response,
                "Previous_RT": RT})



def display_stimulus(side="RIGHT", always_right = False, allies = False, stop = np.nan, time_max = 1500, testmode = False):
    if stop == 0:
        if allies is False:
            display_enemy(side=side, stop=True)
        elif allies is True:
            display_enemy(side=side, stop=True, allies = True)
    else:
        if allies is False:
            display_enemy(side=side)
        elif allies is True:
            display_enemy(side=side, allies = True)
    n.refresh()
    time = datetime.datetime.now()
    if always_right is True:
        if testmode is False:
            response, RT = n.response(allow="DOWN", time_max = time_max)
        else:
            response, RT = "DOWN", np.random.normal(750, 250)
        display_fire(side=side)
        display_explosion(side=side)
    else:
        if np.isnan(stop) or stop == 0:
            if testmode is False:
                response, RT = n.response(allow=["LEFT", "RIGHT"], time_max = time_max)
            else:
                response, RT = np.random.choice(["LEFT", "RIGHT"]), np.random.normal(750, 250)
        else:
            if testmode is True:
                response = np.random.choice(["LEFT", "RIGHT", np.nan])
                if pd.isna(response):
                    RT = np.nan
                else:
                    RT = np.random.normal(750, 250)
            else:
                RT = 0
                response, RT = n.response(allow=["LEFT", "RIGHT"], time_max = stop)
                if response not in ["LEFT", "RIGHT"]:
                    display_enemy(side=side, stop=True)
                    n.refresh()
                    response, RT = n.response(allow=["LEFT", "RIGHT"], time_max = time_max - stop)
                    RT += stop

    if response in ["LEFT", "RIGHT", "DOWN"]:
        display_fire(side=response)
        display_explosion(side=response)

    if testmode is False:
        if response in ["LEFT", "RIGHT", "DOWN"]:
            n.refresh()
            n.time.wait(200)
    return({"Response": response,
            "RT": RT,
            "Trial_Time_Onset": time,
            "Trial_Time_End": datetime.datetime.now()})


def prime(side="RIGHT", duration=1000, conflict=False):
    display_background()
    display_ship()
    display_cue(side=side, conflict=conflict)
    n.refresh()
    time = datetime.datetime.now()
    response = np.nan
    RT = np.nan
    if testmode is False:
        while(datetime.datetime.now() - time).total_seconds()*1000 < duration:
            current_response = n.response(time_max = duration - (datetime.datetime.now() - time).total_seconds()*1000, get_RT=False)
            if(current_response != "Time_Max_Exceeded"):
                response = str(current_response)
                RT = datetime.datetime.now()
    if isinstance(RT, datetime.datetime):
        return({"Cue_Response": response,
                "Cue_Response_RT": -1*(datetime.datetime.now() - RT).total_seconds()*1000})
    else:
        return({"Cue_Response": response,
                "Cue_Response_RT": RT})