
__version__ = '1.3.4'

version_history = """
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
    print("Version %s" % __version__)
    
    print(version_history)
