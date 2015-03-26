"""
Seconds parser
--------------

.. moduleauthor:: Kay Kasemir
"""
import re

def parseSeconds(text):
    """Parse various time durations into seconds
    
    :param text: Text that contains a duration
    :return: Seconds
     
    Convert text that contains "HH:MM:SS" into seconds
    
    >>> parseSeconds("00:00:01")
    1
    >>> parseSeconds("120")
    120
    >>> parseSeconds("01:01:01")
    3661
    >>> parseSeconds("2:01")
    121
    >>> parseSeconds("02:01")
    121
    >>> parseSeconds("48000")
    48000
    
    Can also be called with number:
    
    >>> parseSeconds(120)
    120
    """
    if not isinstance(text, str):
        return text # Assume it's already a number
    match = re.match("([0-9]+):([0-9]+):([0-9]+)", text)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        return (hours*60 + minutes)*60 + seconds
    match = re.match("([0-9]+):([0-9]+)", text)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        return minutes*60 + seconds
    try:
        return int(text)
    except:
        raise Exception("Cannot parse seconds from '%s'" % text)

if __name__ == "__main__":
    print "Performing doctest..."
    import doctest
    doctest.testmod()
    