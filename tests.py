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



class TestContactFormatBasics(unittest.TestCase):

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

    def test_format_nonmatching_colorpunct(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertFalse(fmt.matches('Ted Lorts, Ind-igo, 48098, 248 505 1216'))

    def test_format_nonmatching_bigzip(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertFalse(fmt.matches('Ted Lorts, Indigo, 4809800, 248 505 1216'))

    def test_format_nonmatching_smallzip(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertFalse(fmt.matches('Ted Lorts, Indigo, 4809, 248 505 1216'))

    def test_format_nonmatching_bigphone(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertFalse(fmt.matches('Ted Lorts, Indigo, 48098, 248 505 12161'))

    def test_format_nonmatching_smallphone(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertFalse(fmt.matches('Ted Lorts, Indigo, 48098, 248 505 121'))



class TestContactNormalization(unittest.TestCase):

    def test_object_format_basic_format0(self):
        fmt = nd.ContactFormat('lastname', 'firstname', 'phone_dash', 'color', 'zip')
        self.assertEqual(
            fmt.objectify('Lorts, Ted, (248)-505-1216, Indigo, 48098'),
            {'firstname': 'Ted', 
             'lastname': 'Lorts', 
             'color': 'Indigo', 
             'zipcode': '48098', 
             'phonenumber': '248-505-1216'}
        )

    def test_object_format_basic_format1(self):
        fmt = nd.ContactFormat('fullname', 'color', 'zip', 'phone_space')
        self.assertEqual(
            fmt.objectify('Ted Lorts, Indigo, 48098, 248 505 1216'),
            {'firstname': 'Ted', 
             'lastname': 'Lorts', 
             'color': 'Indigo', 
             'zipcode': '48098', 
             'phonenumber': '248-505-1216'}
        )

    def test_object_format_basic_format2(self):
        fmt = nd.ContactFormat('firstname', 'lastname', 'zip', 'phone_space', 'color')
        self.assertEqual(
            fmt.objectify('Ted, Lorts, 48098, 248 505 1216, Indigo'),
            {'firstname': 'Ted', 
             'lastname': 'Lorts', 
             'color': 'Indigo', 
             'zipcode': '48098', 
             'phonenumber': '248-505-1216'}
        )




if __name__ == '__main__':
    unittest.main()