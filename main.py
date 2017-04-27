
#import tensor_synth as ts

from tensor_synth.translate.encoder import EncoderProxySynth
from tensor_synth.learn.tf_models import SkipGramTF
from tensor_synth.learn.tf_generators import generate_word_sequence

from tensor_synth.translate.decoder import DecoderProxySynth

import tests

import os


def main():

    '''
    This is the main test drive for the tensor_synth API
    when main is run a data should be encoded, trained and decoded to the specified data path
    this output can be played back by the supercollider midi api

    '''


    testpath = os.path.abspath(os.path.join('.','data','grain_improv2.json'))

    x = EncoderProxySynth(testpath)
    
    config_path = os.path.abspath(os.path.join('.','data','test_config_output.json'))
    x.make_config_json(config_path) # generates a test config file for dev purposes

    y = SkipGramTF(x.output_seq)
    y.make_graph()
    y.run_model(100)

    new_seq = generate_word_sequence(y,25,8)
    print(new_seq)

    json_output_path = os.path.abspath(os.path.join('.','data','api_test_output.json'))
    z = DecoderProxySynth(new_seq, config_path)
    
    print(z.word_series)
    print(z.output_df)
    z.export_output_to_json(json_output_path)

if __name__ == '__main__':
    main()
