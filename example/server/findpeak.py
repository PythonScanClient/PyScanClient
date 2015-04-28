# ScriptCommand class that fits a gaussian shape to xpos & signal,
# with optional normalization.
# Updates PVs with position, height, width of the gaussian.

from org.csstudio.scan.command import ScanScript
import sys
from gaussian import Gaussian
#print "findpeak.py path: ", sys.path

import numjy as np

class FindPeak(ScanScript):
    def __init__(self, pos_device, sig_device, norm_device, norm_value, pv_pos, pv_height, pv_width):
        print "FindPeak", pos_device, sig_device
        self.pos_device = pos_device
        self.sig_device = sig_device
        # Older scan ScriptCommand didn't allow empty arguments, so use "-"
        if norm_device == "-":
            norm_device = ""
        self.norm_device = norm_device
        self.norm_value = norm_value
        self.pv_pos = pv_pos
        self.pv_height = pv_height
        self.pv_width = pv_width
        
    def getDeviceNames(self):
        return [ self.pos_device, self.sig_device, self.pv_pos, self.pv_height, self.pv_width ]
    
    def run(self, context):
        # Turn raw python array into ndarray for easier math
        if self.norm_device:
            data = np.array(context.getData(self.pos_device, self.sig_device, self.norm_device))
            x = data[0]
            y = data[1] 
            n = data[2]
            print "x = ", x
            print "y = ", y
            print "n = ", n
            print "norm: ", self.norm_value
            y = y * float(self.norm_value) / n
            context.logData("normalized", y.nda)
        else:
            data = np.array(context.getData(self.pos_device, self.sig_device))
            x = data[0]
            y = data[1]
            print "x = ", x
            print "y = ", y
        
        # Compute fit
        g = Gaussian.fromCentroid(x, y)
        print g
        fit = g.values(x)
        
        # Log the 'fit' data for later comparison with raw data
        context.logData("fit", fit.nda)
        
        # Set PVs with result
        context.write(self.pv_pos, g.center)
        context.write(self.pv_height, g.height)
        context.write(self.pv_width, g.width)
