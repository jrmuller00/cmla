#
# team object definition file

import math
import sys
import getopt

class cmlaTeam(object):
    """
    A class to store CMLA team information including:
    
    teamName  - Name of the team, ie, STM1
    listIndex - This is the index in the scheduling list or in the standing list
    listOpponents - This is a list of scheduled opponents for the team
    listLocation - This is a list of home 'H' or away 'A'
    listPlusMinus - this is a list of the +/- for the games played max 12 pts for grades 3-4 and max 15 pts for grades 5-8
    listScore - this is list of tuples for the game scores (team's score, opponents score).  This is the actual score and teh +/- is adjusted for in the PlusMinus list
    Grade - This is the team grade

    """
    
    def __init__(self):
        self.teamName = ""
        self.Parish = ""
        self.listIndex = -1
        self.listOpponents = []  
        self.listLocation = []
        self.listPlusMinus = []
        self.listScore = []
        self.Grade = 0
        self.Wins = 0
        self.Losses = 0
        self.Ties = 0
        return

    def setName(self,name):
        self.teamName = name
        return

    def getName(self):
        return self.teamName

    def setGrade(self,grade):
        self.Grade = grade
        return

    def getGrade(self):
        return self.Grade

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

    def setGameScore(self,team, opp):
        self.listScore.append((team,opp))
        diff = team - opp
        if self.Grade < 5:
            if diff > 12:
                diff = 12
        else:
            if diff > 15:
                diff = 15
        self.addPlusMinus(diff)
        if team > opp:
            self.Wins = self.Wins + 1
        elif team < opp:
            self.Losses = self.Losses + 1
        else:
            self.Ties = self.Ties + 1
        return

    def getGameScore(self, index):
        return self.listScore[index]

    def getGameScoreList(self):
        return self.listScore

    def addPlusMinus(self,diff):
        self.listPlusMinus.append(diff)
        return

    def getPlusMinus(self, index):
        return self.listPlusMinus[index]

    def getPlusMinusList(self):
        return self.listPlusMinus

    def getWinPercentage(self):
        TotGames = self.Wins + self.Losses + self.Ties
        if TotGames > 0:
            return self.Wins / TotGames
        else:
            return 0.0

        
                        



