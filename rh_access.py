#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, argparse
from argparse import RawTextHelpFormatter
from timeit import default_timer as timer
import json
import requests

from datetime import date
from datetime import datetime, timedelta
from collections import Counter
from colorama import init, Fore, Back, Style

import pyfiglet
from concurrent.futures import ThreadPoolExecutor as PoolExecutor


appname='RH-Access'
description = f'https://access.redhat.com/security/data/metrics/cve_dates.txt'
banner = f"""
   Zzzzz   |\      _,,,---,,_
           /,`.-'`'    -.  ;-;;,_   __author__ : [ zd ]
          |,4-  ) )-,_..;\ (  `'-'  __year__   : [ 2022.07 ]
         '---''(_/--'  `-'\_)       __file__   : [ {__file__} ]

         [ {description} ]
    """

notes="""
"""

url_1 = 'https://access.redhat.com/security/data/metrics/cve_dates.txt'
verberos = False
count = 0
w = 5

def cr(x): return (f'{Style.BRIGHT}{Fore.RED}{x}{Style.RESET_ALL}')
def cg(x): return (f'{Style.BRIGHT}{Fore.GREEN}{x}{Style.RESET_ALL}')
def cy(x): return (f'{Style.BRIGHT}{Fore.YELLOW}{x}{Style.RESET_ALL}')
def sd(x): return (f'{Style.DIM}{x}{Style.RESET_ALL}')

def c10(x): return (sd(x) if type(x) == str else cr(x) if x >= 8 else cg(x) if x <= 3 else cy(x) )

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

      
def curl(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Fail for : ", url, e)

    return(response.text)


def main():
    """ main() function """
    g = globals()

    parser = argparse.ArgumentParser(description=banner, formatter_class=RawTextHelpFormatter, epilog=notes)

    parser.add_argument('-e', dest='cve', metavar='<cve>', nargs='+', help='Specify a CVE or a list of CVEs.')
    parser.add_argument('-v', action='store_true', help='verbose output')

    args = parser.parse_args()
    g['verbose'] = True if args.v else False

    init(autoreset=True)
    print(f'')
    word = pyfiglet.figlet_format(appname, font="slant")
    print(Fore.BLUE + word)

    cve_str = curl(url_1)

    total = f'{len(cve_str):,}'
    print(f' [+] Downloaded  {cg(total)}  cves.')

    cve_list = cve_str.splitlines()
    total = f'{len(cve_list):,}'
    print(f' [+] Total : {cg(total)} CVEs FOUND. ')

    cve_dict = {}

    for line in cve_list:
        cve, detail = line.split()
        cve_dict[cve] =  {}
        info = {}
        items = detail.split(',')
        for item in items:
            hdr,content = item.split('=')
            info[hdr]=content
        cve_dict[cve] = info

    total = f'{len(cve_dict):,}'
    print(f' [+] Total : {cg(total)} CVEs Loaded. ')

    if args.cve:
        cve2 = []
        cves = args.cve

        for cve in cves :
            if not cve.upper().startswith('CVE-'):
                cve = 'CVE-' + cve
            cve2.append(cve.upper())

        #print(cve2)
        for cve in cve2:
            #ic(cve, cve_dict[cve])
            if not cve in cve_dict:
                print(f'')
                print(f' [*] {cve} [ not found ]')
                next
            else:
                info = cve_dict[cve]

                #print(f' [*] {cve} : {info["impact"]}/{info["public"]}')
                print(f'')
                print(f' [*] {cve}')
                print(f'           Severity : {info["impact"]}/{info["public"]}')
                if g['verbose']:
                    if "cvss2" in info:
                        cvss = info["cvss2"]
                    elif "cvss3" in info:
                        cvss = info["cvss3"]
                    else:
                        cvss = '-.-'
                    if cvss != '-.-':
                        base,vector = cvss.split('/',1)
                    else:
                        base,vector = [ '-.-' , ' - N/A - ' ]

                    if isfloat(base):
                        base = float(base)

                    print(f'             Source : {info["source"]}/{info["reported"]}')
                    print(f'               CVSS : Base:{c10(base)}\t\tV:{vector}')
                    print(f'               Link : https://access.redhat.com/security/cve/{cve}')


    return

if __name__ == "__main__":

    if sys.version_info.major == 2:
        print('This script needs Python 3.')
        exit()
    else:
        print(f'')

    start = timer()
    main()
    end = timer()

    print(f'')
    print(f'\n [{date.today()}] Completed within [{end-start:.2f} sec].\n')
    
    
    
