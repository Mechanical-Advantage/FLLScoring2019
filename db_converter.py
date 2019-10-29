import sqlite3 as sql
import time

scoring = {
    8: 20, #M01a
    9: 15, #M01b
    10: 20, #M02a
    11: 15, #M02b
    12: 15, #M02c
    13: 10, #M03a
    14: 10, #M04a
    15: 10, #M05a
    16: 15, #M05b
    17: 10, #M06a
    18: 20, #M07a
    20: 10, #M09a
    21: 20, #M10a
    23: 10, #M12a
    24: 5, #M12b
    25: 10 #M13a
}
mission_lookup = [1, 1, 2, 2, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11, 12, 12, 13]
scoring_extra = {
    "M08a": {
        0: 0,
        1: 15,
        2: 20
    },
    "M11a": {
        0: 0,
        1: 10,
        2: 15
    },
    "M14a": {
        0: 0,
        1: 5,
        2: 10,
        3: 20,
        4: 30,
        5: 45,
        6: 60
    }
}

while True:
    print("Refreshed at", time.ctime())

    conn = sql.connect('data_2019scrimmage.db')
    conn2 = sql.connect('fllipit\\fllipit.db')
    conn_playoff_display = sql.connect('..\\playoffdisplay\\playoffs.db')
    team_conn = sql.connect('teams.db')
    cur = conn.cursor()
    cur2 = conn2.cursor()
    cur_playoff_display = conn_playoff_display.cursor()
    team_cur = team_conn.cursor()
    team_cur.execute("SELECT * FROM master_teams order by team")
    teamscores=[]
    teamdata = team_cur.fetchall()
    cur_playoff_display.execute("DELETE FROM match_scores")

    for i in range (0,len(teamdata)):
        teamscores.append([0,'','',0,0,0,0,0,0,0,0,0,0])

    for i in range(0,len(teamdata)):
        cur.execute("SELECT * FROM scout WHERE team=? ORDER BY match LIMIT 5",(teamdata[i][0],))
        count = 3
        matchdata = cur.fetchall()
        teamscores[i][0]=teamdata[i][0]
        teamscores[i][1]=teamdata[i][1]
        teamscores[i][2]=teamdata[i][2]
        for z in range(0,len(matchdata)):
            matchscore = 0
            for key, score in scoring.items():
                matchscore += matchdata[z][key] * score
            matchscore += scoring_extra["M08a"][matchdata[z][19]]
            matchscore += scoring_extra["M11a"][matchdata[z][22]]
            matchscore += scoring_extra["M14a"][matchdata[z][26]]
            smallinspection = matchdata[z][27] == 1
            if smallinspection:
                missionscomplete = [False] * 13
                for fieldnumber in range(18):
                    if matchdata[z][fieldnumber + 8] > 0:
                        missionscomplete[mission_lookup[fieldnumber]-1] = True
                for f in range(len(missionscomplete)):
                    if missionscomplete[f]:
                        if f == 1:
                            matchscore += 10
                        else:
                            matchscore += 5
            teamscores[i][count]=matchscore
            teamscores[i][count+1] = 6 - matchdata[z][26]
            count = count + 2

            if matchdata[z][2] >=60:
                cur_playoff_display.execute("INSERT INTO match_scores(match, team, score, penalties) VALUES (?, ?, ?, ?)", (matchdata[z][2], matchdata[z][1], matchscore, 6 - matchdata[z][26]))
            else:
                teamscores[i][count]=matchscore
                teamscores[i][count+1] = 6 - matchdata[z][26]
                count = count + 2

    cur2.execute("DELETE FROM team")
    
    for i in range(0,len(teamscores)):
        insertCommand = """INSERT INTO 'team' ('number','name','affiliation', 'round1', 'round1penalties', 'round2', 'round2penalties', 'round3', 'round3penalties', 'round4', 'round4penalties', 'round5', 'round5penalties') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""
        insert_data = ()
        for f in range(0, 13):
            insert_data += (teamscores[i][f],)
        cur2.execute(insertCommand, insert_data)


    conn2.commit()
    conn_playoff_display.commit()
    conn.close()
    conn2.close()
    conn_playoff_display.close()
    team_conn.close()
    time.sleep(15)
