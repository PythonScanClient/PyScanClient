"""
Unit test for RangeHelper

@author: Kay Kasemir
"""
from scan.table.range_helper import getIterable, expandRanges
import unittest

class TestRangeExpansion(unittest.TestCase):
    def test_iterable(self):
        points = getIterable("[ 2, 4 ]")
        self.assertEqual(str(points), "[2, 4]")

        points = getIterable("range(5)")
        self.assertEqual(str(points), "[0, 1, 2, 3, 4]")
        
        points = getIterable("range(2, 5, 2)")
        self.assertEqual(str(points), "[2.0, 4.0]")
        
        points = getIterable("range(0.5, 4, 0.5)")
        self.assertEqual(str(points), "[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]")

        points = getIterable("range(175,245,70)")
        self.assertEqual(str(points), "[175.0]")

        points = getIterable("range(175,0,70)")
        self.assertEqual(str(points), "[]")

        text = getIterable("'Fred'")
        self.assertTrue(text is None)

        points = getIterable("[ 'a', 'b' ]")
        self.assertEqual(str(points), "['a', 'b']")

    
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


        # Mix
        rows = [
           [ "'Fred'",  "range(2, 4, 2)",  "Seconds" ],
           [ "Nop1",    "[]",  "Seconds" ],
           [ "Jane",    "[2]",  "Seconds" ],
           [ "Nop2",    "range(2, 0, 2)",  "Seconds" ],
           ]
        print "Original:"
        for row in rows:
            print row
        print "Expanded:"
        result = expandRanges(rows)
        for row in result:
            print row
        self.assertEqual(len(result), 4)


if __name__ == '__main__':
    unittest.main()
    