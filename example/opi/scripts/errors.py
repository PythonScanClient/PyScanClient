# Helper for displaying exceptions

import sys
import traceback
from java.lang import Throwable
from java.util.logging import Logger, Level
from org.eclipse.jface.dialogs import MessageDialog
from org.csstudio.ui.util.dialogs import ExceptionDetailsErrorDialog
from wisdom import wisdom

def showException(title):
    error = sys.exc_info()[1]
    if isinstance(error, Throwable):
        Logger.getLogger("jython").log(Level.WARNING, title, error)
        ExceptionDetailsErrorDialog.openError(None, title, wisdom(), error)
    else:
        error = str(error)
        Logger.getLogger("jython").log(Level.WARNING, "%s: %s\n%s" % (title, error, traceback.format_exc()))
        MessageDialog.openWarning(None, title, "%s\n\n\n%s" % (wisdom(), error))
