#!/usr/bin/env python3

import dns.resolver
from time import sleep


def wait_dns_update(d_name: str, text: str, sub: str = "_acme-challenge", interval: int = 60):
    sleep(interval)
    for x in range(100):
        if check_record(d_name, text, sub):
            sleep(interval)
            exit(0)
        else:
            sleep(interval)


def check_record(d_name: str, text: str, sub: str = "_acme-challenge"):
    try:
        answers = dns.resolver.query(sub + '.' + d_name, 'TXT')
        print(' query qname:', answers.qname, ' num ans.', len(answers))
        for rdata in answers:
            for txt_string in rdata.strings:
                if txt_string.decode("utf-8") == text:
                    return True
                else:
                    return False
    except dns.resolver.NXDOMAIN:
        print("Couldn't find any records (NXDOMAIN)")
        return False
    except dns.resolver.NoAnswer:
        print("Couldn't find any records (NoAnswer)")
        return False
