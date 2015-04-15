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

    def test_format_exp_construction(self):
        self.assertEqual(
            nd.ContactFormat('firstname', 'lastname', 'zip').format_exp,
            '{firstname}{comma}{lastname}{comma}{zip}'
        )

    def test_regex_construction(self):
        self.assertEqual(
            nd.ContactFormat('firstname', 'lastname', 'zip').regex.pattern,
            r'^\s*[\w \.\-]+\s*,\s*[\w\-]+\s*,\s*\d{5}\s*$'
        )

    def test_format_matching_basic(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertTrue(fmt.matches('Ted Lorts, Indigo, 48098, 248 505 1216'))

    def test_format_matching_nospace(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertTrue(fmt.matches('Ted Lorts,Indigo,48098,248 505 1216'))

    def test_format_matching_extraspace(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertTrue(fmt.matches('Ted Lorts\t, \tIndigo  ,48098, \t\t248 505 1216'))

    def test_format_matching_lotsonames(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertTrue(fmt.matches('J. R. R. Tolkien, Gold, 99999, 999 999 9999'))

    def test_format_nonmatching_onename(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertFalse(fmt.matches('TedLorts, Indigo, 48098, 248 505 1216'))



if __name__ == '__main__':
    unittest.main()