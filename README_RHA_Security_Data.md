# Red Hat Security Data API

The full page can be access at [Red Hat Security Data API](https://docs.redhat.com/en/documentation/red_hat_security_data_api/1.0/html-single/red_hat_security_data_api/index).

## Usage


```console

$ python rha_cve_check.py 2024-3094 2024-6387


 [*] Searching 2/2 CVEs...

 [+] [200] https://access.redhat.com/hydra/rest/securitydata/cve/CVE-2024-3094.json
 [+] [200] https://access.redhat.com/hydra/rest/securitydata/cve/CVE-2024-6387.json

 [*] All [2 responses] are OK.

 [*] Successful fetched : 2/2

 [+] CVE/date   : CVE-2024-3094/10.0 (released at 2024-03-29)
 [-] OS/package : Current investigation indicates that no versions of Red Hat Enterprise Linux (RHEL) are affected.

 [+] CVE/date   : CVE-2024-6387/8.1 (released at 2024-07-01)
 [-] OS/package : cpe:/a:redhat:enterprise_linux:9 [ Red Hat Enterprise Linux 9 ] Packages=openssh-0:8.7p1-38.el9_4.1 | RHSA-2024:4312 (2024-07-03)
 [-] OS/package : cpe:/o:redhat:enterprise_linux:9 [ Red Hat Enterprise Linux 9 ] Packages=openssh-0:8.7p1-38.el9_4.1 | RHSA-2024:4312 (2024-07-03)
 [-] OS/package : cpe:/a:redhat:rhel_e4s:9.0 [ Red Hat Enterprise Linux 9.0 Update Services for SAP Solutions ] Packages=openssh-0:8.7p1-12.el9_0.1 | RHSA-2024:4389 (2024-07-08)
 [-] OS/package : cpe:/a:redhat:rhel_eus:9.2 [ Red Hat Enterprise Linux 9.2 Extended Update Support ] Packages=openssh-0:8.7p1-30.el9_2.4 | RHSA-2024:4340 (2024-07-05)
 [-] OS/package : cpe:/a:redhat:openshift:4.13::el9 [ Red Hat OpenShift Container Platform 4.13 ] Packages=rhcos-413.92.202407091321-0 | RHSA-2024:4484 (2024-07-17)
 [-] OS/package : cpe:/a:redhat:openshift:4.14::el9 [ Red Hat OpenShift Container Platform 4.14 ] Packages=rhcos-414.92.202407091253-0 | RHSA-2024:4479 (2024-07-17)
 [-] OS/package : cpe:/a:redhat:openshift:4.15::el9 [ Red Hat OpenShift Container Platform 4.15 ] Packages=rhcos-415.92.202407091355-0 | RHSA-2024:4474 (2024-07-18)
 [-] OS/package : cpe:/a:redhat:openshift:4.16::el9 [ Red Hat OpenShift Container Platform 4.16 ] Packages=rhcos-416.94.202407081958-0 | RHSA-2024:4469 (2024-07-16)

 [*] main(): completed within [0.1968 sec].

$ python rha_cve_check.py 2024-3094 2024-6387 -v

 [*] Searching 2/2 CVEs...

 [+] [200] https://access.redhat.com/hydra/rest/securitydata/cve/CVE-2024-6387.json
 [+] [200] https://access.redhat.com/hydra/rest/securitydata/cve/CVE-2024-3094.json

 [*] All [2 responses] are OK.

 [*] Successful fetched : 2/2

 [+] CVE/date   : CVE-2024-6387/8.1 (released at 2024-07-01)
 [-] OS/package : cpe:/a:redhat:enterprise_linux:9 [ Red Hat Enterprise Linux 9 ] Packages=openssh-0:8.7p1-38.el9_4.1 | RHSA-2024:4312 (2024-07-03)
 [-] OS/package : cpe:/o:redhat:enterprise_linux:9 [ Red Hat Enterprise Linux 9 ] Packages=openssh-0:8.7p1-38.el9_4.1 | RHSA-2024:4312 (2024-07-03)
 [-] OS/package : cpe:/a:redhat:rhel_e4s:9.0 [ Red Hat Enterprise Linux 9.0 Update Services for SAP Solutions ] Packages=openssh-0:8.7p1-12.el9_0.1 | RHSA-2024:4389 (2024-07-08)
 [-] OS/package : cpe:/a:redhat:rhel_eus:9.2 [ Red Hat Enterprise Linux 9.2 Extended Update Support ] Packages=openssh-0:8.7p1-30.el9_2.4 | RHSA-2024:4340 (2024-07-05)
 [-] OS/package : cpe:/a:redhat:openshift:4.13::el9 [ Red Hat OpenShift Container Platform 4.13 ] Packages=rhcos-413.92.202407091321-0 | RHSA-2024:4484 (2024-07-17)
 [-] OS/package : cpe:/a:redhat:openshift:4.14::el9 [ Red Hat OpenShift Container Platform 4.14 ] Packages=rhcos-414.92.202407091253-0 | RHSA-2024:4479 (2024-07-17)
 [-] OS/package : cpe:/a:redhat:openshift:4.15::el9 [ Red Hat OpenShift Container Platform 4.15 ] Packages=rhcos-415.92.202407091355-0 | RHSA-2024:4474 (2024-07-18)
 [-] OS/package : cpe:/a:redhat:openshift:4.16::el9 [ Red Hat OpenShift Container Platform 4.16 ] Packages=rhcos-416.94.202407081958-0 | RHSA-2024:4469 (2024-07-16)

 [-] Mitigation : The below process can protect against a Remote Code Execution attack by disabling the LoginGraceTime parameter on Red Hat Enterprise Linux 9. However, the sshd server is still vulnerable to a
Denial of Service if an attacker exhausts all the connections.
1) As root user, open the /etc/ssh/sshd_config
2) Add or edit the parameter configuration:
~~~
LoginGraceTime 0
~~~
3) Save and close the file
4) Restart the sshd daemon:
~~~
systemctl restart sshd.service
~~~
Setting LoginGraceTime to 0 disables the SSHD server's ability to drop connections if authentication is not completed within the specified timeout. If this mitigation is implemented, it is highly recommended
to use a tool like 'fail2ban' alongside a firewall to monitor log files and manage connections appropriately.
If any of the mitigations mentioned above is used, please note that the removal of LoginGraceTime parameter from sshd_config is not automatic when the updated package is installed.
 [-] os/package : cpe:/a:redhat:ceph_storage:5 [Red Hat Ceph Storage 5] openssh (Not affected)
 [-] os/package : cpe:/a:redhat:ceph_storage:6 [Red Hat Ceph Storage 6] openssh (Affected)
 [-] os/package : cpe:/a:redhat:ceph_storage:7 [Red Hat Ceph Storage 7] openssh (Affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:6 [Red Hat Enterprise Linux 6] openssh (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:7 [Red Hat Enterprise Linux 7] openssh (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:8 [Red Hat Enterprise Linux 8] openssh (Not affected)

 [+] CVE/date   : CVE-2024-3094/10.0 (released at 2024-03-29)
 [-] OS/package : Current investigation indicates that no versions of Red Hat Enterprise Linux (RHEL) are affected.

 [-] Mitigation : <NO mitigation>
 [-] os/package : cpe:/o:redhat:enterprise_linux:6 [Red Hat Enterprise Linux 6] xz (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:7 [Red Hat Enterprise Linux 7] xz (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:8 [Red Hat Enterprise Linux 8] xz (Not affected)
 [-] os/package : cpe:/o:redhat:enterprise_linux:9 [Red Hat Enterprise Linux 9] xz (Not affected)
 [-] os/package : cpe:/a:redhat:jboss_enterprise_application_platform:8 [Red Hat JBoss Enterprise Application Platform 8] xz (Not affected)

 [*] main(): completed within [0.1574 sec].

```
