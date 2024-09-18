# Red Hat Security Data API

The full page can be access at [Red Hat Security Data API](https://docs.redhat.com/en/documentation/red_hat_security_data_api/1.0/html-single/red_hat_security_data_api/index).

## Usage


```console

$ python3 rh_cve_check.py -e CVE-2022-48565

 [*] Searching 1/1 CVEs...

 [+] [200] https://access.redhat.com/hydra/rest/securitydata/cve/CVE-2022-48565.json

 [*] All [1 responses] are OK.

 [*] Successful fetched : 1/1

 [+] CVE/date   : CVE-2022-48565/7.8 (released at 2023-08-22)
 [-] OS/package : cpe:/a:redhat:enterprise_linux:8 [ Red Hat Enterprise Linux 8 ] Packages=python27:2.7-8100020240208011952.5f0f67de | RHSA-2024:2987
(2024-05-22)

 [*] main(): completed within [0.1276 sec].


$ python3 rh_cve_check.py -e CVE-2022-48565 -v

 [*] Searching 1/1 CVEs...

 [+] [200] https://access.redhat.com/hydra/rest/securitydata/cve/CVE-2022-48565.json

 [*] All [1 responses] are OK.

 [*] Successful fetched : 1/1

 [+] CVE/date   : CVE-2022-48565/7.8 (released at 2023-08-22)
 [-] OS/package : cpe:/a:redhat:enterprise_linux:8 [ Red Hat Enterprise Linux 8 ] Packages=python27:2.7-8100020240208011952.5f0f67de | RHSA-2024:2987
(2024-05-22)

 [-] Mitigation : The XML modules in python are not secure against erroneous or maliciously constructed data. If you need to parse untrusted or
unauthenticated data, see the XML vulnerabilities and the defusedxml package sections.
https://docs.python.org/dev/library/xml.html
 [-] os/package : cpe:/o:redhat:enterprise_linux:6 [Red Hat Enterprise Linux 6] python (Out of support scope)
 [-] os/package : cpe:/o:redhat:enterprise_linux:7 [Red Hat Enterprise Linux 7] python (Out of support scope)
 [-] os/package : cpe:/o:redhat:enterprise_linux:7 [Red Hat Enterprise Linux 7] python3 (Out of support scope)
 [-] os/package : cpe:/o:redhat:enterprise_linux:8 [Red Hat Enterprise Linux 8] gimp:flatpak/python2 (Affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:8 [Red Hat Enterprise Linux 8] inkscape:flatpak/python2 (Will not fix)
 [-] os/package : cpe:/o:redhat:enterprise_linux:8 [Red Hat Enterprise Linux 8] python3 (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:8 [Red Hat Enterprise Linux 8] python3.11 (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:8 [Red Hat Enterprise Linux 8] python36:3.6/python36 (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:8 [Red Hat Enterprise Linux 8] python39:3.9/python39 (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:9 [Red Hat Enterprise Linux 9] python3.11 (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:9 [Red Hat Enterprise Linux 9] python3.9 (Not affected)
 [-] os/package : cpe:/a:redhat:rhel_software_collections:3 [Red Hat Software Collections] rh-python38-python (Not affected)

 [*] main(): completed within [0.2300 sec].

```
