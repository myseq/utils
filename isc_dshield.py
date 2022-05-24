#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, argparse, os
from argparse import RawTextHelpFormatter
from timeit import default_timer as timer
import json
import requests

from datetime import date
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style

import pyfiglet
from icecream import ic

description = f'''  Internet Storm Center / DShield API access  '''
banner = f"""
   Zzzzz   |\      _,,,---,,_
           /,`.-'`'    -.  ;-;;,_   __author__ : [ zd ]
          |,4-  ) )-,_..;\ (  `'-'  __year__   : [ 2022.05 ]
         '---''(_/--'  `-'\_)       __file__   : [ {__file__} ]

         [ {description} ]
    """

notes="""

    Internet Storm Center / DShield API
    @ https://isc.sans.edu/api/

    - url_handler = 'https://isc.sans.edu/api/handler'
    - url_infocon = 'https://isc.sans.edu/api/infocon'
    - url_getmspatch = 'https://isc.sans.edu/api/getmspatch/'
    - url_getmspcves = 'https://isc.sans.edu/api/getmspatchcves/'
    - url_getmspreplaces = 'https://isc.sans.edu/api/getmspatchreplaces/'

"""

identifier = 'zd2600@gmail.com'
url_handler = 'https://isc.sans.edu/api/handler'
url_infocon = 'https://isc.sans.edu/api/infocon'
url_getmspatch = 'https://isc.sans.edu/api/getmspatch/'
url_getmspcves = 'https://isc.sans.edu/api/getmspatchcves/'
url_getmspreplaces = 'https://isc.sans.edu/api/getmspatchreplaces/'

verberos = False
count = 0

def cr(x): return (f'{Fore.RED}{x}{Style.RESET_ALL}')
def cg(x): return (f'{Fore.GREEN}{x}{Style.RESET_ALL}')
def cy(x): return (f'{Fore.YELLOW}{x}{Style.RESET_ALL}')
def cc(x): return (f'{Fore.CYAN}{x}{Style.RESET_ALL}')

def hl(stat):

    if stat == "green":
        return cg(stat)
    elif stat == "yellow":
        return cy(stat)
    elif stat == "red":
        return cr(stat)
    else:
        return cc(stat)

def curl(url):
    hdrs = {'content-type': 'application/json', 'User-Agent': identifier}

    try:
        resp = requests.get(url, headers=hdrs)
    except requests.exceptions.RequestException as e:
        print('Fail for : ', url, e)

    return resp.json()


def Print_MS(msp, data):

    if data.get('getmspatch'):
        print(f'')
        d = data.get('getmspatch')
        print(f' [*] {msp} -- {d.get("title")}')
        print(f'     [-] Products : {d.get("affected")} / {d.get("severity")}')
        print(f'     [-] ID/KB    : {d.get("id")} / {d.get("kb")}')
        print(f'     [-] Exploits : {d.get("exploits")}')

    if data.get('getmspatchcves'):
        cves = data.get('getmspatchcves')
        cvelist = []
        for cve in cves:
            cve_exp = cve.get('cve') + '[' + str(cve.get('exploitability')) + ']'
            cvelist.append(cve_exp)
        cve_list = ', '.join(cvelist)
        print(f'     [-] CVEs     : {cve_list}')

    if data.get('getmspatchreplaces'):
        d = data.get('getmspatchreplaces')
        kb_list = ', '.join(d)
        print(f'     [-] KB       : {kb_list}')


def main():
    """ main() function """
    g = globals()

    parser = argparse.ArgumentParser(description=banner, formatter_class=RawTextHelpFormatter, epilog=notes)
    parser.add_argument('-m', dest='msp', metavar='<ms-patch>', nargs='+', help='Get MS patch (like MS17-010).')
    parser.add_argument('-v', action='count', default=0, help='verbose output')

    args = parser.parse_args()
    g['verbose'] = True if args.v else False

    init(autoreset=True)
    print(f'')
    word = pyfiglet.figlet_format("ISC.DShield", font="slant")
    print(Fore.BLUE + word)

    link = url_handler + '?json'
    d_handler = curl(link)
    #ic(d_handler, link)

    link = url_infocon + '?json'
    d_infocon = curl(link)
    #ic(d_infocon, link)

    print(f'')
    print(f'ISC InfoCon/Handler : {hl(d_infocon.get("status"))} / {hl(d_handler.get("name"))} [ {date.today()} ]')

    if args.msp:
        for msp in args.msp:
            link = url_getmspatch + msp + '?json'
            d_mspatch = curl(link)
            #ic(msp, d_mspatch)
            Print_MS(msp, d_mspatch)
            if g['verbose']:
                link = url_getmspcves + msp + '?json'
                d_mspcves = curl(link)
                #ic(msp, d_mspcves)
                Print_MS(msp, d_mspcves)
                link = url_getmspreplaces + msp + '?json'
                d_mspreplaces = curl(link)
                #ic(msp, d_mspreplaces)
                Print_MS(msp, d_mspreplaces)


    return

if __name__ == "__main__":

    if sys.version_info.major == 2:
        print(f'')
        print(' [!] This script needs Python 3.')
        print(f'')
        exit()

    start = timer()
    main()
    end = timer()

    print(f'')
    print(f'\n [{date.today()}] Completed within [{end-start:.2f} sec].\n')
