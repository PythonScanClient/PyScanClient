
__version__ = '1.0.3'

version_history = """
1.0.3 - Add getDevice() to Loop, Set, Wait commands
1.0.2 - Fix: Default tolerance of Loop, Set, Wait commands
1.0.1 - Fix: Set & Loop command set <wait>false</wait> when no readback desired
1.0.0 - Initial Release
"""

if __name__ == "__main__":
    print "Version ", __version__
    
    print version_history