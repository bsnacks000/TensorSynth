import pandas as pd
import json
import os
from abc import ABCMeta, abstractmethod


from tensor_synth.exceptions import *
import tensor_synth.translate.binning_specs as bspecs


class Encoder(object):
    """
    Abstract Base class for tensor_synth Encoder objects
    Subclasses are instantiated from this class that adhere to specific IO specs
    :param: scjson_filepath: path to the sc input raw data file in json format

    must overwrite _import_json(), _set_decoder_config(), _create_binned_df() in subclass
    """

    __metaclass__ = ABCMeta

    def __init__(self, scjson_filepath):

        # initialize all values
        self.scjson_filepath = scjson_filepath
        self.decoder_config = {
            'path': self.scjson_filepath, 
            'type':None, 
            'encodings':{},
            'word_sequence': None
        }    

        self.df_raw = None
        
        self.binned_df = None
        self.output_seq = None

    @abstractmethod
    def _import_json(self):

        pass # this needs to be overwritten for each subclass

    @abstractmethod
    def _set_decoder_config(self):

        pass # this needs to be overwritten for each subclass

    @abstractmethod
    def _create_binned_df(self):
        '''
        creates the binned_df for synth_type=proxy
        '''
        pass  # this needs to be overwritten in subclass


    def _clean_timestamps(self):
        '''
        cleans the raw df input file by calculating the duration and interevent time for each entry
        '''

        #calculate duration: noteOn[i] - noteOff[i]
        self.df_raw['duration'] = self.df_raw.apply(lambda row: row['noteOff_timestamp'] - row['noteOn_timestamp'],axis=1)

        # calculate interevent duration (wait time between events): noteOn[i] - noteOn[i-1] ...
        # shifting and then dividing by -1 
        self.df_raw['inter_event_duration'] = (self.df_raw['noteOn_timestamp'] - self.df_raw['noteOn_timestamp'].shift(-1))/ -1

        # timestamps no longer needed
        self.df_raw = self.df_raw.drop(['noteOn_timestamp','noteOff_timestamp'],axis=1)


    def _create_output_seq(self):

        '''
        concatenates all columns to form a tensor_synth 'word' sequence as a pd.Series object
        '''
        word_series = self.binned_df.iloc[:,0].astype(str) + '_' # freq first then string of categories 
        
        for i in range(1, len(self.binned_df.columns)):
            word_series += self.binned_df.iloc[:,i].astype(str)

        self.decoder_config['word_sequence'] = list(word_series) # store as plain list in json 
            
        return word_series

    def make_config_json(self, output_filepath):
        
        # TODO need to test valid file path - raise error if invalid
        # TODO need to test to make sure config format is correct or raise custom exception

        with open(output_filepath, 'w') as f:
            json.dump(self.decoder_config, f)


    def get_output_seq(self):
        # TODO possibly check here to make sure output series is valid 
        return self.output_seq

    def get_encodings(self):
        # TODO possibly check here to make sure encodings is valid
        return decoder_config['encodings']



