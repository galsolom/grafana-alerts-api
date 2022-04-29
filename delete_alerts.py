import requests
import os
token = os.environ['GRAFANA_TOKEN']
grafana_url = os.environ['GRAFANA_URL']
headers = {'Authorization': f"Bearer {token}",
           'Content-type': 'application/json'}
base_url = f"{grafana_url}/api/ruler/grafana/api/v1/rules/"
res = requests.delete(base_url+'managed-alerts', headers=headers, timeout=3)
print(res.content)
