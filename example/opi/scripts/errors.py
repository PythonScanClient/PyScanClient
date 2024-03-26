# Helper for displaying exceptions

import sys
import traceback
from java.lang import Throwable
from java.util.logging import Level
from org.csstudio.display.builder.runtime.script import ScriptUtil

def showException(widget, title):
    error = sys.exc_info()[1]
    if not isinstance(error, Throwable):
        trace = str(error)
    else:
        trace = str(traceback.format_exc())

    msg = title + "\n\n" + trace
    ScriptUtil.getLogger().log(Level.WARNING, msg)
    ScriptUtil.showErrorDialog(widget, msg)
