from datetime import datetime
START_LINE = ["Izaro: Ascend with precision.",
"Izaro: The Goddess is watching.",
"Izaro: Justice will prevail."]
FINISH_LINE = ["Izaro: Triumphant at last!", 
"Izaro: You are free!",
"Izaro: I die for the Empire!",
"Izaro: The trap of tyranny is inescapable.",
"Izaro: Delight in your gilded dungeon, ascendant.",
"Izaro: Your destination is more dangerous than the journey, ascendant."]
SECTION_END_LINE = ["Izaro: By the Goddess! What ambition!",
  "Izaro: Such resilience!",
  "Izaro: You are inexhaustible!",
  "Izaro: You were born for this!"]
DEATH_LINE = ["Izaro: Apparently, this is the ending that you deserve.",
"Izaro: For those who ascend too quickly, the fall is inevitable.",
"Izaro: Justice is served."]
lab_run_list =[]

def process_log(client_log):

    start_list = []
    finish_list = []
    section_end_list = []
    death_list = []
    today_log = []
    index = 0

    current_date = datetime.now().date().strftime("%Y/%m/%d") #Year/Month/Date
    log_data = client_log.splitlines()

    for x in log_data:                  #Find the logs specific to today's date and store in new list
        if x.find(current_date) != -1:
            today_log.append(x)
    log_data.clear()

    for x in today_log:
        for lines in START_LINE:
            if x.find(lines) != -1: #If any lines in START_LINE is found in x
                start_list.append(x)
        for lines in FINISH_LINE:
            if x.find(lines) != -1:
                finish_list.append(x)
        for lines in SECTION_END_LINE:
            if x.find(lines) != -1:
                section_end_list.append(x)
        for lines in DEATH_LINE:
            if x.find(lines) != -1:
                death_list.append(x)

    combined_list = sorted(death_list+section_end_list+finish_list+start_list)
    for x in combined_list:
        for lines in START_LINE:
            if x.find(lines) != -1: #If combined list does not have any lines from START LINE
                start_time = datetime.strptime(combined_list[combined_list.index(x)][0:19], "%Y/%m/%d %H:%M:%S")
                section = 1
                break
        for lines in SECTION_END_LINE:
            if x.find(lines) != -1:
                section += 1
                break
        for lines in FINISH_LINE:
            if x.find(lines) != -1 and section == 3: #Make sure we are at the last aspirant trial
                end_time = datetime.strptime(combined_list[combined_list.index(x)][0:19], "%Y/%m/%d %H:%M:%S")
                difference = end_time - start_time
                lab_run_list.append(difference.seconds)
                index += 1
                break
        for lines in DEATH_LINE:
            if x.find(lines) != -1:
                index += 1
                break
    lab_run_list.sort()
    return lab_run_list[0]

