#!/usr/bin/env python3
"""reducer.py"""

import sys

currPage = None
currOutLinks = None
incomingPageRankSum = 0
dampingFactor = 0.85

def processInfo(info : str, 
                incomingPageRankSum : float, 
                currOutLinks : str):
    """
    Returns:
        a tuple of updated values of incomingPageRankSum, currOutLinks
    """
    info = info.split('\t', maxsplit=1)
    if len(info) == 1: # info contains an incoming page rank
        incomingPageRankSum += float(info[0])
    else: # info contains the out going links
        currOutLinks = info[1].strip()
    
    # return updated values
    return incomingPageRankSum, currOutLinks

for line in sys.stdin:
    line = line.strip()
    if line == '': continue

    # * info will contain 1 element for incoming page rank and more than 1 for page info
    page, info = line.split('\t', maxsplit=1)

    if page == currPage: # update using current info
        incomingPageRankSum, currOutLinks = processInfo(info, incomingPageRankSum, currOutLinks)
    else:
        if currPage is not None:
            print(f'{currPage}\t{(1-dampingFactor) + dampingFactor * incomingPageRankSum}\t{currOutLinks}')
        
        currPage = page
        incomingPageRankSum = 0
        currOutLinks = None

        # update using current info
        incomingPageRankSum, currOutLinks = processInfo(info, incomingPageRankSum, currOutLinks)
print(f'{currPage}\t{(1-dampingFactor) + dampingFactor * incomingPageRankSum}\t{currOutLinks}')