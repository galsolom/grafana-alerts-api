import requests
import os
import json
import datetime
token = os.environ['GRAFANA_TOKEN']
grafana_url = os.environ['GRAFANA_URL']
headers = {'Authorization': f"Bearer {token}",
           'Content-type': 'application/json'}
base_url = f"{grafana_url}/api/ruler/grafana/api/v1/rules/"

res = requests.get(base_url, headers=headers, timeout=3)
date = datetime.datetime.now().timestamp()

with open('alerts'+str(date)+'.json', 'wb') as file:
    file.write(res.content)
