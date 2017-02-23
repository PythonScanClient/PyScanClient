"""
Helper for expanding "range(start, end, step)"
or list "[ 1, 2 ]" or tuple "( 2, 4 )"

@author: Kay Kasemir
"""
import re

# Regular expression for a number,
# captured as one group,
# padded by space
__re_dbl = " *([-+]?[0-9]+\.?[0-9]*(?:[eE][-+]?[0-9]+)?) *"

# Regular expression for the range([start,] stop[, step]) command,
# capturing the start, end and step arguments
__re_range = "range\((?:" + __re_dbl + ",)?" + __re_dbl + "(?:," + __re_dbl +")?\)"

# Similar for loop([start,] stop[, step])
__re_loop = "[Ll]oop\((?:" + __re_dbl + ",)?" + __re_dbl + "(?:," + __re_dbl +")?\)"

range_matcher = re.compile(__re_range)
loop_matcher = re.compile(__re_loop)

def getRangeOrLoop(cell, matcher):
    """Using either the range_matcher or loop_matcher,
       get the (start, end, step) or None
    """
    # Check for "range(...)" or "loop(...)"
    m = matcher.match(cell)
    if m:
        # Evaluate yourself to support fractional steps
        # (like numpy.arange, but without requiring numpy)
        (start, end, step) = m.groups()
        start = float(start) if start else 0
        end = float(end)
        step = float(step) if step else 1
        if step == 0:
            raise Exception("Illegal step=0 in " + cell)
        return (start, end, step)
    else:
        return None
    
def getIterable(cell):
    """If cell contains a range, list or tuple, return that iterable.
       Otherwise returns None
    """
    cell = str(cell).strip()

    # Check for "range(...)"
    rng = getRangeOrLoop(cell, range_matcher)
    if rng is not None:
        # Evaluate yourself to support fractional steps
        # (like numpy.arange, but without requiring numpy)
        (start, end, step) = rng
        value = start
        result = []
        while value < end if step > 0 else value > end:
            result.append(value)
            value += step
        return result
    else:
        # Eval a list or tuple
        if (cell.startswith("(") or
            cell.startswith("[")):
            cell_range = eval(cell)
            if isinstance(cell_range, (list, tuple)):
                return cell_range
    return None

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
        cell_range = getIterable(cell)
        if cell_range is not None:
            result = []
            for value in cell_range:
                copy = list(row)
                copy[i] = str(value)
                result.append(copy)
            # If cell expanded to nothing, return row with that cell cleared
            # (not original 'range(2, 0, 1)', nor empty row)
            if len(result) == 0:
                copy = list(row)
                copy[i] = ''
                result.append(copy)
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
    nothing = True
    for row in rows:
        expanded = expandRangeInRow(row)
        if expanded is not None:
            nothing = False
            result.extend(expanded)
        else:
            result.append(row)
    # If nothing was expanded, return as is
    if nothing:
        return result
    # Expanded at least one cell on one row
    # check if there are more cells 
    return expandRanges(result)
