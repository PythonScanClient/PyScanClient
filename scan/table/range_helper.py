"""
Helper for expanding range(start, end, step)

@author: Kay Kasemir
"""
import re

# Regular expression for a number,
# captured as one group,
# padded by space
re_dbl = " *([-+]?[0-9]+\.?[0-9]*(?:[eE][-+]?[0-9]+)?) *"

# Regular expression for the range([start,] stop[, step]) command,
# capturing the start, end and step arguments
re_range = "range\((?:" + re_dbl + ",)?" + re_dbl + "(?:," + re_dbl +")?\)"
range_matcher = re.compile(re_range)

def expandRangeInRow(row):
    """Given a row, look for cells that contain
          range(start, end, step)
       and expand those into multiple rows
       
       Input:
       [ "Line 1",  "range(1, 12, 5)",  "  Neutrons",   "10" ]
        
       Returns:
       [
         [ "Line 1",  "1",  "  Neutrons",   "10" ],
         [ "Line 1",  "6",  "  Neutrons",   "10" ],
         [ "Line 1",  "11",  "  Neutrons",   "10" ]
       ]
       
       Returns None if there is nothing to expand
    """
    for i in range(len(row)):
        cell = row[i]
        m = range_matcher.match(cell)
        if m:
            result = []
            (start, end, step) = m.groups()
            start = float(start) if start else 0
            end = float(end)
            step = float(step) if step else 1
            if step == 0:
                raise Exception("Illegal range(start, stop, step=0)")
            value = start
            if (step > 0 and end < start) or (step < 0 and end > start):
                raise Exception("Ill-defined range(%f, %f, %f)" % (start, end, step))
            while value < end if step > 0 else value > end:
                copy = list(row)
                copy[i] = str(value)
                result.append(copy)
                value += step
            # Performed one expansion, return for another pass
            return result
    # Nothing to expand
    return None


def expandRanges(rows):
    """Given a table of rows, expand rows that contain
          range(start, end, step)
       into multiple rows.
       
       Iterates until there is nothing to expand.
    """
    result = []
    for row in rows:
        expanded = expandRangeInRow(row)
        if expanded:
            result.extend(expanded)
        else:
            result.append(row)
    # If there was nothing expanded, return as is
    if len(rows) == len(result):
        return rows
    # Expanded at least one cell on one row
    # check if there are more cells 
    return expandRanges(result)


# --------------------------------------------------------------------------------------------

import unittest

class TestMatching(unittest.TestCase):
    def test_number(self):
        matcher = re.compile(re_dbl)
        for number in [ "3.14", "3", "1e-19", "-0.123e47" ]:
            m = matcher.match(number)
            print number + " -> " + m.group(0)
            self.assertEqual(m.group(0), number)

    def test_range(self):
        for r in [ "range(5)", "range( 5 )", "range(1, 5 )",
                   "range(1, 5 ,2e-1)", "range(1, 8, 2)", "range(8, 1, -3)"
                   ]:
            m = range_matcher.match(r)
            print r + " -> " + str(m.groups())
            self.assertEqual(m.group(0), r)
        
        m = range_matcher.match("range( 5 )")
        self.assertEquals(m.group(2), "5")
        
        m = range_matcher.match("range(1, 5 ,2e-1)")
        self.assertEquals(m.group(1), "1")
        self.assertEquals(m.group(2), "5")
        self.assertEquals(m.group(3), "2e-1")
            
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
        for row in expandRanges(rows):
            print row

    def test_bad_ranges(self):
        try:
            expandRanges( [ [ "Line 1",  "range(1, 12, 0)",  "  Neutrons",   "10" ] ])
            self.fail("Did not catch zero step size")
        except Exception, e:
            self.assertTrue("step=0" in str(e))

        try:
            expandRanges( [ [ "Line 1",  "range(1, 12, -2)",  "  Neutrons",   "10" ] ])
            self.fail("Did not catch wrong step direction")
        except Exception, e:
            self.assertTrue("Ill-defined" in str(e))



if __name__ == '__main__':
    unittest.main()
    
