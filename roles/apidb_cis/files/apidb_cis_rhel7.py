import commands
import os
file="/tmp/local/api_cis.fact"
f = open(file,"w")
f.write("[cis_facts]\n")



def cis_check_output(command,check,csid):
    status,output = commands.getstatusoutput(command)
    print "Checking if {0} is equal to {1}\n".format(output,check)
    if output == check:
        result = "{0}: PASSED: {1}".format(csid,output)
    else:
        result = "{0}: FAILED: {1}".format(csid,output)
    f.write(result+"\n")

def cis_check_output_rev(command,check,csid):
    status,output = commands.getstatusoutput(command)
    print "Checking if {0} is equal to {1}\n".format(output,check)
    if output == check:
        result = "{0}: FAILED: {1}".format(csid,output)
    else:
        result = "{0}: PASSED: {1}".format(csid,output)
    f.write(result+"\n")

### FILESYSTEM check start:
cis_check_output('if grep "[[:space:]]/tmp[[:space:]]" /etc/fstab > /dev/null; then echo "/tmp is mounted"; else echo "/tmp Not mounted";fi',"/tmp is mounted","1.1.2")
cis_check_output('if mount | grep -E \'\s/tmp\si\' | grep -v noexec; then echo "noexec is set on /tmp"; else echo "noexec is not set on /tmp";fi',"noexec is set on /tmp","1.1.3")
cis_check_output('if mount | grep -E \'\s/tmp\si\' | grep -v nodev; then echo "nodev is set on /tmp"; else echo "nodev is not set on /tmp";fi',"nodev is set on /tmp","1.1.4")
cis_check_output('if mount | grep -E \'\s/tmp\si\' | grep -v nosuid; then echo "nosuid is set on /tmp"; else echo "nosuid is not set on /tmp";fi',"nosuid is set on /tmp","1.1.5")
cis_check_output('if grep "[[:space:]]/dev/shm[[:space:]]" /etc/fstab > /dev/null; then echo "/dev/shm is mounted"; else echo "/dev/shm Not mounted";fi',"/dev/shm is mounted","1.1.6")
cis_check_output('if mount | grep -E \'\s/dev/shm\si\' | grep -v noexec; then echo "noexec is set on /dev/shm"; else echo "noexec is not set on /dev/shm";fi',"noexec is set on /dev/shm","1.1.7")
cis_check_output('if mount | grep -E \'\s/dev/shm\si\' | grep -v nodev; then echo "nodev is set on /dev/shm"; else echo "nodev is not set on /dev/shm";fi',"nodev is set on /dev/shm","1.1.8")
cis_check_output('if mount | grep -E \'\s/dev/shm\si\' | grep -v nosuid; then echo "nosuid is set on /dev/shm"; else echo "nosuid is not set on /dev/shm";fi',"nosuid is set on /dev/shm","1.1.9")
cis_check_output('if grep "[[:space:]]/var[[:space:]]" /etc/fstab > /dev/null; then echo "/var is mounted"; else echo "/var Not mounted";fi',"/var is mounted","1.1.10")
cis_check_output('if grep "[[:space:]]//var/tmp[[:space:]]" /etc/fstab > /dev/null; then echo "/var/tmp is mounted"; else echo "/var/tmp Not mounted";fi',"/var/tmp is mounted","1.1.11")
cis_check_output('if mount | grep -E \'\s/var/tmp\si\' | grep -v noexec; then echo "noexec is set on /var/tmp"; else echo "noexec is not set on /var/tmp";fi',"noexec is set on /var/tmp","1.1.12")
cis_check_output('if mount | grep -E \'\s/var/tmp\si\' | grep -v nodev; then echo "nodev is set on /var/tmp"; else echo "nodev is not set on /var/tmp";fi',"nodev is set on /var/tmp","1.1.13")
cis_check_output('if mount | grep -E \'\s/var/tmp\si\' | grep -v nosuid; then echo "nosuid is set on /var/tmp"; else echo "nosuid is not set on /var/tmp";fi',"nosuid is set on /var/tmp","1.1.14")
cis_check_output('if grep "[[:space:]]/var/log[[:space:]]" /etc/fstab > /dev/null; then echo "/var/log is mounted"; else echo "/var/log Not mounted";fi',"/var/log is mounted","1.1.15")
cis_check_output('if grep "[[:space:]]/var/log/audit[[:space:]]" /etc/fstab > /dev/null; then echo "/var/log/audit is mounted"; else echo "/var/log/audit Not mounted";fi',"/var/log/audit is mounted","1.1.16")
cis_check_output('if grep "[[:space:]]/home[[:space:]]" /etc/fstab > /dev/null; then echo "/home is mounted"; else echo "/home Not mounted";fi',"/home is mounted","1.1.17")
cis_check_output('if mount | grep -E \'\s/home\si\' | grep -v nodev; then echo "nodev is set on /home"; else echo "nodev is not set on /home";fi',"nodev is set on /home","1.1.18")
## FILESYSTEM check end:


