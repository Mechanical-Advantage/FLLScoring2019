import numpy as np
import sqlite3 as sql

#Defines the fields stored in the "Scout" table of the database. This database stores the record for each match scan
SCOUT_FIELDS = {
    "Team": 0,
    "Match": 0,
    "Fouls": 0,
    "TechFouls": 0,
    "Replay": 0,
    "Flag": 0,
    "AllianceColor": 0,
    "StartPos": 0,
    "StartLevel": 0,
    "CrossedLine": 0,
    "AutoShipHatch": 0,
	"AutoShipHatchFailures": 0,
	"AutoShipCargo": 0,
	"AutoShipCargoFailures": 0,
    "AutoRocketHatch": 0,
	"AutoRocketHatchFailures": 0,
    "AutoRocketCargo": 0,
	"AutoRocketCargoFailures": 0,
    "RocketL1Hatch": 0,
	"RocketL1HatchFailures": 0,
    "RocketL1Cargo": 0,
	"RocketL1CargoFailures": 0,
    "RocketL2Hatch": 0,
	"RocketL2HatchFailures": 0,
    "RocketL2Cargo": 0,
	"RocketL2CargoFailures": 0,
    "RocketL3Hatch": 0,
	"RocketL3HatchFailures": 0,
    "RocketL3Cargo": 0,
	"RocketL3CargoFailures": 0,
    "ShipHatch": 0,
	"ShipHatchFailures": 0,
    "ShipCargo": 0,
	"ShipCargoFailures": 0,
    "ClimbLevel": 0,
	"ClimbLevelAttempted": 0,
    "WonMatch": 0,
    "LiftedOthers": 0,
	"LiftedOthersAttempted": 0,
    "Disabled": 0,
    "DriverRating": 0,
    "HatchColRating": 0,
    "HatchDelRating": 0,
    "CargoColRating": 0,
    "CargoDelRating": 0,
    "DefenseRating": 0,
    "AvoidDefenseRating": 0
}

#Defines the fields that are stored in the "averages" and similar tables of the database. These are the fields displayed on the home page of the website.
AVERAGE_FIELDS = {
    "team": 0,
    "apr":0,
    "RocketL1Hatch": 0,
    "RocketL1Cargo": 0,
    "RocketL2Hatch": 0,
    "RocketL2Cargo": 0
}

#Defines the fields displayed on the charts on the team and compare pages
CHART_FIELDS = {
    "match": 0,
    "RocketL1Hatch": 0,
    "RocketL1Cargo": 0,
    "RocketL2Hatch": 0,
    "RocketL2Cargo": 0
}


