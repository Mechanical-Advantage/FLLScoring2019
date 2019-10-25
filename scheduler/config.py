# File paths
teams_db = "../teams.db"
excel_path = "schedule.xlsx"

# Names lists
tables_long = ["Red 1", "Red 2", "Blue 1", "Blue 2"] # for match overview
tables_short = ["R1", "R2", "B1", "B2"] # for team schedules
judging_rooms = ["Room 108"] # for judging overview
judging_catnames = ["Core Values"] # for team schedules

# General config
enable_judging = True
general = {
"match_tablepaircount": 2, # how many pairs of tables are available for matches?
"match_countperteam": 5, # how many matches should each team play?
"match_starttime": 1572199200, # unix time, when does the first match begin?
"match_cycletime": 480, # secs, how long between the start of each match?
"match_breakfrequency": 30, # how many matches should be played between each break?
"match_breaklength": 0, # how many matches should each break last?
"match_endjointhreshold": 1, # how few matches are required to join the final two sections?
"match_teamgrace": 1, # how many match cycles must separate two matches with the same team?
"judging_roomcount": 1, # how many rooms are available FOR EACH CATEGORY?
"judging_catcount": 1, # how many judging categories?
"judging_start": 1572199200, # unix time, when does the first judging session begin?
"judging_inlength": 600, # secs, how long does each judging session take?
"judging_outlength": 300, # secs, how long should the break between judging sessions take?
"judging_teamgrace": 600 # secs, how long before or after judging should a team be excluded from matches?
}

# Debug
print_output = False
team_schedule_tester = False
create_excel = True