### OTHER start:
# 1.1.19 Ensure noexec option set on removable media partitions (Not Sorced)
# 1.1.20 Ensure nodev option set on removable media partitions (Not Scored)
# 1.1.21 Ensure nosuid option set on removable media partitions (Not Scored)

# 1.1.22 Ensure sticky bit is set on all world-writable directories (Scored)
# 1.1.23 Disable Automounting (Scored)
# 1.1.24 Disable USB Storage (Scored)

# 1.2.1 Ensure GPG keys are configured (Not Scored)
# 1.2.2 Ensure package manager repositories are configured (Not Scored)
# 1.2.3 Ensure gpgcheck is globally activated (Scored)
# 1.2.4 Ensure Red Hat Subscription Manager connection is configured (not required?)
# 1.2.5 Disable the rhnsd Daemon (Not Scored)
# 1.3.1 Ensure sudo is installed (Scored)
cis_check_output_rev("rpm -q sudo","package sudo is not installed","1.3.1")
# 1.3.2 Ensure sudo commands use pty (Scored)
# 1.3.3 Ensure sudo log file exists (Scored)

# 1.4.1 Ensure AIDE is installed (Scored)
cis_check_output_rev("rpm -q aide","package aide is not installed","1.4.1")
# 1.4.2 Ensure filesystem integrity is regularly checked (Scored)

# 1.5.1 Ensure bootloader password is set (Scored)
# 1.5.2 Ensure permissions on bootloader config are configured (Scored)
# 1.5.3 Ensure authentication required for single user mode 

# 1.6.1 Ensure core dumps are restricted (Scored)
# 1.6.2 Ensure XD/NX support is enabled
# 1.6.3 Ensure address space layout randomization (ASLR) is enabled (Scored)
# 1.6.4 Ensure prelink is disabled

# 1.7.1.1 Ensure SELinux is installed (Scored)
cis_check_output_rev("rpm -q libselinux| grep x86","package libselinux is not installed","1.7.1.1")
# 1.7.1.2 Ensure SELinux is not disabled in bootloader configuration (Scored)
# 1.7.1.3 Ensure SELinux policy is configured
# 1.7.1.4 Ensure the SELinux state is enforcing or permissive (Scored)
# 1.7.1.5 Ensure the SELinux mode is enforcing
# 1.7.1.6 Ensure no unconfined services exist (Scored)
# 1.7.1.7 Ensure SETroubleshoot is not installed (Scored)
cis_check_output("rpm -q setroubleshoot","package setroubleshoot is not installed","1.7.1.6")
# 1.7.1.8 Ensure the MCS Translation Service (mcstrans) is not installed (Scored)
cis_check_output("rpm -q mcstrans","package mcstrans is not installed","1.7.1.7")

# 1.8.1.1 Ensure message of the day is configured properly (Scored)
# 1.8.1.2 Ensure local login warning banner is configured properly (Scored)
# 1.8.1.3 Ensure remote login warning banner is configured properly
# 1.8.1.4 Ensure permissions on /etc/motd are configured (Scored)
# 1.8.1.5 Ensure permissions on /etc/issue are configured (Scored)
# 1.8.1.6 Ensure permissions on /etc/issue.net are configured (Scored)
# 1.8.2 Ensure GDM login banner is configured (Scored)
# 1.9 Ensure updates, patches, and additional security software are installed (Scored)
# 1.10 Ensure GDM is removed or login is configured

# 2.1.1 Ensure xinetd is not installed (Scored)
cis_check_output("rpm -q xinetd","package xinetd is not installed","2.1.1")

#### NTP/CHRONY CHECK start:
### Need to setup a check for both NTP and Chrony. Check for either and
# only do checks for that service.
# 2.2.1.1 Ensure time synchronization is in use (Not Scored)
#cis_check_output("rpm -q chrony","package chrony is not installed","2.2.1.1")
# 2.2.1.1 Ensure time synchronization is in use (Not Scored)
#cis_check_output("rpm -q ntp","package ntp is not installed","2.2.1.1")
# 2.2.1.2 Ensure chrony is configured (Scored)
#cis_check_output('if grep -E "^(server|pool)" /etc/chrony.conf; then echo "Remote time server is configured"; else echo "Remote time server is Not configured";fi',"Remote time server is configured","2.2.1.2")
# 2.2.1.3 Ensure ntp is configured (Scored)
#cis_check_output('if grep -E "^(server|pool)" /etc/ntp.conf; then echo "Remote time server is configured"; else echo "Remote time server is Not configured";fi',"Remote time server is configured","2.2.1.3")
## NTP/CHRONY CHECK end:


