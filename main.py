from bs4 import BeautifulSoup
from html2image import Html2Image
import re

hti = Html2Image(size = (750, 930))


dir = input('Enter the file path to your html discord file (Ex: "F:\folder\file.html") whitout the quotation mark : ')

def extract_data(file_path):
    users = {}
    with open(file_path, 'r', encoding="utf-8") as file:
        contents = file.read()
    soup = BeautifulSoup(contents, 'html.parser')
    message_containers = soup.find_all('div', class_='chatlog__message-container')

    for container in message_containers:
        if container.find('img', class_='chatlog__avatar'):
            img_element = container.find('img', class_='chatlog__avatar')
            profile_picture_url = img_element['src']

            span_element = container.find('span', class_='chatlog__author')
            name = span_element.text
          
            if name in users:
                users[name]['message_count'] += 1
            else:
                users[name] = {'profile_picture_url': profile_picture_url, 'message_count': 1, 'calls': []}
            if users[name]['profile_picture_url'] == None:
                users[name]['profile_picture_url'] = profile_picture_url

        elif container.find('span', class_='chatlog__system-notification-author'):
            span_element = container.find('span', class_='chatlog__system-notification-author')
            name = span_element.text

            content_element = container.find('span', class_='chatlog__system-notification-content')
            duration_match = re.search(r'(\d+[.,]\d+) minutes', content_element.text)
            if duration_match:
                duration = duration_match.group(1)
                duration = str(duration).replace(',', '.')
                duration = float(duration)
                if name in users:
                    users[name]['calls'].append(float(duration))
                else:
                    users[name] = {'profile_picture_url': None, 'message_count': 0, 'calls': [float(duration)]}
    return users





def convert_time(minutes):
    days = minutes // (24 * 60)
    hours = (minutes % (24 * 60)) // 60
    minutes = minutes % 60

    time_units = [0, 0 , 0]
    if days > 0:
        time_units[0]= int(days)
    if hours > 0:
        time_units[1]= int(hours)
    if minutes > 0:
        time_units[2] = int(minutes)

    return time_units
    

def generate_card(data, time):
    template = f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet"></head><body style="margin: 0; padding: 0;"><p style="color:#dbdbdb;z-index:3;text-align:center;font-family:Inter;font-size:12px;font-style:normal;font-weight:400;line-height:normal;margin-left:245px;position:absolute;margin-top:910px">Generated with Discord Call Calculator by Ousli</p><div style="width:750px;height:930px;border-radius:60px;background-color:#3d3d3d;position:absolute"><h1 style="color:#fff;text-align:center;font-family:Inter;font-size:48px;font-style:normal;font-weight:400;line-height:normal;position:absolute;margin-left:57px;margin-top:66px">Discord<br>Call<br>Calculator</h1><img src="{data[0][1]}" style="width:100px;height:100px;position:absolute;margin-left:82px;margin-top:297px"> <img src="{data[1][1]}" style="width:100px;height:100px;position:absolute;margin-left:219px;margin-top:297px"><div style="width:750px;background-color:#888;height:4px;position:absolute;margin-top:62%"></div><div style="width:4px;background-color:#888;height:465px;position:absolute;margin-left:50%"></div><div style="position:absolute;margin-left:418px;margin-top:51px"><h1 style="color:#acabab;text-align:left;font-family:Inter;font-size:40px;font-style:normal;font-weight:400;line-height:normal">{data[0][0]} :</h1><h1 style="color:#acabab;text-align:left;font-family:Inter;font-size:40px;font-style:normal;font-weight:400;line-height:normal">Started <span style="color:#64b4d2">{data[0][2]}</span> Call</h1></div><div style="position:absolute;margin-left:418px;margin-top:233px"><h1 style="color:#acabab;text-align:left;font-family:Inter;font-size:40px;font-style:normal;font-weight:400;line-height:normal">{data[1][0]} :</h1><h1 style="color:#acabab;text-align:left;font-family:Inter;font-size:40px;font-style:normal;font-weight:400;line-height:normal">Started <span style="color:#64b4d2">{data[1][2]}</span> Call</h1></div><h1 style="color:#64b4d2;text-align:center;font-family:Inter;font-size:64px;font-style:normal;font-weight:400;line-height:normal;position:absolute;margin-top:497px;margin-left:282px">Total :</h1><div style="display:flex;position:static;flex-direction:row;margin-top:607px;justify-content:space-around"><div style="display:flex;flex-direction:column;align-items:center"><h3 style="color:#acabab;font-family:Inter;font-size:40px;font-style:normal;font-weight:400;line-height:normal;display:block">Day(s)</h3><h1 style="color:#64b4d2;text-align:center;font-family:Inter;font-size:64px;font-style:normal;font-weight:400;line-height:normal;display:block">{time[0]}</h1></div><div style="display:flex;flex-direction:column;align-items:center"><h3 style="color:#acabab;font-family:Inter;font-size:40px;font-style:normal;font-weight:400;line-height:normal;display:block">Hour(s)</h3><h1 style="color:#64b4d2;text-align:center;font-family:Inter;font-size:64px;font-style:normal;font-weight:400;line-height:normal;display:block">{time[1]}</h1></div><div style="display:flex;flex-direction:column;align-items:center"><h3 style="color:#acabab;font-family:Inter;font-size:40px;font-style:normal;font-weight:400;line-height:normal;display:block">Minute(s)</h3><h1 style="color:#64b4d2;text-align:center;font-family:Inter;font-size:64px;font-style:normal;font-weight:400;line-height:normal;display:block">{time[2]}</h1></div></div><div style="display:flex;position:static;height:77px;justify-content:space-around"></div></div></body></html>'
    hti.screenshot(html_str=template, save_as='export.png')

data = extract_data(dir)
total_time = 0
card_data = []

for user, details in data.items():
    card_data.append((user, details['profile_picture_url'], len(details.get('calls', [])), sum(details.get('calls', []))))
    total_time += sum(details.get('calls', []))

generate_card(card_data, convert_time(total_time))