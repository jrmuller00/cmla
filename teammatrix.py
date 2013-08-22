import sys
import getopt
import cmlaTeam as cmla
import random
import tkinter
from tkinter import messagebox
from tkinter import filedialog
from pandas.io.parsers import ExcelFile
import pandas as pd
from openpyxl import Workbook


def getScheduleTable(numTeams):
#
#   make a table of teams
#   initialized to all zeroes

    Filename = str(numTeams) + "teams"
    try:
        if len(scheduleTable) > 0:
            scheduleTable.clear()
    except Exception:
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

def readExcelFile(filename):
    xd = pd.ExcelFile(filename)
    df = xd.parse('Sheet1')
    df.fillna(0,inplace=True)
    parishList = list(df.columns[2:])
    gradeList = list(df.iloc[0:,0])
    genderList = list(df.iloc[0:,1])
    regDict = {}
    for index in range(len(gradeList)):
        tag = str(int(gradeList[index])) + genderList[index][0]
        regDict[tag] = []
        numTeamsList = list(df.iloc[index,2:])
        for pIndex in range(0,len(parishList)):
            regDict[tag].append((parishList[pIndex],int(numTeamsList[pIndex])))

    return regDict


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
            
def makeRegistrationDict(filename):
    regDict = {}

    linenum = 0
    for line in open(filename,"r"):
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
                    gradeGender = tokens[0]
                    parish = tokens[1]
                    numTeams = int(tokens[2])

                    if gradeGender in regDict.keys():
                        regDict[gradeGender].append((parish,numTeams))
                    else:
                        regDict[gradeGender] = []
                        regDict[gradeGender].append((parish,numTeams))


    return regDict


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

def makeGradeGenderTeamList(parishList):
#
#   make a dictionary of all the teams
#   and initialize the object variables

    teamDict = {}
    hasBye = False

    for pairs in parishList:
        (parish, numTeams) = pairs
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
        hasBye = True

    return teamDict, hasBye

def makeSchedule(teamDict, teamsNotPlayed):

    #
    # get a list of teams and the number of teams
    teamList = list(teamDict.keys())
    numTeams = len(teamList)

    #
    # now make a random list of the teams to use for scheduling
    scheduleList = []
    for i in range(numTeams):
        scheduleList.append("empty")

    
    #
    # make a list of parishes

    parishDict = {}

    for team in teamList:
        if team in parishDict:
            parishDict[team] = parishDict[team] + 1
        else:
            parishDict[team] = 1
        
        
    trialNumber = 1
    currentIndex = 0
    makeList = True
    
    while (makeList == True):
        try:
            if trialNumber > 5:
                #
                # sort teams into buckets according to how many each parish submitted
                maxParish = teamList[0][0:2]
                maxTeams = parishDict[maxParish]
                for teamCount in teamList:
                    parish = teamCount[0:2]
                    if parishDict[parish] > maxTeams:
                        maxParish = parish
                        maxTeams = parishDict[parish]


                #
                # now with the maxTeams parish add these teams to a list and choose one

                maxTeamsList = []
                for teams in teamList:
                    if teams[0:2] == maxParish:
                        maxTeamsList.append(teams)

                team = random.choice(maxTeamsList)
            elif trialNumber > 15:
                print ("Couldn't find solution")
                makeList = True
                return
            else:
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
        except:
            trialNumber = trialNumber + 1

    return scheduleList

def updateCMLADict(cmlaDict, scheduleTable, teamList):
    
    index = 0
    for pair in scheduleTable:
        (away, home) = pair
        awayTeam = teamList[away - 1]
        homeTeam = teamList[home - 1]

        if awayTeam == "BYE":
            #
            # need to switch bye from being away to home team
            awayTeam = homeTeam
            homeTeam = "BYE"
            scheduleTable[index] = (home,away)

        cmlaDict[awayTeam].addGame(homeTeam,'a')
        cmlaDict[homeTeam].addGame(awayTeam,'h')
        index = index + 1
    return

def switchBookkeeping(switchHome, switchAway, cmlaDict, scheduleTable):
    switchHomeIndex = cmlaDict[switchHome]
    switchAwayIndex = cmlaDict[switchAway]
    
    switchIndex = 0
    #
    # find the pair in the scedule table
    for pair in scheduleTable:
        (away, home) = pair
        if (away == switchAwayIndex) and (home == switchHomeIndex):
            scheduleTable[switchIndex] = (home, away)
        else:
            switchIndex = switchIndex + 1
            
    cmlaDict[switchHome].flipHomeAway(switchAway)
    cmlaDict[switchAway].flipHomeAway(switchHome)
    return 

    

def loadBalanceSchedule(cmlaDict, scheduleTable, teamList):
    """
    This function will load balance the schedule so that each team 
    has 5 home and 5 away games
    """

    homeGamesList = []
    for i in range(10):
        homeGamesList.append([])

    for key in cmlaDict.keys():
        if key != "BYE":
            numHomeGames = cmlaDict[key].getNumHomeGames()
            homeGamesList[numHomeGames - 1].append(key)

    
    balanced = False
    currentIndex = 9
    while (currentIndex >= 5):
        if len(homeGamesList[currentIndex]) == 0:
            currentIndex = currentIndex - 1
        else:
