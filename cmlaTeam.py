#
# team object definition file

import math
import sys
import getopt

class cmlaTeam(object):
    """
    A class to store CMLA team information including:
    
    teamName  - Name of the team, ie, STM1
    Index - This is the index in the scheduling list or in the standing list
    listOpponents - This is a list of scheduled opponents for the team
    listLocation - This is a list of home 'H' or away 'A'
    listPlusMinus - this is a list of the +/- for the games played max 12 pts for grades 3-4 and max 15 pts for grades 5-8
    listScore - this is list of tuples for the game scores (team's score, opponents score).  This is the actual score and teh +/- is adjusted for in the PlusMinus list
    Grade - This is the team grade
    Wins  - number of team wins
    Losses - number of team losses
    Ties - number of team ties
    PF - total points for over the course of the season
    PA- total PA over the course of the season
    SoS  - team strength of schedule

    """
    
    def __init__(self):
        self.teamName = ""
        self.Parish = ""
        self.Index = -1
        self.listOpponents = []  
        self.listLocation = []
        self.listPlusMinus = []
        self.listScore = []
        self.Grade = 0
        self.Wins = 0
        self.Losses = 0
        self.Ties = 0
        self.PF = 0
        self.PA = 0
        self.SoS = 0.0
        return
    #
    # set the object team name
    def setName(self,name):
        """
        setName will set the object team name
            string  name

            return value: Null
        """
        self.teamName = name
        return

    #
    # get the object team name
    def getName(self):
        """
        getName will return the object team name as a string

            return value: string    self.teamName
        """
        return self.teamName

    #
    # set the team grade (3-8)
    def setGrade(self,grade):
        """
        setGrade will set the object grade value 3-8.
        The grade is used for calculating the +/- for the team
        (max 12 for grades 3-4 and max 15 for grades 5-8)
        and for generating overall league standings
        
            grade:  integer

            return value: Null
        """
        self.Grade = grade
        return

    def getGrade(self):
        """
        getGrade will get the object grade value 3-8.
        The grade is used for calculating the +/- for the team
        (max 12 for grades 3-4 and max 15 for grades 5-8)
        and for generating overall league standings
        
            return value: int grade 
        """
        return self.Grade
    #
    # Set the team parish
    def setParish(self, parish):
        """
        setParish will set the object parish.  this value is used for
        easily grouping teams from the same parish
                
            string  parish

            return value: Null
        """
        self.Parish = parish
        return

    def getParish(self):
        """
        getParish will return the parish name for the object.  This value is 
        used for easily grouping teams from the same parish
        
            return value: string self.Parish
        """
        return self.Parish

    #
    # set the list index
    def setIndex(self,index):
        """
        setListIndex will set the object list index.  The list index
        is used in scheduling to determine where the team falls in the 
        scheduling table and also in the standings to determine where
        the team's final standing. 
        
            int index

            return value: Null
        """
        self.Index = index
        return
    #
    # get the list index
    def getIndex(self):
        """
        getIndex will return the object list index value.
        The list index is used in scheduling to determine where 
        the team falls in the scheduling table and also in the 
        standings to determine where the team's final standing. 
        
            return value: int   self.Index
        """
        return self.Index


    #
    # addGame - adds game to Team schedule
    def addGame(self,opp,loc):
        """
        addGame will add a game to the team schedule.  It includes the opponent
        team name and the location 'h' for home and 'a' for away

            string  opp
            string  loc

            return value: Null
        """
        
        if len(self.listOpponents) == len(self.listLocation):
            self.listOpponents.append(opp)
            self.listLocation.append(loc)
        else:
            print ("Game not added, list lengths not equal")
        return 


    #
    # clearGames  - clears the list of games in the object list
    def clearGames(self):
        """
        clearGames will clear all the opponenets list and the locations list

            return: Null
        """
        self.listOpponents.clear()
        self.listLocation.clear()
        return


    #
    # getNumHomeGames will return the total number of home games for the team
    def getNumHomeGames(self):
        """
        getNumHomeGames will return the total number of home games
        for the team as listed in the location list.  This is used
        to balance the schedule as best as possible to 5 home
        and 5 away

        Note: Bye games are always away

        return: int 

        """
        numHome = 0
        for game in self.listLocation:
            if game == 'h':
                numHome = numHome + 1
        return numHome

    #
    # getNumAwayGames
    def getNumAwayGames(self):
        """
        getNumAwayGames will return the total number of home games
        for the team as listed in the location list.  This is used
        to balance the schedule as best as possible to 5 home
        and 5 away

        Note: Bye games are always away

        return: int 

        """
        numAway = 0
        for game in self.listLocation:
            if game == 'a':
                numAway = numAway + 1
        return numAway
    
    #
    # flipHomeAway - flip the location for a specified game
    def flipHomeAway(self,opponent):
        """
        flipHomeAway will flip the location for a specified
        game in the opponents and location list. The function 
        takes the opponents name as an argument and finds 
        the game on the list and flips h/a

            int opponent

            return value: Null
        """
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

    #
    # getOpponentList - will return a list of opponent team names
    def getOpponentList(self):
        """
        getOpponentList lreturns a list of all opponents

        return: list    self.listOpponents
        """
       
        return self.listOpponents
        
    #
    # getHomeGamesList - will return a list of home game opponent team names
    def getHomeGamesList(self):
        """
        getHomeGamesList loops over all games and creates a list 
        of all the home games for the object

        return: list    homeList
        """
        homeList = []
        index = 0
        for loc in self.listLocation:
            if loc == 'h':
                homeList.append(self.listOpponents[index])
            index = index + 1
                
        return homeList
        
    #
    # getAwayGamesList - will return a list of away game opponent team names
    def getAwayGamesList(self):
        """
        getAwayGamesList loops over all games and creates a list 
        of all the away games for the object

        return: list    awayList
        """
        awayList = []
        index = 0
        for loc in self.listLocation:
            if loc == 'a':
                awayList.append(self.listOpponents[index])
            index = index + 1
                
        return awayList

    #
    # setGameScore - will set the scores for the object team and the opponent
    def setGameScore(self,team, opp, byeGame=False):
        """
        setGameScore will set the final game scores for the object team
        and the opponent.  It will also update the +/- for the team and 
        the total number of wins, losses or ties depending on the score.
        The boolean flag is set to true if the game was a bye week for 
        the team and false if it was a regular game.  If it was a bye 
        the score is registered (0 to 0) but the game is not listed as a 
        tie.

            int     team    - object team score for game
            int     opp     - opponents team score for the game
            bool    byeGame - Boolean to determine if the opponent is 'BYE'
                                (default is False)

            return value: Null
        """
        self.listScore.append((team,opp))
        self.PF = self.PF + team
        self.PA = self.PA + opp
        diff = team - opp
        if self.Grade < 5:
            if diff > 12:
                diff = 12
            elif diff < -12:
                diff = -12
        else:
            if diff > 15:
                diff = 15
            elif diff < -15:
                diff = -15
        self.addPlusMinus(diff)
        
        if team > opp:
            self.Wins = self.Wins + 1
        elif team < opp:
            self.Losses = self.Losses + 1
        else:
            if byeGame == False:
                self.Ties = self.Ties + 1
        return

    #
    # getGameScore - returns a score for a single game
    def getGameScore(self, index):
        """
        getGameScore will return the score for a single game during the teams 
        season.  The user must pass the index of the game (ie, the game 
        number during the season)

        int index   - game number NOTE: this is between 0 and Number of season games - 1

        Return value:   tuple   (team score, opponent score)
        
        """
        return self.listScore[index]

    #
    # getGameScoreList - will return the list of score for the season
    def getGameScoreList(self):
        """
        getGameScoreList will return the scores for the season in the
        form of a list of tuples
       
        
        Return value:   list of tuples   self.listScore (team score, opponent score)
        
        """
        return self.listScore

    #
    # addPlusMinus - will add teh score difference for a game to a list of all +/- for the season
    def addPlusMinus(self,diff):
        """
        addPlusMinus will add the score difference for a game to a list of all differences.
        These +/- values are used in case of a tie at the end of the season to determine
        final standings and ultimately tournament seedings

            int     diff    (score difference grades 3-4, max 12, grades 5-8 max 15)

            Return value:   Null
        """
        self.listPlusMinus.append(diff)
        return

    #
    # getplusMinus - will return the score difference for a specific game given the game index
    def getPlusMinus(self, index):
        """
        getPlusMinus will get the score difference for a specific game given the
        game index These +/- values are used in case of a tie at the end of the 
        season to determine final standings and ultimately tournament seedings

            int     index     

            Return value:   self.listPlusMinus[index]
        """
        return self.listPlusMinus[index]

    def getPlusMinusList(self):
        """
        getPlusMinus will get the score difference for a specific game given the
        game index These +/- values are used in case of a tie at the end of the 
        season to determine final standings and ultimately tournament seedings

            int     index     

            Return value:   self.listPlusMinus[index]
        """

        return self.listPlusMinus
    #
    # getWinPercentage - will return the winning percentage for a team
    def getWinPercentage(self):
        """
        getWinPercentage will calculate the winning percentage for a team
        given the list of scores entered. The formula is 

            Winning Percentage = [Wins]/[Wins + Losses + Ties]

            if [Wins + Losses + Ties] > 0
            else 0.0

            
            Return value:   Winning Percentage
        """
        TotGames = self.Wins + self.Losses + self.Ties
        if TotGames > 0:
            return self.Wins / TotGames
        else:
            return 0.0

    #
    # getOpponentInfo will get game location 'h' or 'a' and the score
    def getOpponentInfoOld(self, team):
        """

        here is the one i just looked at 

        getOpponentInfo will take a team name and search if the team is listed 
        in listOpponents.  If yes, the function will return the location (home or away)
        and the score (if it exists).  If the game exists but no score, the score tuple
        will be (-1, -1)

        string  team

        Return value: tuple (Boolean, location, tuple (team score, opponent score))

        """
        index = 0
        exists = False
        location = 'na'
        score = (-1,-1)
        for index in range(len(self.listOpponents)):
            if team.lower() == self.listOpponents[index]:
                #
                # team exists, get game location
                exists = True
                location = self.listLocation[index]
                if len(self.listScore) > index:
                    score = self.listScore[index]
                break

        return (exists, location, score)

    #
    # getActualPointDifferential will return the total point differential for the team

    def getActualPointDifferential(self):
        """
        getPointDifferential will return the total point differential 
        for the team over the course of the season

            Return value:   int pointDifferential [PF - PA]


        """

        return self.PF - self.PA

    #
    # getAdjustedPointDifferential will return the adjusted point differential (max 15 or 12)

    def getAdjustedPointDifferential(self):
        """
        getAdjustedPointDifferential will return the adjusted total point differential 
        for the team over the course of the season.  According to CMLA rules
        the max DP per game is 15 pts for grades 5-8 and 12 pts for grades 3-4

            Return value:   int adjustedDP = SUM (self.listPlusMinus)


        """

        sumDP = 0
        for dp in self.listPlusMinus:
            sumDP = sumDP + dp

        return sumDP



    #
    # getPFSeasonAvg will return the average PF for the team over the course of the season

    def getPFSeasonAvg(self):
        """
        getPFSeasonAvg will return the average "Points For" for the team, i.e.,

        [Total Points Scored]/[Number of Games Played]

        Return Value: float avgPF

        """
        totalGames = 0
        totalGames = self.Wins + self.Losses + self.Ties

        if totalGames > 0:
            return self.PF / totalGames
        else:
            return 0.0


    #
    # getPASeasonAvg will return the average PA for the team over the course of the season

    def getPASeasonAvg(self):
        """
        getPASeasonAvg will return the average "Points Against" for the team, i.e.,

        [Total Points Scored by Opponents]/[Number of Games Played]

        Return Value: float avgPA

        """
        totalGames = 0
        totalGames = self.Wins + self.Losses + self.Ties

        if totalGames > 0:
            return self.PA / totalGames
        else:
            return 0.0

    #
    # getTotalGamesPlayed will return the total number of games played (does not include Bye's)

    def getTotalGamesPlayed(self):
        """
        getTotalGamesPlayed will return the total number
        of games played by the team.  This does not include
        bye games

        Return value: total games played

        """
        return self.Wins + self.Losses + self.Ties

    def setSoS(self, SoS):
        """
        setSoS will return the strentgh of schedule calculated for the team
         
            float   SoS     team strength of schedule
        
        """

        self.SoS = SoS
        return

    def getSoS(self):
        """
        getSoS will return the strentgh of schedule calculated for the team
        
            Return value:
                float   self.Sos

        """

        return self.SoS

    def getWins(self):
        """
        getWins returns the number of wins currently entered for the team

            Return value:
                
                int     self.Wins   
        """
        return self.Wins

    def getLosses(self):
        """
        getLosses returns the number of losses currently entered for the team

            Return value:
                
                int     self.Losses
        """
        return self.Losses

    def getTies(self):
        """
        getTies returns the number of ties currently entered for the team

            Return value:
                
                int     self.Ties
        """
        return self.Ties

    #
    # get the opponent index if it exists
    def getOpponentIndex(self, opp):
        """
        getOpponentIndex will return the list index
        for the specified opponent if it exists.
        If it's not found it will return -1

        string  opp - opponent team name

        Return value: int   list index (-1 if not found)
        """
        oppIndex = -1
        for index in range(len(self.listOpponents)):
            if opp == self.listOpponents[index]:
                oppIndex = index
        return oppIndex

    #
    # get the opponent info if it exists
    def getOpponentInfo(self, opp):
        """
        getOpponentInfo will return the opponent
        information in the form of a tuple if it exists.
        (list index, location, (team score, opp score))

        If any or all info is not found it will return 

        (-1, "", (-1,-1))

        string  opp - opponent team name

        Return value: tuple (int: list index (-1 if not found), string: game location (empty if not found),tuple: (teamscore, opp score) (-1,-1) if not found)
        """
        
        oppIndex = -1
        gameLocation = ""
        gameScore = (-1,-1)
        #
        # search opponent list to find index
        for index in range(len(self.listOpponents)):
            if opp == self.listOpponents[index]:
                oppIndex = index

        if oppIndex >= 0:
            #
            # found index, check for additional info
            if len(self.listLocation) > oppIndex:
                gameLocation = self.listLocation[oppIndex]

            if len(self.listScore) > oppIndex:
                gameScore = self.listScore[oppIndex]

        return (oppIndex, gameLocation, gameScore)


       

        
                        



