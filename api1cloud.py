#!/usr/bin/env python3

import requests
import json

headers = {
    'Authorization': 'Bearer 2a50a831e55d096d0cc27a2874a8acfcc7ae5d8b1b368265841582c2163f841b',
    'Content-Type': 'application/json'
}

domain = "photos-nature.ru"
txt = "тестовая запись для домена"
api_url = "https://api.1cloud.ru/dns"
ttl = 720


def id_by_domain(d_name: str):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        content = json.loads(response.content)
        for dom in content:
            if dom['Name'] == d_name:
                return dom["ID"]
        return False


def add_record(dom: str, text: str, sub: str = "_acme-challenge"):
    d_id = id_by_domain(dom)
    data = {
        'DomainId': d_id,
        'TTL': "720",
        'Text': text,
        'Name': sub
    }
    if d_id:
        response = requests.post(api_url + "/recordtxt", data=str(data), headers=headers)
        print(response.content)
        if response.status_code == 200:
            content = json.loads(response.content)
            return content["ID"]
    return False


def delete_record(domain_id: int, record_id: int):
    response = requests.delete(api_url + "/" + str(domain_id) + "/" + str(record_id), headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False


def remove_all_acme(d_name: str, sub: str = "_acme-challenge"):
    count = 0
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        content = json.loads(response.content)
        for dom in content:
            print(dom)
            if dom['Name'] == d_name:
                for rec in dom['LinkedRecords']:
                    if rec['TypeRecord'] == 'TXT' and rec['HostName'] == sub + '.' + d_name + '.':
                        count += 1
                        delete_record(dom['ID'], rec['ID'])
    else:
        count = -1
    return count


if __name__ == "__main__":
    print(remove_all_acme(domain))
    exit(0)
