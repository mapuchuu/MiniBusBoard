import json
import sys
import requests
import pandas as pd
import datetime
import time

sys.path.append('/opt/site-packages')
AKEY = #get an API key from OneBusAway Developer developer

def busCall(stop_id):
    url = f'https://api.pugetsound.onebusaway.org/api/where/arrivals-and-departures-for-stop/1_{stop_id}.json?key={AKEY}' # you can change the prefix number to switch agencies
    response = requests.get(url, timeout = 10)

    if response.status_code == 200:
        try:
            data = response.json()

            if 'data' in data and 'entry' in data['data'] and 'arrivalsAndDepartures' in data['data']['entry']:
                arrivals_departures = data['data']['entry']['arrivalsAndDepartures']
                df = pd.DataFrame(arrivals_departures)
                df = df[(df["numberOfStopsAway"] >= 0) & (df["lastUpdateTime"] != 0)]
                df = df.sort_values('predictedDepartureTime')
                dfm = df[['numberOfStopsAway', 'predictedArrivalTime', 'routeShortName', 'tripHeadsign']]
                dfm = dfm.sort_values('predictedArrivalTime')
                dfm = dfm.copy()
                dfm.loc[:, 'humanTime'] = dfm['predictedArrivalTime'].apply(
                    lambda x: datetime.datetime.utcfromtimestamp((x / 1000) - 25200).strftime('%Y-%m-%d %H:%M:%S')
                )

                current_time_ms = int(time.time() * 1000)
                dfm['minutesAway'] = ((dfm['predictedArrivalTime'] - current_time_ms) / (1000 * 60)).round(1)
                formatted_buses = []
                for _, row in dfm.iterrows():
                    bus_number = str(row['routeShortName']).strip()[:4] 
                    minutes_remaining = int(row['minutesAway'])
                    stops_remaining = row['numberOfStopsAway']
                    bus_number = bus_number.ljust(4)
                    time_str = f"{minutes_remaining}m".rjust(4)
                    stops_str = f"{stops_remaining}stps".rjust(6)
                    formatted_entry = f"{bus_number}{time_str} {stops_str}"
                    formatted_buses.append(formatted_entry)

                return formatted_buses
            else:
                print("Error: valid Stop, but no registered buses incoming.")
        except ValueError:
            print("Error: Unable to parse the response JSON.")
    else:
        print(f"Error: Stop not found. Please enter a valid Stop ID")


def lambda_handler(event, context):
    stop_id = event.get('id', 'No ID provided')
    data = busCall(stop_id)

    if data:
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Failed to retrieve data for {stop_id}')
        }
