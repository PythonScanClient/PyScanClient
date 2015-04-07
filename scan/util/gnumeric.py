"""Gnumeric table reader

@author: Kay Kasemir
"""

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
    f = gzip.open(filename)
    gnumeric = f.read()
    f.close()
    
    root = ET.fromstring(gnumeric)
    
    # ET.dump(root)
    
    if not "gnumeric" in root.tag:
        raise Exception("Expected GNUMERIC document, got %s" % root.tag)
    
    sheets = __findWithoutNamespace(root, "Sheets")
    if sheets is None:
        raise Exception("Cannot locate Sheets")
    sheet = __findWithoutNamespace(sheets, "Sheet")
    if sheet is None:
        raise Exception("Cannot locate Sheets/Sheet")
    
    # Locate table size        
    size = __findWithoutNamespace(sheet, "MaxRow")
    if size is None:
        raise Exception("Cannot locate Sheets/Sheet/MaxRow")
    rows = int(size.text) + 1
    
    size = __findWithoutNamespace(sheet, "MaxCol")
    if size is None:
        raise Exception("Cannot locate Sheets/Sheet/MaxCol")
    cols = int(size.text) + 1
    
    logger.debug("Size: %d rows, %d cols" % (rows, cols))
    
    # Create empty table, because cells will only provide
    # data for non-empty cells, and maybe in random order
    table = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append("")
        table.append(row)
    
    cells = __findWithoutNamespace(sheet, "Cells")
    if cells is None:
        raise Exception("Cannot locate Sheets/Sheet/Cells")
    
    for cell in cells:
        row = int(cell.attrib['Row'])
        col = int(cell.attrib['Col'])
        val = cell.text
        logger.debug("Cell (%d, %d): %s" % (row, col, val))
        table[row][col] = val
    
    # Trim empty trailing columns
    while cols > 0:
        for col in range(cols-1, 0, -1):
            for row in range(rows):
                if len(table[row][col].strip()) > 0:
                    return table
            # Remove rightmost table column
            cols -= 1
            for row in table:
                del row[cols]
    
    return table
