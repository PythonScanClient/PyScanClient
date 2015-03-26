"""
XML Helpers from http://effbot.org/zone/element-lib.html
"""

XML_HEADER = '<?xml version="1.0"?>'

def indent(elem, level=0):
    """in-place prettyprint formatter
       :param elem: xml.etree.ElementTree.Element from which to start indentation
    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i