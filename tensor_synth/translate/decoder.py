import pandas as pd
import json
import os
from abc import ABCMeta, abstractmethod


from tensor_synth.exceptions import *


class Decoder(object):

    """
    Decoder converts tensor_synth word format back to midi output for supercollider
    It reads in a unique json file with the correct binnings in order to unbin the corpus
    Midi values are chosen by generating a random number based on these bin widths
    
    :param: config_filepath - the json formatted config filepath
    """

    __metaclass__ = ABCMeta

    def __init__(self,word_series,config_filepath):
        
        self.word_series = word_series  #TODO check formatting errors
        self.config_filepath = config_file_path

        self.config = None
        self.output_df = None

        self.encoding_dict = None

    @abstractmethod
    def _import_config(self):

        pass # this needs to be overwritten for each subclass 

    @abstractmethod
    def _unbin_df(self):(self):
        
        pass


    @abstractmethod
    @staticmethod
    def unbin_callback(row, bin_data, col_name):

        pass

    def export_output_to_json(filepath):
        ''' exports the converted df'''

        #TODO check valid filepath
        #TODO to make sure formatting is correct
        
        self.output_df.to_json(filepath,orient='index')


class DecoderProxySynth(Decoder):
    """
    Subclass of Decoder with methods that are configured for the MidiGrain Proxy Synth Spec
    """

    def __init__(self, word_series, config_filepath)
        
        super().__init__(word_series, config_file_path)

        self.config = _import_config()
        self.encoding_dict = self.config['encodings']
    
    def _import_config(self):
        
        try:
            with open(self.config_file_path, 'r') as config_data:
                config = json.load(config_data)
            
            #TODO raise tsDecoderProxyException formatting errors here

        except tcDecoderProxyException as e:
            raise e

        return config

    @staticmethod
    def unbin_callback(row, bin_data, col_name):  #TODO error check/unittests
        
        inputs = [string.ascii_lowercase[i] for i in range(len(bin_data))]
        bin_indx = inputs.index(row[col_name])  # gets replaced with iterator
        low, high = bin_data[bin_indx][0], bin_data[bin_indx][1]
        
        if col_name == 'duration' or col_name == 'inter_event_duration':
            return np.random.uniform(low, high)
        
        return np.random.randint(low,high)


    def _unbin_df(self):
        '''
        builds the output df using the unbin callback
        '''

        #TODO check formatting

        for k,v in encoding_dict.items():
            if k == 'freq':
                continue

            self.output_df[k] = self.output_df.apply(unbin_int_callback,args=(v,k,),axis=1)
        
