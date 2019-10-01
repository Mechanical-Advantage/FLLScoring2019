import xlsxwriter
from datetime import datetime

#Config
file_path = "schedule.xlsx"
table_names = ["Red 1", "Red 2", "Blue 1", "Blue 2", "Yellow 1", "Yellow 2"]
room_names = ["Robot 1", "Robot 2", "Project 1", "Project 2", "Core Values 1", "Core Values 2"]

def create(judging_sessions=[], matches=[]):
    #Initialization
    workbook = xlsxwriter.Workbook(file_path)
    formats = {}
    
    #Add formats
    formats["matches_title"] = workbook.add_format({"bold": True, "bg_color": "#00FF00"})
    formats["matches_headers"] = workbook.add_format({"align": "center", "bold": True, "top": True, "bottom": True})
    formats["matches_data"] = workbook.add_format({"align": "center"})
    
    #Create match overview setup
    matches_sheet = workbook.add_worksheet()
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
        matches_sheet.write(match_number + 1, 1, datetime.fromtimestamp(match["start_time"]).strftime("%-I:%M") + "-" + datetime.fromtimestamp(match["end_time"]).strftime("%-I:%M"), formats["matches_data"])
        table = -1
        for team in match["teams"]:
            table += 1
            if team == -1:
                to_write = ""
            else:
                to_write = team
            matches_sheet.write(match_number + 1, table + 2, to_write, formats["matches_data"])

    #Close workbook
    workbook.close()