## OTHER end:


### PACKAGE check start:
cis_check_output("rpm -q ypbind","package ypbind is not installed","2.2.1")

cis_check_output("rpm -q xorg-x11-server*","package xorg-x11-server* is not installed","2.2.2")
cis_check_output("rpm -q avahi","package avahi is not installed","2.2.3")
cis_check_output("rpm -q cups","package cups is not installed","2.2.4")
cis_check_output("rpm -q dhcp","package dhcp is not installed","2.2.5")
cis_check_output("rpm -q openldap-servers","package openldap-servers is not installed","2.2.6")
# 2.2.7 Ensure nfs-utils is not installed or the nfs-server service is masked
# 2.2.8 Ensure rpcbind is not installed or the rpcbind services are masked
cis_check_output("rpm -q bind","package bind is not installed","2.2.9")
cis_check_output("rpm -q vsftp","package vsftp is not installed","2.2.10")
cis_check_output("rpm -q httpd","package httpd is not installed","2.2.11")
cis_check_output("rpm -q dovecot","package dovecot is not installed","2.2.12")
cis_check_output("rpm -q smb","package smb is not installed","2.2.13")
cis_check_output("rpm -q squid","package squid is not installed","2.2.14")
cis_check_output("rpm -q net-snmp","package net-snmp is not installed","2.2.15")
# 2.2.16 Ensure mail transfer agent is configured for local-only mode
# 2.2.17 Ensure rsync is not installed or the rsyncd service is masked
cis_check_output("rpm -q ypserv","package ypserv is not installed","2.2.18")
cis_check_output("rpm -q telnet-server","package telnet-server is not installed","2.2.19")
cis_check_output("rpm -q ypbind","package ypbind is not installed","2.3.1")
cis_check_output("rpm -q rsh","package rsh is not installed","2.3.2")
cis_check_output("rpm -q talk","package talk is not installed","2.3.3")
cis_check_output("rpm -q telnet","package telnet is not installed","2.3.4")
cis_check_output("rpm -q openldap-clients","package openldap-clients is not installed","2.3.5")

## PACKAGE check end:


#### SYSCTL checks start:
cis_check_output('if grep \'GRUB_CMDLINE_LINUX="ipv6.disable=1"\' /etc/default/grub || /usr/sbin/sysctl net.ipv6.conf.all.disable_ipv6 -eq "net.ipv6.conf.all.disable_ipv6 = 0" > /dev/null && /usr/sbin/sysctl net.ipv6.conf.default.disable_ipv6 -eq "net.ipv6.conf.default.disable_ipv6 = 1" > /dev/null; then echo "IPV6 disabled in GRUB"; else echo "IPV6 Not disabled in GRUB";fi',"IPV6 disabled in GRUB","3.1.1")
## SYSCTL check end:

cis_check_output("/usr/sbin/sysctl net.ipv4.conf.all.forwarding","net.ipv4.conf.all.forwarding = 0","3.2.1") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.all.send_redirects","net.ipv4.conf.all.send_redirects = 0","3.2.2") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.default.send_redirects","net.ipv4.conf.default.send_redirects = 0","3.1.2") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.all.accept_source_route","net.ipv4.conf.all.accept_source_route = 0","3.3.1") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.default.accept_source_route","net.ipv4.conf.default.accept_source_route = 0","3.3.1") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.all.accept_redirects","net.ipv4.conf.all.accept_redirects = 0","3.3.2") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.default.accept_redirects","net.ipv4.conf.default.accept_redirects = 0","3.3.2") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.all.secure_redirects","net.ipv4.conf.all.secure_redirects = 0","3.3.3") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.default.secure_redirects","net.ipv4.conf.default.secure_redirects = 0","3.3.3") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.all.log_martians","net.ipv4.conf.all.log_martians = 1","3.3.4") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.default.log_martians","net.ipv4.conf.default.log_martians = 1","3.3.4") 
cis_check_output("/usr/sbin/sysctl net.ipv4.icmp_echo_ignore_broadcasts","net.ipv4.icmp_echo_ignore_broadcasts = 1","3.3.5") 
cis_check_output("/usr/sbin/sysctl net.ipv4.icmp_ignore_bogus_error_responses","net.ipv4.icmp_ignore_bogus_error_responses = 1","3.3.6") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.all.rp_filter","net.ipv4.conf.all.rp_filter = 1","3.3.7") 
cis_check_output("/usr/sbin/sysctl net.ipv4.conf.default.rp_filter","net.ipv4.conf.default.rp_filter = 1","3.3.7") 
cis_check_output("/usr/sbin/sysctl net.ipv4.tcp_syncookies","net.ipv4.tcp_syncookies = 1","3.3.8") 

