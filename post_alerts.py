import requests
import os
import json

grafana_url=os.environ['GRAFANA_URL']
token = os.environ['GRAFANA_TOKEN']
data_source = os.environ['GRAFANA_DATASOURCE_ID']

base_url = f"{grafana_url}/api/ruler/grafana/api/v1/rules/"


with open('alerts.json', 'r') as file:
    data = file.read()

headers = {'Authorization': f"Bearer {token}",
           'Content-type': 'application/json'}


# temp
json_data = json.loads(data)

#create folder


for folder_name in json_data.keys():
    folder = str(folder_name)
    new_folder_name = f'{{"title":"{folder}"}}'
    res = requests.post(f"{grafana_url}/api/folders",headers=headers,data=new_folder_name,timeout=3)
    print(res.content)
    print("removing existing alerts in folder: "+folder)
    res = requests.delete(base_url+folder, headers=headers, timeout=2)
    if res.status_code == 200:
        print("current rules deleted")
    else:
        print('Failed to delete alerts in folder: '+folder)
    rule_groups = json_data[folder]
    for rule_group in rule_groups:
        for idx, _ in enumerate(rule_group['rules']):
            del rule_group['rules'][idx]['grafana_alert']['uid']
            rule_group['rules'][idx]['grafana_alert']['data'][0]['datasourceUid'] = data_source
        # some logging
        num_of_rules = len(rule_group['rules'])
        print(
            f"inserting rule group: {rule_group['name']}, group consists of {num_of_rules} rules")

        data = json.dumps(rule_group)
        res = requests.post(base_url+folder_name,
                            headers=headers, data=data, timeout=2)
        res_msg = json.loads(res.content)['message']
        print(res_msg)
