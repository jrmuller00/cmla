import sys
import getopt
import cmlaTeam as cmla
import random

def getScheduleTable(numTeams):
#
#   make a table of teams
#   initialized to all zeroes

    Filename = str(numTeams) + "teams"
    scheduleTable = []

    linenum = 0
    for line in open(Filename,"r"):
        # print (line)
        tokens = line.split()
        linenum = linenum + 1
#        print (tokens)
        if len(tokens) > 1:
            if tokens[0] == "#":
                # comment line ignore
                print ('Comment ',line)
                pass
            else:
#                print (tokens)
                if len(tokens) == 3:
                    team1 = int(tokens[0])
                    team2 = int(tokens[2])
                    scheduleTable.append((team1, team2))
    return scheduleTable

def getTeamMatrix(scheduleTable):
#
#   make a table of teams
#   initialized to all zeroes

    teamMatrix = []

    for i in range(len(scheduleTable)):
        teamMatrix.append([])
        for j in range(len(scheduleTable)):
            teamMatrix[i].append(0)

    for pair in scheduleTable:
        (team1, team2) = pair
        teamMatrix[team1-1][team2-1] = 1
        teamMatrix[team2-1][team1-1] = 1
    return teamMatrix

def getTeamsPlayed(numTeams, scheduleTable):
    """
    This function will create a matrix of teams
    played from the scheudle table
    """
    teamsPlayed = []
    for i in range(numTeams):
        teamsPlayed.append([])

    for pair in (scheduleTable):
        (team1, team2) = pair
        teamsPlayed[team1-1].append(team2)
        teamsPlayed[team2-1].append(team1)

    return teamsPlayed

def getTeamsNotPlayed(numTeams, teamsPlayed):
    teamsNotPlayed = []
    for i in range(numTeams):
        teamsNotPlayed.append([])
        for j in range(numTeams):
            teamsNotPlayed[i].append(j+1)

    for i in range(numTeams):
        teamsNotPlayed[i].remove(i+1)
        for j in range(len(teamsPlayed[i])):
            teamsNotPlayed[i].remove(teamsPlayed[i][j])

    return teamsNotPlayed
            

def makeTeamDict(teamFilename):
#
#   make a dictionary of all the teams
#   and initialize the object variables

    teamDict = {}

    linenum = 0
    for line in open(teamFilename,"r"):
        # print (line)
        tokens = line.split()
        linenum = linenum + 1
#        print (tokens)
        if len(tokens) > 1:
            if tokens[0] == "#":
                # comment line ignore
                print ('Comment ',line)
                pass
            else:
#                print (tokens)
                if len(tokens) == 2:
                    parish = tokens[0]
                    numTeams = int(tokens[1])
                    for i in range(numTeams):
                        newTeam = cmla.cmlaTeam()
                        teamName = parish +str(i+1)
                        newTeam.setName(teamName)
                        newTeam.setParish(parish)
                        teamDict[teamName] = newTeam
#    print ('In makeTeamDict',len(teamDict))
    if len(teamDict) % 2 == 1:
#
#       odd number of teams add BYE
        print ('Odd number of teams; Add BYE')
        newTeam = cmla.cmlaTeam()
        newTeam.setName("BYE")
        newTeam.setParish("BYE")
        teamDict["BYE"] = newTeam

    return teamDict

def makeSchedule(teamDict, teamsNotPlayed):

    #
    # get a list of teams and the number of teams
    teamList = teamDict.keys()
    numTeams = len(teamList)

    #
    # now make a random list of the teams to use for scheduling
    scheduleList = []
    for i in range(numTeams):
        scheduleList.append("empty")
    currentIndex = 0

    makeList = True
    
    while (makeList == True):
        team = random.choice(teamList)
        # 
        # add the team to the schedule list
        while scheduleList[currentIndex] != "empty":
            currentIndex = currentIndex + 1
        scheduleList[currentIndex] = team
        teamDict[team].setListIndex(currentIndex)
        teamList.remove(team)
        #
        # now need to find any other teams from that parish
        # and add them to the schedule list

        noPlayIndicies = []
        noPlayIndicies.append(currentIndex)

        for otherTeam in teamList:
            if team[:2] == otherTeam[:2]:
#                print ('Found same parish ',team, otherTeam)
                #
                # need to pull them from the team list
                # and add them to the schedule list in a slot that 
                # does not play "team"
                emptySpot = False
                while emptySpot == False:
                    #
                    # get a set of viable teams to play
                    viableTeams = []
                    for k in range(len(noPlayIndicies)):
                        if k == 0:
                            viableTeams = teamsNotPlayed[noPlayIndicies[k]]
                        else:
                            viableTeams = set(viableTeams).intersection(teamsNotPlayed[k])
                        
                    addIndex = random.choice(viableTeams) - 1 
                    if scheduleList[addIndex] == 'empty':
                        emptySpot = True
                    else:
                        teamsNotPlayed[currentIndex].remove(addIndex + 1)
                
                scheduleList[addIndex] = otherTeam
                teamDict[otherTeam].setListIndex(addIndex)
                teamList.remove(otherTeam)
        
        if len(teamList) == 0:
            makeList = False

    return scheduleList

def updateCMLADict(cmlaDict, scheduleTable, teamList):
    
    for pair in scheduleTable:
        (away, home) = pair
        awayTeam = teamList[away - 1]
        homeTeam = teamList[home - 1]
        cmlaDict[awayTeam].addGame(homeTeam,'a')
        cmlaDict[homeTeam].addGame(awayTeam,'h')
    return


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:n:t:",["help","filename="])
    except getopt.error as msg:
        print (msg)
        print ("for help use --help")
        sys.exit(2)

    for o, arg in opts:
#        print (o, arg)
        if o == "-h":
            print ("python teammatrix.py [filename]")
        if o == "-f":
            filename = arg
        if o == "-n":
            numTeams = int(arg,10)
        if o == "-t":
            teamListFilename = arg

#    print ("Team list is ", teamListFilename)
    cmlaTeamDict = makeTeamDict(teamListFilename)
#    print ("Num teams = ",len(cmlaTeamDict))
    numTeams = len(cmlaTeamDict)
#    print (cmlaTeamDict)
    scheduleTable = getScheduleTable(len(cmlaTeamDict))
    teamsPlayed = getTeamsPlayed(numTeams, scheduleTable)
    teamsNotPlayed = getTeamsNotPlayed(numTeams, teamsPlayed)
#    print scheduleTable
    scheduleList = makeSchedule(cmlaTeamDict, teamsNotPlayed)
    updateCMLADict(cmlaTeamDict, scheduleTable, scheduleList)

    for key in cmlaTeamDict.keys():
        print 'Team ', key, ' has ',cmlaTeamDict[key].getNumHomeGames(),' and ',cmlaTeamDict[key].getNumAwayGames(), ' away games',cmlaTeamDict[key].listOpponents


if __name__ == "__main__":
    main()