class EncoderProxySynth(Encoder):

    '''
    imports and bins according to the midi_grain_proxy specification
    exports 
    :param: scjson_filepath - 

    '''

    def __init__(self, scjson_filepath):

        super(EncoderProxySynth,self).__init__(scjson_filepath)  # initialize super class

        #set all values
        self.decoder_config['type'] = 'midi_grain_proxy'
        
        self.df_raw = self._import_json(self.scjson_filepath)
        
        self._clean_timestamps()
        self._set_decoder_config()

        self.binned_df = self._create_binned_df()    
        self.output_seq = self._create_output_seq()


    def _import_json(self, json_filepath):
        
        try:

            df_raw = pd.read_json(json_filepath,orient='index') \
                .sort_values('noteOn_timestamp') \
                .drop('id',axis=1) \
                .reset_index(drop=True)

            # TODO check formatting here and adhere to synth_type=proxy specs raise tsRawInputFormattingExc

        except tsRawInputFormattingException as err:
            print('error handling stuff here')        
            raise   # will re-raise this exception and halt execution

        return df_raw


    def _set_decoder_config(self):    
        ''' store the original ranged values of binnings... this data is used by a Decoder object to retranslate to midi format '''

        # this covers all except freq which are left as integers for now...
        self.decoder_config['encodings']['amp'] = bspecs.get_binning_specs(pd.cut(self.df_raw['amp'], bspecs.midi_bins4()).cat.categories)
        self.decoder_config['encodings']['freq_dev'] = bspecs.get_binning_specs(pd.cut(self.df_raw['freq_dev'], bspecs.midi_bins16()).cat.categories)
        
        self.decoder_config['encodings']['grain_dur'] = bspecs.get_binning_specs(pd.cut(self.df_raw['grain_dur'], bspecs.midi_bins16()).cat.categories)
        self.decoder_config['encodings']['grain_dur_dev'] = bspecs.get_binning_specs(pd.cut(self.df_raw['grain_dur_dev'],bspecs.midi_bins16()).cat.categories)
        
        self.decoder_config['encodings']['grain_rate']  = bspecs.get_binning_specs(pd.cut(self.df_raw['grain_rate'],bspecs.midi_bins16()).cat.categories)
        self.decoder_config['encodings']['grain_rate_dev'] = bspecs.get_binning_specs(pd.cut(self.df_raw['grain_rate_dev'],bspecs.midi_bins16()).cat.categories)
        
        self.decoder_config['encodings']['n_voices'] = bspecs.get_binning_specs(pd.cut(self.df_raw['n_voices'],bspecs.midi_bins8()).cat.categories)
        self.decoder_config['encodings']['rel'] = bspecs.get_binning_specs(pd.cut(self.df_raw['rel'], bspecs.midi_bins4()).cat.categories)

        self.decoder_config['encodings']['duration'] = bspecs.get_binning_specs(pd.cut(self.df_raw['duration'],bspecs.dur_bins12()).cat.categories)
        self.decoder_config['encodings']['inter_event_duration'] = bspecs.get_binning_specs(pd.cut(self.df_raw['inter_event_duration'],bspecs.dur_bins12()).cat.categories)


    def _create_binned_df(self):
        ''' create the binned_df dataframe '''

        binned_df = pd.DataFrame(columns=self.df_raw.columns)

        binned_df['amp'] = pd.cut(self.df_raw['amp'], bspecs.midi_bins4(),labels=bspecs.midi_labels4())
        binned_df['freq_dev'] = pd.cut(self.df_raw['freq_dev'], bspecs.midi_bins16(),labels=bspecs.midi_labels16())
        
        binned_df['grain_dur'] = pd.cut(self.df_raw['grain_dur'], bspecs.midi_bins16(),labels=bspecs.midi_labels16())
        binned_df['grain_dur_dev'] = pd.cut(self.df_raw['grain_dur_dev'],bspecs.midi_bins16(),labels=bspecs.midi_labels16())
        
        binned_df['grain_rate']  = pd.cut(self.df_raw['grain_rate'],bspecs.midi_bins16(),labels=bspecs.midi_labels16())
        binned_df['grain_rate_dev'] = pd.cut(self.df_raw['grain_rate_dev'],bspecs.midi_bins16(),labels=bspecs.midi_labels16())
        
        binned_df['n_voices'] = pd.cut(self.df_raw['n_voices'],bspecs.midi_bins8(),labels=bspecs.midi_labels8())
        binned_df['rel'] = pd.cut(self.df_raw['rel'], bspecs.midi_bins4(),labels=bspecs.midi_labels4())

        binned_df['duration'] = pd.cut(self.df_raw['duration'],bspecs.dur_bins12(),labels=bspecs.dur_labels12())
        binned_df['inter_event_duration'] = pd.cut(self.df_raw['inter_event_duration'],bspecs.dur_bins12(),labels=bspecs.dur_labels12())

        binned_df['freq'] = self.df_raw['freq']   # does not bin the freq column
        
        # realign rows
        cols = list(binned_df)   
        cols[1], cols[0] = cols[0], cols[1]
        binned_df = binned_df.ix[:,cols]  # works for this sample, but may need to explicitly reorder if json file inputs differently
        binned_df = binned_df.dropna().reset_index(drop=True)  # need to do mean substitution here... 

        return binned_df


class EncoderServerSynth(Encoder):
    '''
    Place holder for midi_grain_server specification

    '''
    pass


