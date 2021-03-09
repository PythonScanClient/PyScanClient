from __future__ import print_function

__version__ = '1.9.0'

version_history = """
1.9.0 - Support submit(.., timeline, deadline) parameters
1.8.1 - Fix error in requests.HTTPError handling
1.8.0 - Set command with 'readback_value'
1.7.0 - CommandSequence class inherits from list
1.6.0 - Add support for Python3, CPython uses requests library
1.5.6 - wait..() fix
1.5.5 - scanInfo() time out
1.5.4 - Add '!=' to If() and Wait()
1.5.3 - Fix 'id' vs. 'scanID' in patch()
1.5.2 - Try to use cElementTree
1.5.1 - ScanInfo.finish
1.5.0 - If(..) command
1.4.1 - Better Set(..) representation
1.4.0 - Jython uses Java HTTP API, CPython uses urllib2
1.3.12 - Add Parallel.append(..) method
1.3.11 - Fix list-of-lists check
1.3.10 - Table: Check 'rows' for list-of-lists
1.3.9 - Seconds parser: Allow float "6.0" or "6.5"
1.3.8 - Table 'Wait For: Completion' support 'Or Time:..'
1.3.7 - Table 'Wait For' logs the name returned by settings, allowing for alias
1.3.6 - Add seconds.formatSecondsAsTime()
1.3.5 - Allow lower-case 'wait for', 'value' columns.
1.3.4 - Allow 'loop' for parallel columns.
1.3.3 - Allow space after 'loop' or 'range'.
1.3.2 - Table scan writes current row to PV settings.table_scan_row.
1.3.1 - Table scan 'time' as alternative for 'seconds'.
1.3.0 - Table scan 'loop' support.
1.2.1 - Table scan '+p' update.
        Used to accumulate _all_ the parallel commands
        on a line. Now only combines adjacent +p columns.
1.1.1 - Allow site-specific ScanSettings to override
        getDefaultSettings() such that is replaces
        the PV name, preserving that name.
1.1.0 - Table scan adds "# Line .." and "# End" comments,
        and also uses the original line number
        in error messages, even for expanded rows.
1.0.9 - Scan settings match the complete name,
        i.e. the pattern is anchored, as if
        there was an implied "^...$" around the pattern.
        Before, it was an implied "^.." only.
1.0.8 - Workaround for 'event executor terminated'
1.0.7 - Support ScanClient.submit(.., queue=False)
1.0.6 - Fix ranges like 'range(1,2,1)' which failed because expansion contains only one item
1.0.5 - Fix table 'Comment' check
1.0.4 - Gnumeric support much faster and lower memory
1.0.3 - Add getDevice() to Loop, Set, Wait commands
1.0.2 - Fix: Default tolerance of Loop, Set, Wait commands
1.0.1 - Fix: Set & Loop command set <wait>false</wait> when no readback desired
1.0.0 - Initial Release
"""

if __name__ == "__main__":
    print(("Version %s" % __version__))
    
    print(version_history)
