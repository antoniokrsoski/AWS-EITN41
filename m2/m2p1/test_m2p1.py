import unittest
from m2p1 import *

class TestParsePoly(unittest.TestCase):

    def test_parse_poly(self):
        m = {
            "" : [],
            "x" : [1], # this case is very funny, how do we know if we have a 1 at x^0 or at x^1
            "1+x" : [1,1], 
            "5+x-x^2" : [5,1,-1],
            "13+8x+11x^2+x^3+5x^4" : [13,8,11,1,5],
        }

        for key, expected in m.items(): 
            self.assertEqual(parse_poly(key), expected, "Not matching input with expected output")


if __name__ == '__main__':
    unittest.main()