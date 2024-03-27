# Used by plot in alignment scan to update local waveform PVs
# that are used to display markers
#
# pvs[0]: Location of fit
# pvs[1]: Height of fit
# pvs[2]: Width of fit
# pvs[3]: 'x' waveform for center marker
# pvs[4]: 'y' waveform for center markers
# pvs[5]: 'x' waveform for left marker
# pvs[6]: 'x' waveform for right marker
from org.csstudio.display.builder.runtime.script import PVUtil
from jarray import array

x = PVUtil.getDouble(pvs[0])
h = PVUtil.getDouble(pvs[1])
# Show half of full-widths-half-height on each side of center
hw = PVUtil.getDouble(pvs[2]) / 2

pvs[3].write(array([ x, x ], 'd'))
pvs[4].write(array([ 0, h ], 'd'))
pvs[5].write(array([ x-hw, x-hw ], 'd'))
pvs[6].write(array([ x+hw, x+hw ], 'd'))