#           
#           get the team to switch
            
            switchHomeTeam = random.choice(homeGamesList[currentIndex])
#
#           now get the list of teams played
            teamsPlayed = cmlaDict[switchHomeTeam].getHomeGamesList()
            switchFound = False
            searchIndex = 0
            while switchFound == False:
                switchBucket = 0 
                gotList = False
                switchbucket = 0
                while (gotList == False):
                    if len(homeGamesList[switchBucket]) == 0:
                        switchBucket = switchBucket + 1
                    else:
                        switchList = homeGamesList[switchBucket]
                        intersectList = list(set(teamsPlayed).intersection(switchList))
                        if len(intersectList) == 0:
                            switchBucket = switchBucket + 1
                        else:
                            gotList = True
                if len(intersectList) == 0:
                    #print ('No team found to switch home/away', currentIndex, searchIndex)
                    switchFound = True
                else:
                    #print ('Found these teams to switch with',intersectList)
                    #
                    # pick the first team and do the book keeping
                    
                    switchAwayTeam = random.choice(intersectList)
                    switchBookkeeping(switchHomeTeam, switchAwayTeam, cmlaDict, scheduleTable)
                    homeGamesList[currentIndex].remove(switchHomeTeam)
                    homeGamesList[currentIndex - 1].append(switchHomeTeam)
                    homeGamesList[switchBucket].remove(switchAwayTeam)
                    homeGamesList[switchBucket + 1].append(switchAwayTeam)
                    switchFound = True
#            currentIndex = currentIndex - 1
                    

    return

def writeExcelInterimFile(masterSchedule):

    excelFilename = tkinter.filedialog.asksaveasfilename()
    
    keyList = list(masterSchedule.keys())
    keyList.sort()
    #
    # create new workbook
    wb = Workbook()

    for key in keyList:
        #
        # create sheet in file for key
        ws = wb.create_sheet()
        ws.title = key
        (scheduleTable, scheduleList, hasBye) = masterSchedule[key]
        sortedList = []
        for team in scheduleList:
            if team != "BYE":
                sortedList.append(team)
        sortedList.sort()
        if hasBye == True:
            sortedList.append("BYE")
        
        ws.cell(row=0,column=0).value =  key + 'Team List'
        cellrow = 1
        cellcol = 0
        for team in sortedList:
            ws.cell(row=cellrow,column=cellcol).value = team
            cellrow = cellrow + 1

        teamSchedule = []

        cellrow = 0
        cellcol = 3
        ws.cell(row=cellrow,column=cellcol).value = 'Vis'
        ws.cell(row=cellrow,column=cellcol+1).value = 'Hm'
        cellrow = 2
        for game in scheduleTable:
            (away,home) = game
            ws.cell(row=cellrow,column=cellcol).value = scheduleList[away-1]
            ws.cell(row=cellrow,column=cellcol+1).value = scheduleList[home-1]
            cellrow = cellrow + 1

        ws.cell(row=0,column=10).value = 'NOTE:'
        ws.cell(row=1,column=10).value = 'COPY TEAM LIST [COL A] TO [COL M] ON SHEET ' + key
        ws.cell(row=2,column=10).value = "AND COPY SCHEDULE TABLE [COL'S D & E] TO [COL'S D & E] ON SHEET " + key

    wb.save(excelFilename)




    return



        





def main():
    teamListFilename = ""
    registrationFilename = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:n:t:r:",["help","filename="])
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
        if o == "-r":
            registrationFilename = arg

    if registrationFilename == "":
        registrationFilename = tkinter.filedialog.askopenfilename()

    tokens = registrationFilename.split('.')
    numTokens = len(tokens)
    extension = tokens[numTokens-1]

    if extension in ('xls','xlsx'):
        regDict = readExcelFile(registrationFilename)
    else:
        regDict = makeRegistrationDict(registrationFilename)
#       print ("Team list is ", teamListFilename)

    #
    # Now loop over all grade/genders to make the schedule
    rKeys = list(regDict.keys())
    rKeys.sort()
    masterSchedule = {}
    for rKey in rKeys:
        parishList = regDict[rKey]
        cmlaTeamDict, hasBye = makeGradeGenderTeamList(parishList)
        numTeams = len(cmlaTeamDict)
        scheduleTable = getScheduleTable(len(cmlaTeamDict))
        teamsPlayed = getTeamsPlayed(numTeams, scheduleTable)
        teamsNotPlayed = getTeamsNotPlayed(numTeams, teamsPlayed)

        scheduleList = makeSchedule(cmlaTeamDict, teamsNotPlayed)
        updateCMLADict(cmlaTeamDict, scheduleTable, scheduleList)
        loadBalanceSchedule(cmlaTeamDict, scheduleTable, scheduleList)
        print('##########################')
        print('      ',rKey,' Schedule   ')
        print('##########################')
        tKeys = list(cmlaTeamDict.keys())
        tKeys.sort()
        for key in tKeys:
            print ('Team ', key, ' has ',cmlaTeamDict[key].getNumHomeGames(),'home games and ',cmlaTeamDict[key].getNumAwayGames(), ' away games',cmlaTeamDict[key].listOpponents)

        print()
        print()
        masterSchedule[rKey] = (scheduleTable, scheduleList, hasBye)
    writeExcelInterimFile(masterSchedule)
if __name__ == "__main__":
    main()




