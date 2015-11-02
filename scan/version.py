
__version__ = '1.0.7'

version_history = """
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
    print "Version ", __version__
    
    print version_history
