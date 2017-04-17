'''
Custom exceptions for tensor_synth
'''

class tsBaseException(Exception): 
    """ base exception class for tensor_synth """

    def __init__(self, msg=None):
        if msg is None:                        # Set some default useful error message
            msg = "A tensor_synth error occured: {0}".format(obj)
        
        super().__init__(msg)

        #TODO add error logging here maybe
       


class tsRawInputFormattingException(tsBaseException):
    """
    thrown if there is an import problem with raw input json file
    """
    def __init__(self, filepath):
        msg = "The sc_input json file {0} is not properly formatted for synth_type={1} ".format(filepath,synth_type)
        super().__init__(msg=msg)

        self.filepath = filepath



class tsConfigFileFormatException(tsBaseException):
    """ thrown if formatting error for JSON config file in Encoder class"""

    def __init__(self, filepath):
        msg = "The decoder config json file {0} is not properly formatted for synth_type={1} ".format(filepath,synth_type)
        super().__init__(msg=msg)

        self.filepath = filepath


class tsSkipGramWordSeriesInputFormatException(tsBaseException):

    def __init__(self):
        msg = "The word series is improperly formatted: must be pd.Series or np.array of strings: <num>_<letters>"
        super(tsSkipGramWordSeriesInputFormatException, self).__init__(msg=msg)

class tsSkipGramSpanInputFormatException(tsBaseException):

    def __init__(self, value):
        msg = "{0} must either be an integer, either 2 or 4".format(value)
        super().__init__(msg=msg)


class tsSkipGramGenBatchException(tsBaseException):

    def __init__(self,df):
        msg = "The df {0} is improperly formatted".format(df)
        print(df)
        super().__init__(msg=msg)


#TODO need to fill these out...

#TODO These should be made more specific -- maybe refactor each module to have its own set of exceptions
class tsSkipGramBatchException(tsBaseException):

    pass


class tsSkipGramLabelsException(tsBaseException):

    pass


class tsModelNotTrainedException(tsBaseException)

    pass


class tsGeneratorException(tsBaseException):
    pass


class tsDecoderException(tsBaseException):
    pass


class tsDecoderProxyException(tsBaseException):
    pass

