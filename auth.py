#!/usr/bin/env python3

import os
import yandex
import dns_check

if __name__ == "__main__":
    domain = os.environ.get("CERTBOT_DOMAIN", "")
    txt = os.environ.get("CERTBOT_VALIDATION", "")

    if domain != "" and txt != "":
        yandex.add_record(domain, txt)
        dns_check.wait_dns_update(domain, txt)
exit(1)