#status,output = commands.getstatusoutput('grep GRUB_CMDLINE_LINUX="ipv6.disable=1" /etc/default/grub')
# FIX LOGIC
status,output = commands.getstatusoutput('if grep \'GRUB_CMDLINE_LINUX="ipv6.disable=1"\' /etc/default/grub || /usr/sbin/sysctl net.ipv6.conf.all.disable_ipv6 -eq "net.ipv6.conf.all.disable_ipv6 = 0" > /dev/null && /usr/sbin/sysctl net.ipv6.conf.default.disable_ipv6 -eq "net.ipv6.conf.default.disable_ipv6 = 1" > /dev/null; then echo "1"; else "256";fi')
#print(status)
if status == 256:
## ONLY RUN IF IPV6 ABOVE IS NOT DISABLED:
  cis_check_output("/usr/sbin/sysctl net.ipv6.conf.all.forwarding","net.ipv6.conf.all.forwarding = 0","3.2.1")
  cis_check_output("/usr/sbin/sysctl net.ipv6.conf.all.accept_source_route","net.ipv6.conf.default.send_redirects = 0","3.3.1")
  cis_check_output("/usr/sbin/sysctl net.ipv6.conf.default.accept_source_route","net.ipv6.conf.default.accept_source_route = 0","3.3.1")
  cis_check_output("/usr/sbin/sysctl net.ipv6.conf.all.accept_redirects","net.ipv6.conf.all.accept_redirects = 0","3.3.2")
  cis_check_output("/usr/sbin/sysctl net.ipv6.conf.default.accept_redirects","net.ipv6.conf.default.accept_redirects = 0","3.3.2")
  cis_check_output("/usr/sbin/sysctl net.ipv6.conf.all.accept_ra","net.ipv6.conf.all.accept_ra = 1","3.3.9")
  cis_check_output("/usr/sbin/sysctl net.ipv6.conf.default.accept_ra","net.ipv6.conf.default.accept_ra = 1","3.3.9")
else:
  pass
## SYSCTL check end:

# Uncommon network protocols - These need work
### MODPROBE check start:
# 3.4.1 Ensure DCCP is disabled 
# 3.4.2 Ensure SCTP is disabled
#cis_check_output("modprobe -n -v DCCP","install /bin/true","3.3.3")
#cis_check_output("modprobe -n -v SCTP","install /bin/true","3.3.3")
## MODPROBE check end:


### FIREWALL check start:
# Pass only if both are installed
cis_check_output('if rpm -q --quiet firewalld && rpm -q --quiet iptables ; then echo "Both firewalld & iptables are installed"; else echo "Both firewalld & iptables are not installed";fi',"Both firewalld & iptables are installed","3.5.1.1")
cis_check_output("rpm -q iptables-services","package iptables-services is not installed","3.5.1.2")
# 3.5.1.3 Ensure nftables is not installed or stopped and masked
# 3.5.1.4 - need to remove sudo and use ansible become = root
#cis_check_output('if systemctl is-enabled -q firewalld && sudo firewall-cmd -q --state 2> /dev/null; then echo "Firewall service is enabled and running"; else echo "Firewall service is not enabled and running";fi',"Firewall service is enabled and running","3.5.1.4")
# 3.5.1.5 Ensure default zone is set
# 3.5.1.6 Ensure network interfaces are assigned to appropriate zone 
# 3.5.1.7 Ensure unnecessary services and ports are not accepted
cis_check_output("rpm -q nftables","package nftables is not installed","3.5.2.1")

#### nftables start:
## Following only required if not using firewalld - I think we should remove
# 3.5.2.2 Ensure firewalld is not installed or stopped and masked
# 3.5.2.3 Ensure iptables-services package is not installed
# 3.5.2.4 Ensure iptables are flushed 
# 3.5.2.5 Ensure a table exists
# 3.5.2.6 Ensure base chains exist
# 3.5.2.7 Ensure loopback traffic is configured
# 3.5.2.8 Ensure outbound and established connections are configured
# 3.5.2.9 Ensure default deny firewall policy
# 3.5.2.10 Ensure nftables service is enabled
# 3.5.2.11 Ensure nftables rules are permanent
# nftables end:

# 3.5.3 -->  3.5.3.3.6 - Need to discuss.
## FIREWALL check end:

## Logging and Auditing
cis_check_output('if rpm -q --quiet audit && rpm -q --quiet audit-libs; then echo "Both Audit & Audit-libs are installed"; else echo "Both Audit & Audit-libs are not installed";fi',"Both Audit & Audit-libs are installed","4.1.1.1")
cis_check_output('if systemctl is-enabled -q auditd && systemctl status auditd | grep "Active: active (running) " > /dev/null; then echo "Auditd service is enabled and running"; else echo "Auditd service is not enabled and running";fi',"Auditd service is enabled and running","4.1.1.2")



f.close()

