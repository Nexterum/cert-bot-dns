#!/usr/bin/env python3

import os
import api1cloud

if __name__ == "__main__":
    domain = os.environ.get("CERTBOT_DOMAIN", "")
    txt = os.environ.get("CERTBOT_VALIDATION", "")
    if domain != "":
        api1cloud.remove_all_acme(domain)
        exit(0)
