import re

dir = input('Enter the file path to your html discord file (Ex: "F:\folder\file.html") whitout the quotation mark : ')

def find_call_duration(file_path):
    total_min = 0
    with open(file_path, 'r', encoding="utf-8") as file:
        contents = file.read()
        call_text = re.findall(r'started a call that lasted (\d+\.\d+) minutes', contents)
        for e in call_text:
            total_min += float(e)
        return total_min
        


def convert_time(minutes):
    days = minutes // (24 * 60)
    hours = (minutes % (24 * 60)) // 60
    minutes = minutes % 60

    time_units = []
    if days > 0:
        time_units.append(f"{days} day(s)")
    if hours > 0:
        time_units.append(f"{hours} hour(s)")
    if minutes > 0:
        time_units.append(f"{int(minutes)} minute(s)")

    if len(time_units) == 0:
        return "0 minutes"
    elif len(time_units) == 1:
        return time_units[0]
    else:
        return ", ".join(time_units[:-1]) + " and " + time_units[-1]
    

duration = find_call_duration(dir)
print(f"You spend a total of {convert_time(duration)} on call with this person")

