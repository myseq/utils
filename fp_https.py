#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
from timeit import default_timer as timer
from rich import print as rprint

import ssl, socket
import OpenSSL
import hashlib

#https = 'myseq.github.io'

desc = f'Fingerprinting HTTPS Certificate.'
note = f'''

        This is a tool to fingerprint any HTTPS certificate, including the Issuer and Issuee. 

'''

banner = f'''
   Zzzzz   |\\      _,,,---,,_
           /,`.-'`'    -.  ;-;;,_   __author__ : [ zd ]
          |,4-  ) )-,_..;\\ (  `'-'  __year__   : [ 2024.06 ]
         '---''(_/--'  `-'\\_)       __file__   : [ {__file__} ]

         [ {desc} ]
    '''

verbose = False

def timeit(func):
    def timed(*args, **kwargs):
        stime = timer()
        result = func(*args, **kwargs)
        etime = timer()
        rprint(f'\n :timer_clock:  {func.__name__}(): completed within [{etime-stime:.4f} sec].\n ')
        return result
    return timed


def Formatting(thumb_hash):
    """ Formatting(): Format the hash value """ 
    fp = ''
    for i in range(0, len(thumb_hash), 2):
        fp += thumb_hash[i:i+2]
        if i < len(thumb_hash)-2:
            fp += ':'
    return fp


def Validating(date1,date2):
    """ Validating(): Check the validity of the certificate date """

    today = datetime.now()
    dt1 = datetime.strptime(date1, "%Y%m%d%H%M%SZ")
    dt2 = datetime.strptime(date2, "%Y%m%d%H%M%SZ")

    if dt1 <= today <= dt2:
        return 'Valid :+1: '
    else:
        return 'Invalid :warning: '

def get_details(cert):
    """ get_details() function: To get details out of the certificate """
    details = {}

    details['subject'] = {key.decode(): value.decode() for key, value in cert.get_subject().get_components()}
    details['issuer'] = {key.decode(): value.decode() for key, value in cert.get_issuer().get_components()}
    details['serialNumber'] = cert.get_serial_number()
    details['version'] = cert.get_version() + 1  # pyOpenSSL returns version as 0-indexed
    details['notBefore'] = cert.get_notBefore().decode()
    details['notAfter'] = cert.get_notAfter().decode()
    details['signatureAlgorithm'] = cert.get_signature_algorithm().decode()
    
    # Extract public key details
    pub_key = cert.get_pubkey()
    pub_key_bits = pub_key.bits()
    pub_key_type = pub_key.type()
    details['publicKey'] = {
        'type': pub_key_type,
        'bits': pub_key_bits,
        'key': pub_key
    }
    
    # Extract extensions
    extensions = {}
    for i in range(cert.get_extension_count()):
        ext = cert.get_extension(i)
        extensions[ext.get_short_name().decode()] = str(ext)
    details['extensions'] = extensions

    return details

def Showing(cert_bin):
    """ Showing() function: To display the output """

    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert_bin)
    cert_details = get_details(cert)
    #rprint(cert_details)

    issued_to = f"{cert_details.get('subject').get('CN')}"
    org_name1 = f"{cert_details.get('subject').get('O','')}"
    issued_by = f"{cert_details.get('issuer').get('CN')}"
    org_name2 = f"{cert_details.get('issuer').get('O','')}"
    serial_no = f"{cert_details.get('serialNumber')}"
    notbefore = f"{cert_details.get('notBefore')}"
    not_after = f"{cert_details.get('notAfter')}"
    sign_algo = f"{cert_details.get('signatureAlgorithm')}"
    publickey = f"{cert_details.get('publicKey').get('bits')}"
    subjetalt = f"{cert_details.get('extensions').get('subjectAltName','')}"

    title = 'Certificate'
    rprint(f'{title}')
    rprint(f'{"="*len(title)}')

    if verbose:
        rprint(f'Serial_No: [i]{serial_no}[/i]')

    validity = Validating(notbefore, not_after)
    rprint(f'Issued_To: [i]cn={issued_to}[/i] [ o={org_name1} ]')
    rprint(f'Issued_By: [i]cn={issued_by}[/i] [ o={org_name2} ]')
    dt1 = datetime.strptime(notbefore, '%Y%m%d%H%M%SZ')
    dt2 = datetime.strptime(not_after, '%Y%m%d%H%M%SZ')
    rprint(f'   Validity: [i]\'{dt1:%Y-%m-%d %H:%M:%S %Z}\'/\'{dt2:%Y-%m-%d %H:%M:%S %Z}\'[/i] [ {validity} ]')

    print(f'')
    thumb_sha1 = hashlib.sha1(cert_bin).hexdigest()
    thumb_sha2 = hashlib.sha256(cert_bin).hexdigest()
    fp1 = Formatting(thumb_sha1)
    fp2 = Formatting(thumb_sha2)

    if verbose:
        rprint(f'Public Key : {publickey} bits ')
        rprint(f'Algo Used  : {sign_algo} ')

    rprint(f'Fingerprint: \'{fp1}\' :thumbsup: [SHA1]')
    if verbose: 
        rprint(f'Fingerprint: \'{fp2}\' :+1: [SHA256]')
        rprint(f'\nAlt Name : \'{subjetalt}\'\n')

def usage():
    """ usage(): argument parser  """
    parser = argparse.ArgumentParser(description=banner, formatter_class=argparse.RawTextHelpFormatter, epilog=note)

    parser.add_argument('https', metavar='https-site', help='HTTPS site.')
    parser.add_argument('-p', metavar='[0..65535]', default=443, type=int, help='TCP port (default to 443).')
    parser.add_argument('-v', action='store_true', help='verbose output')

    return parser.parse_args()

@timeit
def main():
    """ main() function """
    global verbose
    global https

    args = usage()
    verbose = True if args.v else False
    https = args.https
    port = args.p

    rprint(f'\n  [*] [i]Fingerprint-check on [u]https://{https}:{port}/[/u] ...[/i] :magnifying_glass_tilted_left: \n')

    ctx = ssl.create_default_context()
    ctx.check_hostname = False    
    ctx.verify_mode = ssl.CERT_NONE

    with ctx.wrap_socket(socket.socket(), server_hostname=https) as s:
        s.connect((https, port))
        cert_bin = s.getpeercert(True)
        #cert = s.getpeercert()

    Showing(cert_bin)

if __name__ == "__main__":
    main()

