import os
import datetime

import requests


url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"
service_key = os.environ['service_key']     # "YOUR_SERVICE_KEY"

today = datetime.datetime.today()
date = today.strftime("%Y%m%d")
# date = "20200922"
time = "0200"

locations = [(73, 134), (55, 124), (102, 84), (60, 127), (62, 118), (67, 100), (61, 120), (62, 123), (90, 77)]
location_name = ["춘천", "인천", "울산", "서울", "오산", "대전", "수원", "분당", "창원"]

payload = f"serviceKey={service_key}&dataType=json&numOfRows=50&base_date={date}&base_time={time}"
# &numOfRows=40


def make_weather_data(data):
    result = f"강수확률 : {data['pop']}%, "
    if data['pty']:
        if data['pty'] == 1:
            result += '비, '
        elif data['pty'] == 2:
            result += '진눈개비, '
        elif data['pty'] == 3:
            result += '눈, '
        elif data['pty'] == 4:
            result += '소나기, '
        elif data['pty'] == 5:
            result += '빗방울, '
        elif data['pty'] == 6:
            result += '빗방울/눈날림, '
        elif data['pty'] == 7:
            result += '눈날림, '
    else:
        if data['sky'] == '1':
            result += '맑음, '
        elif data['sky'] == '3':
            result += '구름많음, '
        else:
            result += '흐림, '

    result += f"최저기온 : {data['tmn']}, 최고기온 : {data['tmx']}"

    return result

for location in range(len(locations)):
    location_xy = f"&nx={locations[location][0]}&ny={locations[location][1]}"
    res = requests.get(url+payload+location_xy)
    # print(res.json())
    # print(res.json().get('response').get('body').get('items'))
    items = res.json().get('response').get('body').get('items')['item']
    # print(items)
    data =dict()
    for item in items:
        if item['category'] == 'POP':
            data['pop'] = item['fcstValue']
        elif item['category'] == 'SKY':
            data['sky'] = item['fcstValue']
        elif item['category'] == 'TMN':
            data['tmn'] = item['fcstValue']
        elif item['category'] == 'TMX':
            data['tmx'] = item['fcstValue']
        elif item['category'] == 'PTY':
            data['pty'] = int(item['fcstValue'])
    # print(location_name[location], data)
    print(location_name[location], '|', make_weather_data(data))
