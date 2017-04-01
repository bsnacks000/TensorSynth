'''
Custom exceptions for tensor_synth
'''

class tsBaseException(Exception):
    """
    Base Exception class for tensor_synth
    """

    def __init__(self, obj, msg=None):
        if msg is None:                        # Set some default useful error message
            msg = "A tensor_synth error occured: {}".format(obj)
        
        super(tsBaseException, self).__init__(msg)
       
        self.obj = obj  # the object that caused the error
        


class tsRawDFInputException(tsBaseException, IOError):
    """
    Thrown if there is an import problem with json file
    """
    def __init__(self, filepath):
        msg = "The sc_input json file is not correctly formatted: {}".format(filepath)
        super(tsRawDFInputException, self).__init__(msg)

        self.filepath = filepath


