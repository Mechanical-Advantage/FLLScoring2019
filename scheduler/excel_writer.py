import xlsxwriter
from datetime import datetime

#Config
file_path = "schedule.xlsx"
table_names = ["Red 1", "Red 2", "Blue 1", "Blue 2", "Yellow 1", "Yellow 2"]
room_names = ["Robot 1", "Robot 2", "Project 1", "Project 2", "Core Values 1", "Core Values 2"]

def create(judging_sessions=None, judging_catcount=None, matches=[], team_schedules={}):
    #Initialization
    workbook = xlsxwriter.Workbook(file_path)
    formats = {}
    
    #Add formats
    formats["matches_title"] = workbook.add_format({"bold": True, "bg_color": "#00FF00"})
    formats["schedule_title"] = workbook.add_format({"bold": True, "bg_color": "#FFFF00"})
    formats["matches_headers"] = workbook.add_format({"align": "center", "bold": True, "top": True, "bottom": True})
    formats["matches_data"] = workbook.add_format({"align": "center"})
    formats["judging_title"] = workbook.add_format({"bold": True, "bg_color": "#00FFFF"})
    formats["judging_headers"] = workbook.add_format({"align": "center", "valign": "vcenter", "bold": True, "top": True, "text_wrap": True})
    formats["judging_data"] = workbook.add_format({"align": "center"})
    formats["judging_sectionstart"] = workbook.add_format({"align": "center", "top": True})
    
    #Create match overview setup
    matches_sheet = workbook.add_worksheet("Match Schedule")
    matches_sheet.set_column(0, 1, 12)
    matches_sheet.set_column(2, len(table_names) + 1, 8)
    matches_sheet.merge_range(0, 0, 0, len(table_names) + 1, "OFFICIAL ROBOT ROUNDS SCHEDULE", formats["matches_title"])
    matches_sheet.write(1, 0, "Match Number", formats["matches_headers"])
    matches_sheet.write(1, 1, "Time", formats["matches_headers"])
    for i in range(len(table_names)):
        matches_sheet.write(1, i + 2, table_names[i], formats["matches_headers"])
    
    #Fill in match data
    match_number = 0
    for match in matches:
        match_number += 1
        matches_sheet.write(match_number + 1, 0, match_number, formats["matches_data"])
        matches_sheet.write(match_number + 1, 1, datetime.fromtimestamp(match["start_time"]).strftime("%I:%M") + "-" + datetime.fromtimestamp(match["end_time"]).strftime("%I:%M"), formats["matches_data"])
        table = -1
        for team in match["teams"]:
            table += 1
            if team == -1:
                to_write = ""
            else:
                to_write = team
            matches_sheet.write(match_number + 1, table + 2, to_write, formats["matches_data"])

    if judging_sessions != None:
        #Create judging overview setup
        judging_sheet = workbook.add_worksheet("Judging Schedule")
        judging_sheet.set_column(0, 0, 12)
        judging_sheet.set_column(1, len(table_names), 8)
        judging_sheet.merge_range(0, 0, 0, len(room_names), "JUDGING SESSION SCHEDULE", formats["judging_title"])
        judging_sheet.write(1, 0, "Time", formats["judging_headers"])
        for i in range(len(room_names)):
            judging_sheet.write(1, i + 1, room_names[i], formats["judging_headers"])

        #Fill in judging data
        i = -1
        for session in judging_sessions:
            i += 1
            if judging_catcount == None or judging_catcount == 1:
                format = formats["judging_data"]
            else:
                if i % judging_catcount == 0:
                    format = formats["judging_sectionstart"]
                else:
                    format = formats["judging_data"]
            judging_sheet.write(i + 2, 0, datetime.fromtimestamp(session["start_time"]).strftime("%I:%M") + "-" + datetime.fromtimestamp(session["end_time"]).strftime("%I:%M"), format)
            room = -1
            for team in session["teams"]:
                room += 1
                if team == -1:
                    to_write = ""
                else:
                    to_write = team
                judging_sheet.write(i + 2, room + 1, to_write, format)

    #Creates spreadsheets for each team's schedules
    for team, schedule in team_schedules.items():
        team_sheet = workbook.add_worksheet("Team " + str(team) + " Schedule")
        team_sheet.set_column(0,2,18)
        team_sheet.merge_range(0, 0, 0, 2, "TEAM " + str(team) + " SCHEDULE", formats["schedule_title"])
        team_sheet.write(1, 0, "Time", formats["matches_headers"])
        team_sheet.write(1, 1, "Activity", formats["matches_headers"])
        team_sheet.write(1, 2, "Location", formats["matches_headers"])

        row = 2
        for i in schedule:
            team_sheet.write(row, 0, datetime.fromtimestamp(i["start_time"]).strftime("%I:%M") + "-" + datetime.fromtimestamp(i["end_time"]).strftime("%I:%M"), formats["matches_data"])
            team_sheet.write(row, 1, i["title"], formats["matches_data"])
            team_sheet.write(row, 2, i["location"], formats["matches_data"])
            row = row+1
    
    #Close workbook
    workbook.close()
