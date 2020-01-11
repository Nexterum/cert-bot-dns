#!/usr/bin/env python3

import requests
import json

domain = "sonys.ru"
txt = "тестовая запись для домена"
sub = "_acme-challenge"
api_url = "https://pddimp.yandex.ru"
ttl = 720


tokens = {"sonys.ru":         "3PVKNFY5K5PHNAOA5HAVJW7FJHQTIZRZPIS7AKLG6JGRC3IJ3Z4Q",
          "photos-nature.ru": "OFNTRRVATECMCXPV6F7TUCJP4LAONZREZ4EUGJSRDALAMWNZPQBQ"}


def add_record(d_name: str, text: str):
    pddtoken = tokens.get(d_name, "")
    if pddtoken == "":
        return False
    headers = {
        'PddToken': pddtoken,
        'Content-Type': 'application/json'
    }
    params = {
        'domain': d_name,
        'type': 'TXT',
        'content': text,
        'subdomain': sub,
        'ttl': ttl
    }
    url = "https://pddimp.yandex.ru/api2/admin/dns/add"
    response = requests.post(url, headers=headers, params=params)
    print(response)


def get_all_records(d_name: str):
    pddtoken = tokens.get(d_name, "")
    if pddtoken == "":
        return False
    headers = {
        'PddToken': pddtoken,
        'Content-Type': 'application/json'
    }
    params = {
        'domain': d_name
    }
    url = "https://pddimp.yandex.ru/api2/admin/dns/list"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        result = json.loads(response.content).get('records')
    else:
        result = False
    return result


def delete_record(d_name: str, r_id: int):
    url = "https://pddimp.yandex.ru/api2/admin/dns/del"
    pddtoken = tokens.get(d_name, "")
    if pddtoken == "":
        return False
    headers = {
        'PddToken': pddtoken,
        'Content-Type': 'application/json'
    }
    params = {
        'domain': d_name,
        'record_id': r_id
    }
    response = requests.post(url, headers=headers, params=params)
    if response.status_code == 200 and response:
        if json.loads(response.content).get('success') == 'ok':
            return True
        else:
            return json.loads(response.content)
    return False


def remove_all_acme(d_name: str):
    records = get_all_records(d_name)
    count = 0
    if type(records) == list:
        for r in records:
            if (r.get('type', "") == 'TXT') and (r.get('subdomain') == sub):
                record_id = int(r.get('record_id', 0))
                print("Удаление записи № " + str(record_id))
                if delete_record(d_name, record_id):
                    print('Запись удалена!')
                    count += 1
    return count


if __name__ == "__main__":
    exit(0)
