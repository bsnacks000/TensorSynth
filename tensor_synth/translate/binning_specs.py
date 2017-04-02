
'''
collection of utility methods that process midi/dur bin widths and labels at different sizes
these are used in encoder with pd.cut and the results are saved to the encoder object's config json dictionary

'''

import string
import numpy as np


def midi_bins4():
    return [i for i in range(0,127,32)]

def midi_labels4():
    return [string.ascii_lowercase[i] for i in range(3)]

def midi_bins8():
    return [i for i in range(0,127,16)]

def midi_labels8():
    return [string.ascii_lowercase[i] for i in range(7)]

def midi_bins16():
    return [i for i in range(0,127,8)]

def midi_labels16():
    return [string.ascii_lowercase[i] for i in range(15)]
    
def dur_bins12():
    return np.logspace(-1,1.25,12)
    
def dur_labels12():
    return [string.ascii_lowercase[i] for i in range(11)]



