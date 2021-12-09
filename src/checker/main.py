import math
import time
from typing import List
import os

from log_setup import logger
from huge_dict import huge_dict


def report_free(domain: str, price: int):
    print(f"{domain}, {price}€")
    with open("free.txt", "a+") as f:
        f.write(f"{domain}; {price}\n")


def main(name, only_buyable=True, price_below=20):
    to_request = huge_dict

    for entry in huge_dict:
        if only_buyable and not entry.get("price", False):
            to_request.remove(entry)
            continue

        if price_below and not entry.get("price", math.inf) < price_below:
            to_request.remove(entry)
            continue

    for entry in to_request:
        domain = entry["tld"]
        price = entry.get('price', None)

        domain_name = f"{name}.{domain}"
        logger.debug(f"Trying {domain_name}")
        ret: str = os.popen(f"whois {domain_name}").read()

        if "available" in ret.lower() and "not available" not in ret.lower():
            logger.info(f"FOUND FREE: {domain_name} for price: {price}")
            report_free(domain_name, price)

        time.sleep(0.2)

