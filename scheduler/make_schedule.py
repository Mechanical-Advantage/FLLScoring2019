import sqlite3 as sql
import math

#Config
teams_db = "../teams.db"
config = {
"match_paircount": 3, # how many pairs of tables are available for matches?
"match_starttime": 1575640800, # unix time, when does the first match begin?
"match_cycletime": 480, # secs, how long between the start of each match?
"match_breakfrequency": 6, # how many matches should be played between each break?
"match_breaklength": 2, # how many matches should each break last?
"judging_roomcount": 2, # how many rooms are available FOR EACH CATEGORY?
"judging_start": 1575640800, # unix time, when does the first judging session begin?
"judging_inlength": 600, # secs, how long does each judging session take?
"judging_outlength": 600, # secs, how long should the break between judging sessions take?
"judging_teamgrace": 600 # secs, how long before or after judging should a team be excluded from matches?
}

#Setup db connection
conn = sql.connect(teams_db)
cur = conn.cursor()

#Generate team objects
teams = {}
teams_raw = cur.execute("SELECT team FROM master_teams ORDER BY team ASC").fetchall()
for teamrow in teams_raw:
    teams[teamrow[0]] = {"matches_played": 0, "last_match": 0, "blackout_start": None, "blackout_end": None}

#Create judging blocks
judging_blocks = {}
block_count = math.ceil(len(teams)/(config["judging_roomcount"]*3))
block_length = (config["judging_inlength"] + config["judging_outlength"]) * 3
for i in range(1, block_count+1):
    start_time = config["judging_start"] + (block_length * (i - 1))
    judging_blocks[i] = {"teams": [], "start_time": start_time}

#Assign judging blocks
block = 1
for teamnumber in teams.keys():
    judging_blocks[block]["teams"].append(teamnumber)
    teams[teamnumber]["blackout_start"] = judging_blocks[block]["start_time"] - config["judging_teamgrace"]
    teams[teamnumber]["blackout_end"] = judging_blocks[block]["start_time"] + (3 * (config["judging_inlength"] + config["judging_outlength"])) - config["judging_outlength"] + config["judging_teamgrace"]
    if len(judging_blocks[block]["teams"]) >= config["judging_roomcount"]*3:
        block += 1

#Create judging sessions
judging_sessions = []
for blockdata in judging_blocks.values():
    while len(blockdata["teams"]) < config["judging_roomcount"] * 3:
        blockdata["teams"].append(-1)
    for shift in [0, 2, 1]:
        start_time = blockdata["start_time"] + (shift * (config["judging_inlength"] + config["judging_outlength"]))
        session = {"start_time": start_time, "end_time": start_time + config["judging_inlength"], "teams": []}
        for i in range(len(blockdata["teams"])):
            i_shifted = (i + (shift * config["judging_roomcount"])) % (config["judging_roomcount"] * 3)
            session["teams"].append(blockdata["teams"][i_shifted])
        judging_sessions.append(session)

#Print judging sessions
print("Judging sessions:")
[print(x) for x in judging_sessions]
