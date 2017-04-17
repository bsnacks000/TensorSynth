import pandas as pd
import json
import os
from abc import ABCMeta, abstractmethod


from tensor_synth.exceptions import *
import tensor_synth.translate.binning_specs as bspecs


class Decoder(object):

    """
    Decoder converts tensor_synth word format back to midi output for supercollider
    It reads in a unique json file with the correct binnings in order to unbin the corpus
    Midi values are chosen by generating a random number based on these bin widths
    
    :param: config_filepath - the json formatted config filepath
    """

    __metaclass__ = ABCMeta

    def __init__(self, config_filepath):
        
        pass


class DecoderProxySynth(Decoder):
    pass