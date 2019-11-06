import numpy as np
import pandas as pd
import neurokit as nk
import datetime
import random

def random_number(mini=0, maxi=0, n=1, seed=None):
    if seed is not None:
        random.seed(seed)
    if isinstance(mini, list):
        maxi = mini[1]
        mini = mini[0]
    return(np.random.uniform(mini, maxi, n))

def random_choice(choices, n=1, replace=True, probability=None, seed=None):
    if seed is not None:
        random.seed(seed)
    return(np.random.choice(choices, n, replace, probability))

def randomize(x):
    np.random.shuffle(x)
    return(x)


"""
>>> x = [1, 3, 2, 3, 3, 2, 1, 5]
>>> check_if_repetitions(x)
"""
def check_if_repetitions(x):
    x.sort()
    for i in range(len(x)-1):
       if x[i] == x[i+1]:
          return(True)
    return(False)


"""
>>> x = [1, 3, 2, 3, 4, 2, 2, 1, 5]
>>> randomize_without_repetition(x)
"""
def randomize_without_repetition(x, max_iter=10):
    x = list(x)
    randomized = [np.random.choice(x)]
    x.remove(randomized[0])
    for i in range(len(x)):
        candidate = np.random.choice(x)
        for j in range(max_iter):
            if candidate == randomized[len(randomized)-1]:
                candidate = np.random.choice(x)
            else:
                break
        randomized += [candidate]
        x.remove(candidate)
    return(randomized)



def randomize_and_repeat(x, n=2):
    new = []
    for i in range(n):
        new += list(randomize(x))
    return(new)


"""
>>> x = [1, 2, 3]
>>> randomize_and_repeat_without_repetition(x, n=3)
"""
def randomize_and_repeat_without_repetition(x, n=2):

    new = []
    for i in range(n):
        candidate = list(randomize_without_repetition(x))
        if len(new) == 0:
            new = candidate
        else:
            while new[len(new)-1] == candidate[0]:
                candidate = list(randomize_without_repetition(x))
            new += candidate
    return(new)




def generate_interval_frames(mini, maxi, n=10, frame=16.6666667):
    x = np.linspace(np.round(mini/frame), np.round(maxi/frame), int(n), endpoint = True)
    x = np.round(x)*frame
    return(x)



def convert_to_frames(x, frame=16.6666667):
    x = np.round(x/frame)
    return(x*frame)


def save_data(data, start_time, participant, task, path):
    data["Duration"] = (datetime.datetime.now() - start_time).total_seconds() / 60
    data["Participant"] = participant
    data["Task"] = task
    data.to_csv(path + ".csv", index=False)
    data.to_excel(path + ".xlsx", index=False)