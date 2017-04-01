import pandas as pd

from tensor_synth.exceptions import *



class Encoder(object):
    """
    Encodes tensor_synth json file
    :param: scjson_filepath: path to the sc input raw data file in json format
    """

    def __init__(self, scjson_filepath):
        
        # --> some check here for improper json file format
        self.df_raw = _import_json(scjson_filepath)
        
        self.decoder_config = {}
        self.binned_df = None

    def _import_json(self):

        try:
                        
            out = pd.read_json(scjson_filepath,orient='index') \    
                .sort_values('noteOn_timestamp')\
                .drop('id',axis=1)\
                .reset_index(drop=True)

            # check formatting here and raise tsRawDFInputException if not to spec:


        except tsRawDFInputException as e:
            print('handle exception here')

        return out


    def _clean_raw_df(self):
        pass

    def _create_binned_df(self):
        pass

    def make_config_json(self, filepath):
        pass



