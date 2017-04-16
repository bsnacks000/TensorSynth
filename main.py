
#import tensor_synth as ts

from tensor_synth.translate.encoder import EncoderProxySynth
import tests

import os


def main():

    # development test code here... 
    testpath = os.path.abspath(os.path.join('.','data','grain_improv2.json'))

    x = EncoderProxySynth(testpath)
    #print(x.binned_df)
    #print(x.output_seq)
    #print(x.decoder_config)
    x.make_config_json(os.path.join('.','data','test_config_output.json')) # generates a test config file for dev purposes


if __name__ == '__main__':
    main()
