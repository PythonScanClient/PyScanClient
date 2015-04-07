"""Excel table reader

Requires the xlrd package.
For xlrd 0.7.4, the timemachine.py
can be used with both Python and Jython
based on a small patch.

@author: Kay Kasemir
"""

try:
    from xlrd import open_workbook
except:
    def open_workbook(dummy):
        raise Exception("Excel not supported, missing `xlrd`")

import logging

logger = logging.getLogger("Excel2ScanTable")

def readExcel(filename):
    """Read an excel file.
    
    Reads the basic table of strings and numbers
    from an Excel file.
    
    :param filename: Name of file to read
    :return: `[ [ row0cell0, row0cell1 ], [ row1cell0, row1cell1 ], ... ]`

    Example::
    
    >>> table = readExcel('/path/to/file.xls')
    >>> print table
    """
    wb = open_workbook(filename)
    if wb.nsheets < 1:
        raise Exception("No sheets found")
    sheet = wb.sheets()[0]
    logger.debug("File '%s', sheet '%s', %d x %d rows x cols"
                 % (filename, sheet.name, sheet.nrows, sheet.ncols))
    table = []
    for row in range(sheet.nrows):
        vals = [ str(sheet.cell(row, col).value) for col in range(sheet.ncols) ]
        # Skip comments, empty lines
        valstr = " ".join(vals)
        valstr = valstr.strip()
        if len(valstr) <= 0  or  valstr.startswith("#"):
            continue
        table.append(vals)
    return table
