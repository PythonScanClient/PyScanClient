"""
Unit test for RangeHelper

@author: Kay Kasemir
"""
from scan.table.range_helper import expandRanges
import unittest

class TestRangeExpansion(unittest.TestCase):
    def test_expand(self):
        rows = [
           # Full range(start, end, step)
           [ "Line 1",  "range(1, 12, 5)",  "  Neutrons",   "10" ],
           # Plain row still works
           [ "Line 2",  "47",  "Seconds",   "2" ],
           # Simple range(count), but two of them
           [ "Line 3",  "range(3)",  "Seconds",  "range(2)" ],
           # One range stepping down
           [ "Line 4",  "range(2)",  "Seconds",  "range(2,0,-1)" ],
           ]
        print "Original:"
        for row in rows:
            print row
        print "Expanded:"
        result = expandRanges(rows)
        for row in result:
            print row
        self.assertEqual(len(result), 14)

        # List, tuple        
        rows = [
           [ "( 2, 4)",  "[ 0, 90, 180]",  "Seconds" ],
           ]
        print "Original:"
        for row in rows:
            print row
        print "Expanded:"
        result = expandRanges(rows)
        for row in result:
            print row
        self.assertEqual(len(result), 6)



if __name__ == '__main__':
    unittest.main()
    