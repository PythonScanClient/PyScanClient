"""Spreadsheet reader and writer

@author: Kay Kasemir
"""
from scan.util.csvtable import readCsv, writeCsv
from scan.util.gnumeric import readGnumeric
from scan.util.excel import readExcel

def readSpreadsheet(filename):
    """Read a spreadsheet file.
    
    Reads the basic table of strings and numbers
    from a gnumeric file.
    
    :param filename: Name of file to read, either '*.cvs', '*.tab', '*.xls' or '*.gnumeric'
    :return: `[ [ row0cell0, row0cell1 ], [ row1cell0, row1cell1 ], ... ]`
    
    Example::
    
    >>> table = readSpreadsheet('/path/to/file.csv')
    >>> print table
    """
    if filename.endswith('.gnumeric'):
        return readGnumeric(filename)
    elif filename.endswith('.xls'):
        return readExcel(filename)
    else:
        return readCsv(filename)


def writeSpreadsheet(filename, table):
    """Save table to file

    Writes table as spreadsheet file.

    :param filename: File path, must end in ".csv" or ".tab"
    :param table: Table `[ [ row0cell0, row0cell1 ], [ row1cell0, row1cell1 ], ... ]`

    Example::
    
    >>> writeSpreadsheet('/path/to/file.csv', [ [ 'X', 'Y' ], [ 1, 2 ], [ 3, 4 ] ])
    """
    # At this time only supports Csv
    writeCsv(filename, table)


if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 1:
        print("Usage: spreadsheet file.csv other.xls finally.gnumeric")
    else:
        for filename in sys.argv[1:]:
            print(("========= %s ===========" % file))
            # logging.basicConfig(level=logging.NOTSET)
            table = readSpreadsheet(filename)
            header = table[0]
            rows = table[1:]
            print("Header: ", header)
            print("Rows: ", rows)