# Main method to process a full-page sheet
# Submits three times, because there are three matches on one sheet
# The sheet is developed in Google Sheets and the coordinates are defined in terms on the row and column numbers from the sheet.
def processSheet(scout):
    for s in (0, 23):
        #Sets the shift value (used when turning cell coordinates into pixel coordinates)
        scout.shiftDown(s)

        num1 = scout.rangefield('J-5', 0, 9)
        num2 = scout.rangefield('J-6', 0, 9)
        num3 = scout.rangefield('J-7', 0, 9)
        num4 = scout.rangefield('J-8', 0, 9)
        scout.set("Team", 1000 * num1 + 100 * num2 + 10 * num3 + num4)

        match1 = scout.rangefield('AB-5', 0, 1)
        match2 = scout.rangefield('AB-6', 0, 9)
        match3 = scout.rangefield('AB-7', 0, 9)
        scout.set("Match", 100 * match1 + 10 * match2 + match3)

        scout.set("Fouls", int(0))
        scout.set("TechFouls", int(0))
        tm = scout.readqrcode("C-6")
        tm1 = tm.split(',')
        scout.set("Team", tm1[0])
        scout.set("Match", tm1[1])
        scout.set("AllianceColor", scout.rangefield('L-10', 0, 1))
        scout.set("StartPos", scout.rangefield('F-10', 0, 2))
        scout.set("StartLevel", scout.rangefield('G-12', 1, 2))
        scout.set("CrossedLine", scout.boolfield('M-12'))
        scout.set("AutoShipHatch", scout.rangefield('T-10', 1, 2))
        scout.set("AutoShipCargo", scout.rangefield('T-11', 1, 2))
        scout.set("AutoShipHatchFailures", scout.rangefield('W-10', 1, 2))
        scout.set("AutoShipCargoFailures", scout.rangefield('W-11', 1, 2))
        scout.set("AutoRocketHatch", scout.rangefield('AE-10', 1, 2))
        scout.set("AutoRocketCargo", scout.rangefield('AE-11', 1, 2))
        scout.set("AutoRocketHatchFailures", scout.rangefield('AH-10', 1, 2))
        scout.set("AutoRocketCargoFailures", scout.rangefield('AH-11', 1, 2))

        scout.set("RocketL1Hatch", scout.rangefield('H-14', 1, 4))
        scout.set("RocketL1HatchFailures", scout.rangefield('M-14', 1, 6))
        scout.set("RocketL2Hatch", scout.rangefield('H-15', 1, 4))
        scout.set("RocketL2HatchFailures", scout.rangefield('M-15', 1, 6))
        scout.set("RocketL3Hatch", scout.rangefield('H-16', 1, 4))
        scout.set("RocketL3HatchFailures", scout.rangefield('M-16', 1, 6))

        scout.set("RocketL1Cargo", scout.rangefield('Y-14', 1, 4))
        scout.set("RocketL1CargoFailures", scout.rangefield('AD-14', 1, 6))
        scout.set("RocketL2Cargo", scout.rangefield('Y-15', 1, 4))
        scout.set("RocketL2CargoFailures", scout.rangefield('AD-15', 1, 6))
        scout.set("RocketL3Cargo", scout.rangefield('Y-16', 1, 4))
        scout.set("RocketL3CargoFailures", scout.rangefield('AD-16', 1, 6))

        scout.set("ShipHatch", scout.rangefield('F-18', 1, 8))
        scout.set("ShipHatchFailures", scout.rangefield('O-18', 1, 8))
        scout.set("ShipCargo", scout.rangefield('F-19', 1, 8))
        scout.set("ShipCargoFailures", scout.rangefield('O-19', 1, 8))

        scout.set("ClimbLevelAttempted", scout.rangefield('G-21', 1, 3))
        scout.set("ClimbLevel", scout.rangefield('G-22', 1, 3))
        scout.set("WonMatch", scout.boolfield('F-24'))
        scout.set("LiftedOthersAttempted", scout.rangefield('P-21', 2, 3))
        scout.set("LiftedOthers", scout.rangefield('P-22', 2, 3))
        scout.set("Disabled", scout.boolfield('F-25'))

        scout.set("DriverRating", scout.rangefield('U-21', 0, 5))
        scout.set("HatchColRating", scout.rangefield('U-22', 0, 1))
        scout.set("HatchDelRating", scout.rangefieldcolumn('AI-18', 0, 5))
        scout.set("CargoColRating", scout.rangefielddebug('AD-19', 0, 1))
        scout.set("CargoDelRating", scout.rangefield('AD-20', 0, 1))
        scout.set("DefenseRating", scout.rangefield('AD-21', 0, 1))
        scout.set("AvoidDefenseRating", scout.rangefield('AD-22', 0, 1))

        scout.set("Replay", scout.boolfield('AK-5'))

        scout.submit()


#Takes an entry from the Scout database table and generates text for display on the team page. This page has 4 columns, currently used for auto, 2 teleop, and other (like fouls and end game)
def generateTeamText(e):
    text = {'auto': "", 'teleop1': "", 'teleop2': "", 'other': ""}
    text['auto'] += 'baseline, ' if e['RocketL1Hatch'] else ''
    text['auto'] += 'Switch try, ' if e['RocketL1Cargo'] else ''
    text['auto'] += 'Scale try, ' if e['RocketL2Hatch'] else ''
    text['auto'] += 'Exchange try, ' if e['RocketL2Cargo'] else ''

    text['teleop1'] += str(
        e['RocketL1Hatch']) + 'x to scale, ' if e['RocketL1Hatch'] else ''

    text['teleop2'] += str(
        e['RocketL1Cargo']) + 'to switch, ' if e['RocketL1Cargo'] else ''
    text['teleop2'] += str(
        e['RocketL2Hatch']) + 'to opp switch, ' if e['RocketL2Hatch'] else ''

    text['other'] = 'Climb, ' if e['Climb'] else ' '


    return text


#Takes an entry from the Scout database table and generates chart data. The fields in the returned dict must match the CHART_FIELDS definition at the top of this file
def generateChartData(e):
    dp = dict(CHART_FIELDS)
    dp["match"] = e['match']

    dp['RocketL1Hatch'] += e['RocketL1Hatch']
    dp['RocketL1Cargo'] += e['RocketL1Cargo']
    dp['RocketL2Hatch'] += e['RocketL2Hatch']
    dp['RocketL2Cargo'] += e['RocketL2Cargo']

    return dp


