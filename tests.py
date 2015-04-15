"""
Unit tests for normalize_data
Ted Lorts
2015 April 14
"""

from __future__ import unicode_literals
import unittest
import normalize_data as nd


class TestNormalizeData(unittest.TestCase):

    def test_extract_fullname(self):
        self.assertEqual(
            nd.extract_fullname('M. Paul Weeks'),
            {'firstname': 'M. Paul', 'lastname': 'Weeks'}
        )

    def test_extract_phone_space(self):
        self.assertEqual(
            nd.extract_phone_space('248 505 1216'), 
            {'phonenumber': '248-505-1216'}
        )

if __name__ == '__main__':
    unittest.main()