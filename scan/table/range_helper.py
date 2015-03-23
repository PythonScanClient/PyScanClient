"""
Helper for expanding "range(start, end, step)"
or list "[ 1, 2 ]" or tuple "( 2, 4 )"

@author: Kay Kasemir
"""
import re

def getIterable(cell):
    """If cell contains a range, list or tuple, return that iterable.
       Otherwise returns None
    """
    cell = str(cell).strip()
    if (cell.startswith("range") or
        cell.startswith("(") or
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
        if cell_range:
            result = []
            for value in cell_range:
                copy = list(row)
                copy[i] = str(value)
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
