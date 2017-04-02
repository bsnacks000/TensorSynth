
#import tensor_synth as ts

from tensor_synth.translate.encoder import EncoderProxySynth
import tests

import os


def main():

    # development test code here... 
    testpath = os.path.abspath(os.path.join('.','data','test.json'))

    x = EncoderProxySynth(testpath)
    print(x.binned_df)
    print(x.output_seq)
    print(x.decoder_config)


if __name__ == '__main__':
    main()
