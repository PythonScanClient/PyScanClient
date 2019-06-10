"""Gnumeric table reader

@author: Kay Kasemir
"""

try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
import logging
import gzip


logger = logging.getLogger("GnumericSupport")

def __findWithoutNamespace(element, desired_tag):
    """Dumb search for child by tag, ignoring potential namespace prefix"""
    for child in element:
        tag = child.tag
        pos = tag.rfind('}')
        if pos > 0:
            tag = tag[pos+1:]
        if tag == desired_tag:
            return child
    return None

def readGnumeric(filename):
    """Read a gnumeric file.
    
    Reads the basic table of strings and numbers
    from a gnumeric file.
    
    :param filename: Name of file to read
    :return: `[ [ row0cell0, row0cell1 ], [ row1cell0, row1cell1 ], ... ]`
    
    Example::
    
    >>> table = readGnumeric('/path/to/file.gnumeric')
    >>> print table
    """
    logger.debug("UnZIP %s", filename)
    f = gzip.open(filename)
    gnumeric = f.read()
    f.close()
    
    logger.debug("Parse XML")
    root = ET.fromstring(gnumeric)
    del gnumeric
    
    # ET.dump(root)
    
    if not "gnumeric" in root.tag:
        raise Exception("Expected GNUMERIC document, got %s" % root.tag)
    
    sheets = __findWithoutNamespace(root, "Sheets")
    if sheets is None:
        raise Exception("Cannot locate Sheets")
    sheet = __findWithoutNamespace(sheets, "Sheet")
    if sheet is None:
        raise Exception("Cannot locate Sheets/Sheet")
    # Sheets/Sheet/MaxRow and Sheets/Sheet/MaxCol
    # have size, but that can include many empty cells
    # when for example setting the format for a 'column',
    # so ignore
    cells = __findWithoutNamespace(sheet, "Cells")
    if cells is None:
        raise Exception("Cannot locate Sheets/Sheet/Cells")
    
    # Locate all cells with valid content
    max_row = 0
    max_col = 0
    valid = []
    for cell in cells:
        row = int(cell.attrib['Row'])
        col = int(cell.attrib['Col'])
        val = cell.text
        if val is None:
            continue
        val = val.strip()
        if len(val) <= 0:
            continue
        logger.debug("Cell (%d, %d): %s" % (row, col, val))
        valid.append((row, col, val))
        if row > max_row:
            max_row = row
        if col > max_col:
            max_col = col
    del cells
    del sheet
    del root

    logger.debug("Size: %d rows, %d cols", max_row, max_col)
    # Create table, then populate cells
    table = []
    for r in range(max_row+1):
        row = [ "" for c in range(max_col+1) ]
        table.append(row)
    for info in valid:
        (row, col, val) = info
        table[row][col] = val

    return table
