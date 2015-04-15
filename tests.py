"""
Unit tests for normalize_data
Ted Lorts
2015 April 14
"""

from __future__ import unicode_literals
import unittest
import normalize_data as nd


class TestExtractionFunctions(unittest.TestCase):

    def test_extract_fullname(self):
        self.assertEqual(
            nd.extract_fullname('M. Paul Weeks'),
            {'firstname': 'M. Paul', 'lastname': 'Weeks'}
        )
    def test_extract_fullname_extraspaces_between(self):
        self.assertEqual(
            nd.extract_fullname('M. Paul \t  Weeks'),
            {'firstname': 'M. Paul', 'lastname': 'Weeks'}
        )
    def test_extract_fullname_extraspaces_within(self):
        self.assertEqual(
            nd.extract_fullname('M. \t   Paul Weeks'),
            {'firstname': 'M. Paul', 'lastname': 'Weeks'}
        )
    def test_extract_fullname_hyphenated(self):
        self.assertEqual(
            nd.extract_fullname('M. Paul Smith-Weeks'),
            {'firstname': 'M. Paul', 'lastname': 'Smith-Weeks'}
        )

    def test_extract_phone_space(self):
        self.assertEqual(
            nd.extract_phone_space('248 505 1216'),
            {'phonenumber': '248-505-1216'}
        )
    def test_extract_phone_space_extraspaces(self):
        self.assertEqual(
            nd.extract_phone_space('248\t  505 \t 1216'),
            {'phonenumber': '248-505-1216'}
        )

    def test_extract_phone_dash(self):
        self.assertEqual(
            nd.EXTRACTION_FUNCTIONS['phone_dash']('(248)-505-1216'),
            {'phonenumber': '248-505-1216'}
        )

    # Skipping the rest of the extraction functions, as they perform
    # no transformation on the data



class TestContactFormat(unittest.TestCase):
    pass
    # def test_



if __name__ == '__main__':
    unittest.main()