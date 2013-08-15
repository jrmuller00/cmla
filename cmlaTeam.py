#
# team object definition file

import math
import sys
import getopt

class cmlaTeam(object):
    """
    A class to store CMLA team information including:
    
    teamName
    listIndex
    listOpponents
    listLocation

    """
    
    def __init__(self):
        self.teamName = ""
        self.Parish = ""
        self.listIndex = -1
        self.listOpponents = []
        self.listLocation = []
        return

    def setName(self,name):
        self.teamName = name
        return

    def getName(self):
        return self.teamName

    def setParish(self, parish):
        self.Parish = parish
        return

    def getParish(self):
        return self.Parish

    def setListIndex(self,index):
        self.listIndex = index
        return

    def addGame(self,opp,loc):
        if len(self.listOpponents) == len(self.listLocation):
            self.listOpponents.append(opp)
            self.listLocation.append(loc)
        else:
            print ("Game not added, list lengths not equal")
        return 

    def clearGames(self):
        self.listOpponents.clear()
        self.listLocation.clear()
        return

    def getNumHomeGames(self):
        numHome = 0
        for game in self.listLocation:
            if game == 'h':
                numHome = numHome + 1
        return numHome

    def getNumAwayGames(self):
        numAway = 0
        for game in self.listLocation:
            if game == 'a':
                numAway = numAway + 1
        return numAway



