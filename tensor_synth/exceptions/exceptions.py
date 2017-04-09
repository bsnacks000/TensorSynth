'''
Custom exceptions for tensor_synth
'''

class tsBaseException(Exception): 
    """ base exception class for tensor_synth """

    def __init__(self, msg=None):
        if msg is None:                        # Set some default useful error message
            msg = "A tensor_synth error occured: {0}".format(obj)
        
        super(tsBaseException, self).__init__(msg)
       


class tsRawInputFormattingException(tsBaseException, IOError):
    """
    thrown if there is an import problem with raw input json file
    """
    def __init__(self, filepath):
        msg = "The sc_input json file {0} is not properly formatted for synth_type={1} ".format(filepath,synth_type)
        super(tsInputFormatException, self).__init__(msg=msg)

        self.filepath = filepath



class tsConfigFileFormatException(tsBaseException, ValueError):
    """ thrown if formatting error for JSON config file in Encoder class"""

    def __init__(self, filepath):
        msg = "The decoder config json file {0} is not properly formatted for synth_type={1} ".format(filepath,synth_type)
        super(tsConfigFileFormatException, self).__init__(msg=msg)

        self.filepath = filepath


