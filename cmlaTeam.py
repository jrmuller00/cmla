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
    def getListIndex(self):
        return self.listIndex

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
        
    def flipHomeAway(self,opponent):
        index = 0
        for team in self.listOpponents:
            if team == opponent:
                if self.listLocation[index] == 'a':
                    self.listLocation[index] = 'h'
                else:
                    self.listLocation[index] = 'a'
            else:
                index = index + 1
        return
        
        
    def getHomeGamesList(self):
        homeList = []
        index = 0
        for loc in self.listLocation:
            if loc == 'h':
                homeList.append(self.listOpponents[index])
            index = index + 1
                
        return homeList
        
        
    def getAwayGamesList(self):
        awayList = []
        index = 0
        for loc in self.listLocation:
            if loc == 'a':
                awayList.append(self.listOpponents[index])
            index = index + 1
                
        return awayList
        
                        



