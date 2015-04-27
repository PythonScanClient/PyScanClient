# Used by plot in EdgeScan.opi to update local waveform PVs
# that are used to display edge markers
#
# pvs[0]: Location of edge
# pvs[1]: Height of edge
# pvs[2]: Width of edge
# pvs[3]: 'x' waveform for edge marker
# pvs[4]: 'y' waveform for edge markers
# pvs[5]: 'x' waveform for left edge marker
# pvs[6]: 'x' waveform for right edge marker
from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.eclipse.jface.dialogs import MessageDialog
from jarray import array

x = PVUtil.getDouble(pvs[0])
h = PVUtil.getDouble(pvs[1])
# Show half of full-widths-half-height on each side of center
hw = PVUtil.getDouble(pvs[2]) / 2

# MessageDialog.openWarning(None, "Debug",  "Set %s = %s" % (pvs[2].getName(), str(x)) )

pvs[3].setValue(array([ x, x ], 'd'))
pvs[4].setValue(array([ 0, h ], 'd'))
pvs[5].setValue(array([ x-hw, x-hw ], 'd'))
pvs[6].setValue(array([ x+hw, x+hw ], 'd'))
