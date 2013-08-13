import sys
import getopt
import cmlaTeam as cmla

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
    print ('In makeTeamDict',len(teamDict))
    if len(teamDict) % 2 == 1:
#
#       odd number of teams add BYE
        print ('Odd number of teams; Add BYE')
        newTeam = cmla.cmlaTeam()
        newTeam.setName("BYE")
        newTeam.setParish("BYE")
        teamDict["BYE"] = newTeam

    return teamDict


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:n:t:",["help","filename="])
    except getopt.error as msg:
        print (msg)
        print ("for help use --help")
        sys.exit(2)

    for o, arg in opts:
        print (o, arg)
        if o == "-h":
            print ("python teammatrix.py [filename]")
        if o == "-f":
            filename = arg
        if o == "-n":
            numTeams = int(arg,10)
        if o == "-t":
            teamListFilename = arg

    print ("Team list is ", teamListFilename)
    cmlaTeamDict = makeTeamDict(teamListFilename)
    print ("Num teams = ",len(cmlaTeamDict))
    numTeams = len(cmlaTeamDict)
    print (cmlaTeamDict)
    scheduleTable = getScheduleTable(len(cmlaTeamDict))
    teamsPlayed = getTeamsPlayed(numTeams, scheduleTable)
    teamsNotPlayed = getTeamsNotPlayed(numTeams, teamsPlayed)
#    print scheduleTable
    for i in range(len(teamsPlayed)):
        print ('team ',i+1, ' plays ',teamsPlayed[i])

    for i in range(len(teamsNotPlayed)):
        print ('team ',i+1, ' does not play ',teamsNotPlayed[i])


if __name__ == "__main__":
    main()




