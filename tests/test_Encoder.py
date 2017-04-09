
import unittest
import os


# these unittests are mainly to check whether improper input/output file raise errors and/or are properly formatted


class EncoderTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_raw_df_bad_format_throws_RawInputFormatException(self):
        """ test that error gets thrown on bad raw sc_json input"""
        pass

    def test_config_file_bad_format_throws_ConfigFileFormatException(self):
        pass


class DecoderTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
