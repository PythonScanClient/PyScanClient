# ScriptCommand class that writes logged data to PV

from org.csstudio.scan.command import ScanScript
from jarray import array
import numjy as np

class WriteDataToPV(ScanScript):
    def __init__(self, device, pv, norm_device=None, norm_value=1.0):
        self.device = device
        self.pv = pv
        self.norm_device = norm_device
        # Older scan ScriptCommand didn't allow empty arguments, used "-"
        if norm_device == "-":
             self.norm_device = None
        self.norm_value = norm_value
        
    def getDeviceNames(self):
        return [ self.device, self.pv ]
    
    def run(self, context):
        # print "\nWrite data for %s to %s" % (self.device, self.pv)
        if self.norm_device:
            data = np.array(context.getData(self.device, self.norm_device))
            d = data[0]
            n = data[1]
            try:
                normed = d * float(self.norm_value) / n
                # Convert np.array back into Java array for 'write'
                data = array(normed, 'd')
            except:
                # On zero division use original data
                data = context.getData(self.device)[0]
        else:
            data = context.getData(self.device)
            data = data[0]
        # print "Data: ", data.__class__.__name__
        try:
            context.write(self.pv, data, False)
        except Exception, e:
            print "WriteDataToPV(%s, %s) exception:" % (self.pv, data)
            print e
        except:
            print "WriteDataToPV(%s, %s) error with unknown exception" % (self.pv, data)
