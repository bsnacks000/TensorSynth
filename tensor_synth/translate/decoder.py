


class Decoder(object):

    """
    Decoder converts tensor_synth word format back to midi output for supercollider
    It reads in a unique json file with the correct binnings in order to unbin the corpus
    Midi values are chosen by generating a random number based on these bin widths
    
    :param: config_filepath - the json formatted config filepath
    """

    def __init__(self, config_filepath):
        pass