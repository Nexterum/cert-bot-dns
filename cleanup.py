#!/usr/bin/env python3

import os
import yandex

if __name__ == "__main__":
    domain = os.environ.get("CERTBOT_DOMAIN", "")
    txt = os.environ.get("CERTBOT_VALIDATION", "")
    if domain != "":
        yandex.remove_all_acme(domain)
        exit(0)
