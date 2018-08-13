"""Scan Info

Copyright (c) 2015
All rights reserved. Use is subject to license terms and conditions

@author: Kay Kasemir
"""
from datetime import datetime

class ScanInfo(object):
    """Information about a scan
    
    :param xml: XML element for a scan info
    """
    def __init__(self, xml):
        self.id = int(xml.find('id').text)
        self.name = xml.find('name').text
        self.created = int(xml.find('created').text)
        self.state = xml.find('state').text
        self.runtime = int(xml.find('runtime').text)
        
        node = xml.find('total_work_units')
        self.total_work_units = 0 if node is None else int(node.text)
        
        node = xml.find('performed_work_units')
        self.performed_work_units = 0 if node is None else int(node.text)
        
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
    
    def createdDatetime(self):
        """:return: datetime when scan was created"""
        return datetime.fromtimestamp(self.created / 1000)
    
    # TODO Turn id, name, ... into @property?
    
    def __str__(self):
        if self.state == 'Running':
            return "'%s' [%d]: %s, %d %%" % (self.name, self.id, self.state, self.percentage())
        return "'%s' [%d]: %s" % (self.name, self.id, self.state)
