#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, argparse
from argparse import RawTextHelpFormatter
from timeit import default_timer as timer
#import json

from rich import print as rprint
import asyncio, httpx


base_url = 'https://access.redhat.com/hydra/rest/securitydata'

appname='RH-Access'
desc = f'https://docs.redhat.com/en/documentation/red_hat_security_data_api/1.0/html-single/red_hat_security_data_api/index'

banner = f"""
   Zzzzz   |\      _,,,---,,_
           /,`.-'`'    -.  ;-;;,_   __author__ : [ zd ]
          |,4-  ) )-,_..;\ (  `'-'  __year__   : [ 2024.09 ]
         '---''(_/--'  `-'\_)       __file__   : [ {__file__} ]

         Retrieve CVE details directly via RedHat Security Data API.

         [ {base_url = } ]
"""

note = f"""

    RedHat Security Data API:

        See {desc}

"""


#url_1 = 'https://access.redhat.com/security/data/metrics/cve_dates.txt'
verbose = False
#count = 0
#w = 5

def timeit(func):
    def timed(*args, **kwargs):
        stime = timer()
        result = func(*args, **kwargs)
        etime = timer()
        print(f'\n [*] {func.__name__}(): completed within [{etime-stime:.4f} sec].\n ')
        return result
    return timed

async def curl(client,link):
    global verbose

    try:
        resp = await client.get(link)
        resp.raise_for_status()
    except httpx.RequestError as err:
        if verbose:
            rprint(f' [!] [{err}] {link}')
    except httpx.HTTPStatusError as err:
        if verbose:
            rprint(f' [!] [{resp.status_code}] {link}')
    else:
        rprint(f' [+] [{resp.status_code}] {link}')
        return resp

async def fetching(links):
    hdrs = { 'accept': 'application/json', 'content-type': 'application/json' }
    print(f'')

    async with httpx.AsyncClient(headers=hdrs, http2=True) as client:
        tasks = [ curl(client,link) for link in links ]
        responses = await asyncio.gather(*tasks)

    print(f'')
    fail = 1 if any(r is None or r.status_code != 200 for r in responses) else 0

    if not fail:
        print(f' [*] All [{len(responses)} responses] are OK.')
    else:
        print(f' [!] Errors: Not all [{len(responses)} responses] are OK.')

    print(f'')
    resp = [ r for r in responses if r is not None and r.status_code == 200]
    rprint(f' [*] Successful fetched : {len(resp)}/{len(responses)}')
    return resp


def Showing(resp):
    global verbose

    for r in resp:
        #rprint(f' [-] [{r.status_code}] {r.url} ')
        #rprint(r.json())
        jj = r.json()
        
        cname = jj.get('name', None)
        cdate = jj.get('public_date', '')
        ccvss = jj.get('cvss3').get('cvss3_base_score', '')
        if jj.get('mitigation'):
            cfixv = jj.get('mitigation').get('value', '')
        else:
            cfixv = f'<NO mitigation>'

        cprod = []
        cvuln = jj.get('affected_release')
        for v in cvuln:
            prod = v.get('product_name', '')
            vcpe = v.get('cpe', '')
            rhsa = v.get('advisory', '')
            date = f"{v.get('release_date', ''):<10.10s}"
            pack = v.get('package', '')
            #cprod.append(f'{prod} [ {vcpe} ]\n\t\t{rhsa} ({date})\n\t\tPackages: {pack}')
            #cprod.append(f'OS      : {prod} [ {vcpe} ]\n\tPackages: {pack}')
            #cprod.append(f'OS/package : [blue]{prod}[/blue] [ [green]{vcpe}[/green] ] [i]Packages=[magenta]{pack}[/magenta][/i] | [red]{rhsa}[/red] ({date:<10.10s})')
            cprod.append(f'OS/package : [blue]{vcpe}[/blue] [ [green]{prod}[/green] ] [i]Packages=[magenta]{pack}[/magenta][/i] | [red]{rhsa}[/red] ({date:<10.10s})')

        print(f'')
        rprint(f' [+] CVE/date   : {cname}/{ccvss} (released at {cdate:<10.10s})')
        for p in cprod:
            # Showing affected_release
            rprint(f' [-] {p}')

        if verbose:
            print(f'')
            rprint(f' [-] Mitigation : {cfixv}')
            pstat = jj.get('package_state')
            for p in pstat:
                pname = p.get('product_name', '')
                ppack = p.get('package_name', '')
                pdcpe = p.get('cpe', '')
                pfixs = p.get('fix_state')

                rprint(f' [-] os/package : [i]{pdcpe} [{pname}] [magenta]{ppack}[/magenta] ([cyan]{pfixs}[/cyan])[/i]')



def usage():
    """ usage() function """
    parser = argparse.ArgumentParser(description=banner, formatter_class=argparse.RawTextHelpFormatter, epilog=note)
    parser.add_argument('-e', dest='cve', metavar='<cve>', nargs='+', help='Specify a CVE or a list of CVEs.')
    parser.add_argument('-v', action='store_true', help='verbose output')

    return parser.parse_args()

@timeit
def main():
    """ main() function """
    global verbose

    args = usage()
    verbose = True if args.v else False
    links = []

    # /cve/CVE-2016-3706.json
    # https://access.redhat.com/hydra/rest/securitydata/csaf.json?cve=CVE-2023-1829,CVE-2023-3090,CVE-2023-3390

    if args.cve:
        cves1 = []
        for cve in args.cve:
            if not cve.upper().startswith('CVE-'):
                cve = 'CVE-' + cve
            cves1.append(cve)
        cves2 = list(set(cve.upper() for cve in cves1))
        links = [ f'{base_url}/cve/{cve}.json' for cve in cves2 ]

    print(f'')
    rprint(f' [*] Searching {len(cves2)}/{len(cves1)} CVEs...')

    resp = asyncio.run(fetching(links))
    Showing(resp)

    return

if __name__ == "__main__":

    if sys.version_info.major == 2:
        print('This script needs Python 3.')
    else:
        print(f'')
        main()
    
