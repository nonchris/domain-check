import math
import time
import os
from typing import Union

from .log_setup import logger
from .huge_dict import huge_dict


def report_free(domain: str, price: Union[int, float], file_path="free.txt"):
    """
    Print free domains on terminal and append domain to file
    The file will have csv format 'domain; price'
    :param domain: Free domain name like example.net
    :param price: Price of domain
    :param file_path: Name of file to report to
    """
    print(f"{domain}, {price}€")
    with open(file_path, "a+") as f:
        f.write(f"{domain}; {price}\n")


# travelersinsurance is the longest upcoming toplevel domain with 18 chars, lol
def main(name, only_buyable=True, price_below=20000, max_len=18, request_delay=0.2, file_path="free.txt"):
    """
    Main routine for checking availability
    Using a subprocess to access the 'nslookup' cli command
    :param name: domain name to check for
    :param only_buyable: ignore domains that are not buyable yet
    :param price_below: max price for the domain (on checkdomain.net)
    :param max_len: max length the domain should have
    :param request_delay: delay between whois-requests
    :param file_path: Name of file to report to
    """

    to_request = huge_dict

    # remove entries that don't match criteria
    for entry in huge_dict:
        if only_buyable and not entry.get("price", False):
            to_request.remove(entry)
            continue

        if price_below and not entry.get("price", math.inf) < price_below:
            to_request.remove(entry)
            continue

        if max_len < len(entry["tld"]):
            to_request.remove(entry)
            continue

    # cycle trough domains that are left and check if available
    for entry in to_request:
        domain = entry["tld"]
        price = entry.get('price', None)

        domain_name = f"{name}.{domain}"

        logger.debug(f"Trying {domain_name}")
        ret: str = os.popen(f"dig {domain_name} SOA").read()

        # to blacklist clauses (whoami):
        # abogado: "is 'available',"
        # be: "still available", "made available to", "not available"
        # info: "available due", "available through"
        # io: "available due"
        # io: "available through"
        # net: "available by"
        if f"AUTHORITY SECTION" in ret:
            logger.info(f"FOUND FREE: {domain_name} for price: {price}")
            report_free(domain_name, price, file_path=file_path)

        time.sleep(request_delay)

