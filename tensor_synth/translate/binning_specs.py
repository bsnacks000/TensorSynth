
'''
collection of utility methods that process midi/dur bin widths and labels at different sizes
these are used in encoder with pd.cut 


the results are saved to the encoder object's config json dictionary

'''

import string
import numpy as np
import re


def midi_bins4():
    return [i for i in range(0,127+32,32)]


def midi_labels4():
    return [string.ascii_lowercase[i] for i in range(4)]


def midi_bins8():
    return [i for i in range(0,127+16,16)]


def midi_labels8():
    return [string.ascii_lowercase[i] for i in range(8)]


def midi_bins16():
    return [i for i in range(0,127+8,8)]


def midi_labels16():
    return [string.ascii_lowercase[i] for i in range(16)]
    

def dur_bins12():
    return np.logspace(-1,1.25,12)
    

def dur_labels12():
    return [string.ascii_lowercase[i] for i in range(11)]


def get_binning_specs(index_obj):
    ''' 
    parses an index object with regex and returns a list of bin values
    :param: index_obj - a pd.Index object
    returns a list of tuples (specific ranges of each bin)
    '''
    bin_list = list(index_obj)

    bin_list = [re.findall('[-+]?\d+[\.]?\d*',i) for i in bin_list]

    for i in range(len(bin_list)):
        for j in range(len(bin_list[i])):
            bin_list[i][j] = float(bin_list[i][j])  # need float to account for continuous dur value specs
        

    return bin_list