#Takes a set of team numbers and a string indicating quals or playoffs and returns a prediction for the alliances score and whether or not they will achieve any additional ranking points
def predictScore(datapath, teams, level='quals'):
    conn = sql.connect(datapath)
    conn.row_factory = sql.Row
    cursor = conn.cursor()
    ballScore = []
    endGame = []
    autoGears = []
    teleopGears = []
    for n in teams:
        average = cursor.execute('SELECT * FROM averages WHERE team=?',
                                 (n, )).fetchall()
        assert len(average) < 2
        if len(average):
            entry = average[0]
        else:
            entry = [0] * 8
        autoGears.append(entry[2])
        teleopGears.append(entry[3])
        ballScore.append((entry[5] + entry[6]))
        endGame.append((entry[7]))
    retVal = {'score': 0, 'gearRP': 0, 'fuelRP': 0}
    score = sum(ballScore[0:3]) + sum(endGame[0:3])
    if sum(autoGears[0:3]) >= 1:
        score += 60
    else:
        score += 40
    if sum(autoGears[0:3]) >= 3:
        score += 60
    elif sum(autoGears[0:3] + teleopGears[0:3]) >= 2:
        score += 40
    if sum(autoGears[0:3] + teleopGears[0:3]) >= 6:
        score += 40
    if sum(autoGears[0:3] + teleopGears[0:3]) >= 12:
        score += 40
        if level == 'playoffs':
            score += 100
        else:
            retVal['gearRP'] == 1
    if sum(ballScore[0:3]) >= 40:
        if level == 'playoffs':
            score += 20
        else:
            retVal['fuelRP'] == 1
    retVal['score'] = score
    return retVal


#Takes an entry from the Scout table and returns whether or not the entry should be flagged based on contradictory data.
def autoFlag(entry):
#    if (entry['AutoHighBalls']
#            or entry['TeleopHighBalls']) and (entry['AutoLowBalls']
#                                              or entry['AutoHighBalls']):
#        return 1
#    if entry['Hang'] and entry['FailedHang']:
#        return 1
    return 0


#Takes a list of Scout table entries and returns a nested dictionary of the statistical calculations (average, maxes, median, etc.) of each field in the AVERAGE_FIELDS definition
def calcTotals(entries):
    sums = dict(AVERAGE_FIELDS)
    noDefense = dict(AVERAGE_FIELDS)
    lastThree = dict(AVERAGE_FIELDS)
    noDCount = 0
    lastThreeCount = 0
    for key in sums:
        sums[key] = []
    #For each entry, add components to the running total if appropriate
    for i, e in enumerate(entries):
        sums['RocketL1Hatch'].append(e['RocketL1Hatch'])
        sums['RocketL1Cargo'].append(e['RocketL1Cargo'])
        sums['RocketL2Hatch'].append(e['RocketL2Hatch'])
        sums['RocketL2Cargo'].append(e['RocketL2Cargo'])

        if i < 3:
            lastThree['RocketL1Hatch'] += e['RocketL1Hatch']
            lastThree['RocketL1Cargo'] += e['RocketL1Cargo']
            lastThree['RocketL2Hatch'] += e['RocketL2Hatch']
            lastThree['RocketL2Cargo'] += e['RocketL2Cargo']
            lastThreeCount += 1

    #If there is data, average out the last 3 or less matches
    if (lastThreeCount):
        for key, val in lastThree.items():
            lastThree[key] = round(val / lastThreeCount, 2)

    #If there were matches where the team didn't play D, average those out
    if (noDCount):
        for key, val in noDefense.items():
            noDefense[key] = round(val / noDCount, 2)

    average = dict(AVERAGE_FIELDS)
    median = dict(AVERAGE_FIELDS)
    maxes = dict(AVERAGE_FIELDS)
    for key in sums:
        if key != 'team' and key != 'apr':
            average[key] = round(np.mean(sums[key]), 2)
            median[key] = round(np.median(sums[key]), 2)
            maxes[key] = round(np.max(sums[key]), 2)
    retVal = {
        'averages': average,
        'median': median,
        'maxes': maxes,
        'noDefense': noDefense,
        'lastThree': lastThree
    }

    #Calculate APRs. This is an approximate average points contribution to the match
    for key in retVal:
        apr = 100
#        apr = retVal[key]['autoballs'] + retVal[key]['teleopballs'] + retVal[key]['end']
#        if retVal[key]['autogear']:
#            apr += 20 * min(retVal[key]['autogear'], 1)
#        if retVal[key]['autogear'] > 1:
#            apr += (retVal[key]['autogear'] - 1) * 10
#
#            min(retVal[key]['teleopgear'], 2 - retVal[key]['autogear']) * 20,
#            0)
#        if retVal[key]['autogear'] + retVal[key]['teleopgear'] > 2:
#            apr += min(retVal[key]['teleopgear'] + retVal[key]['autogear'] - 2,
#                       4) * 10
#        if retVal[key]['autogear'] + retVal[key]['teleopgear'] > 6:
#            apr += min(retVal[key]['teleopgear'] + retVal[key]['autogear'] - 6,
#                       6) * 7
        apr = int(apr)
        retVal[key]['apr'] = apr

    return retVal
