"""CSV table reader and writer

@author: Kay Kasemir
"""

import csv

# Supported file endings for writing
WRITE_TYPES = ( ".csv", ".tab" )

def readCsv(filename):
    """Read a CSV file.
    
    Reads the basic table of strings and numbers
    from a gnumeric file.
    
    :param filename: Name of file to read
    :return: `[ [ row0cell0, row0cell1 ], [ row1cell0, row1cell1 ], ... ]`
    
    Example::
    
    >>> table = readCsv('/path/to/file.csv')
    >>> print table
    """
    f = open(filename, 'rU')
    reader = csv.reader(f)
    table = []
    for row in reader:
        table.append(row)
    f.close()
    return table


def writeCsv(filename, table):
    """Save table to file

    Writes table as CSV file.

    :param filename: File path, must end in ".csv" or ".tab"
    :param table: Table `[ [ row0cell0, row0cell1 ], [ row1cell0, row1cell1 ], ... ]`

    Example::
    
    >>> writeCsv('/path/to/file.csv', [ [ 'X', 'Y' ], [ 1, 2 ], [ 3, 4 ] ])
    """
    sep = filename.rfind('.')
    if sep < 0:
        raise Exception("Missing file type suffix in '%s'" % filename)
    ending = filename[sep:]
    if not ending in WRITE_TYPES:
        raise Exception("Cannot save '%s', must use one of these file type: %s" % (filename, str(WRITE_TYPES)))
    f = open(filename, 'w')
    writer = csv.writer(f)
    for row in table:
        writer.writerow(row)
    f.close()
