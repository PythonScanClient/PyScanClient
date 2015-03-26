"""Scan Info

Copyright (c) 2015
All rights reserved. Use is subject to license terms and conditions

@author: Kay Kasemir
"""
import xml.etree.ElementTree as ET

class ScanInfo(object):
    """Information about a scan
    
    :param scan_info_xml: XML for scan info as returned by server 
    """
    def __init__(self, scan_info_xml):
        xml = ET.fromstring(scan_info_xml)
        
        self.id = int(xml.find('id').text)
        self.name = xml.find('name').text
        self.created = int(xml.find('created').text)
        self.state = xml.find('state').text
        self.runtime = int(xml.find('runtime').text)
        self.total_work_units = int(xml.find('total_work_units').text)
        self.performed_work_units = int(xml.find('performed_work_units').text)
        self.address = int(xml.find('address').text)
        self.command = xml.find('command').text
    
    def isDone(self):
        """:return: `True` if scan has completed, successful or not"""
        return not (self.state in ( 'Idle', 'Running', 'Paused' )) 
    
    def percentage(self):
        """:return: Percent of work done, 0...100"""
        if self.total_work_units <= 0:
            return 0;
        return int(self.performed_work_units * 100 / self.total_work_units);
    
    # TODO Methods to convert raw seconds into time stamps
    
    def __str__(self):
        if self.state == 'Running':
            return "'%s' [%d]: %s, %d %%" % (self.name, self.id, self.state, self.percentage())
        return "'%s' [%d]: %s" % (self.name, self.id, self.state)
