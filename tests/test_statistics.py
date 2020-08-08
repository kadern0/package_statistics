#!/usr/bin/env python3
"""Testing docstring"""

import unittest
from unittest.mock import patch
from package_statistics import *

class BasicTests(unittest.TestCase):
    """Project's tests"""
    package_stats_value = [(b'ten', 10), (b'nine', 9), (b'eight', 8),
                           (b'seven', 7), (b'six', 6), (b'five', 5),
                           (b'four', 4), (b'three', 3), (b'two', 2),
                           (b'one', 1)]

    def create_sample_file(arch, fname):
        response_content = b'etc/asdf ten\netc/asdf nine,ten\netc/asdf eight,nine,ten\netc/asdf seven,eight,nine,ten\netc/asdf six,seven,eight,nine,ten\netc/asdf five,six,seven,eight,nine,ten\netc/asdf four,five,six,seven,eight,nine,ten\netc/asdf three,four,five,six,seven,eight,nine,ten\netc/asdf two,three,four,five,six,seven,eight,nine,ten\netc/asdf one,two,three,four,five,six,seven,eight,nine,ten\n'
        fname.write(response_content)
    def test_is_arch_valid_true(self):
        """Test if the architecture is valid"""
        self.assertTrue(is_arch_valid("i386"))
    def test_is_arch_valid_false(self):
        """Test if the architecture is not valid"""
        self.assertFalse(is_arch_valid("i387"))

    @patch('package_statistics.download_file', side_effect=create_sample_file)
    def test_get_stats(self, mock_get_file):
        """Test the package stats"""
        self.assertEqual(get_stats('test'), self.package_stats_value)

if __name__ == "__main__":
    unittest.main()

