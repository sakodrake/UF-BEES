# Honeypot Demerit Report

**Honeypot:** `root@10.4.27.49:2222`  
**Ground truth:** `scalpel/tests/ground_truth.jsonl`  
**Generated:** 2026-04-23 11:53:01

## Summary

- **Tested:** 92 commands
- **Clean:** 18
- **Flagged:** 74 (80.4%)
- **Skipped (identity-dependent):** 24 — captured as `pi` user on ref Pi but red team logs into cowrie as `root`, so these mismatches are test-setup artifacts, not real fidelity gaps.

### Findings by type

| Count | Type |
|-------|------|
| 71 | output mismatch |
| 3 | line count far off |

## Flagged commands

### `hostnamectl` — deterministic

- output mismatch

**Expected:**
```
 Static hostname: raspberrypi
       Icon name: computer
      Machine ID: deb3ea2bcab54412a5ec9c8c0c2281fb
         Boot ID: b384a3a8d40c4ca9b688908a728ddf54
Operating System: Debian GNU/Linux 13 (trixie)
          Kernel: Linux 6.12.75+rpt-rpi-2712
    Architecture: arm64
```

**Got:**
```
-bash: hostnamectl: command not found
```

---

### `uname -a` — deterministic

- output mismatch

**Expected:**
```
Linux raspberrypi 6.12.75+rpt-rpi-2712 #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11) aarch64 GNU/Linux
```

**Got:**
```
Linux raspberrypi 3.2.0-4-amd64 #1 SMP Debian 3.2.68-1+deb7u1 x86_64 GNU/Linux
```

---

### `uname -m` — deterministic

- output mismatch

**Expected:**
```
aarch64
```

**Got:**
```
x86_64
```

---

### `uname -r` — deterministic

- output mismatch

**Expected:**
```
6.12.75+rpt-rpi-2712
```

**Got:**
```
3.2.0-4-amd64
```

---

### `uname -v` — deterministic

- output mismatch

**Expected:**
```
#1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11)
```

**Got:**
```
#1 SMP Debian 3.2.68-1+deb7u1
```

---

### `arch` — deterministic

- output mismatch

**Expected:**
```
aarch64
```

**Got:**
```
-bash: /usr/bin/arch: cannot execute binary file: Exec format error
```

---

### `cat /proc/cpuinfo` — deterministic

- output mismatch

**Expected:**
```
processor	: 0
BogoMIPS	: 108.00
Features	: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm lrcpc dcpop asimddp
CPU implementer	: 0x41
CPU architecture: 8
CPU variant	: 0x4
CPU part	: 0xd0b
CPU revision	: 1

processor	: 1
BogoMIPS	: 108.00
Features	: fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm lrcpc dcpop asimddp
CPU implementer	: 0x... [+637B]```

**Got:**
```
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 23
model name	: Intel(R) Core(TM)2 Duo CPU     E8200  @ 2.66GHz
stepping	: 6
cpu MHz		: 2133.304
cache size	: 6144 KB
physical id	: 0
siblings	: 2
core id		: 0
cpu cores	: 2
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 10
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat... [+1011B]```

---

### `cat /proc/version` — deterministic

- output mismatch

**Expected:**
```
Linux version 6.12.75+rpt-rpi-2712 (serge@raspberrypi.com) (aarch64-linux-gnu-gcc-14 (Debian 14.2.0-19) 14.2.0, GNU ld (GNU Binutils for Debian) 2.44) #1 SMP PREEMPT Debian 1:6.12.75-1+rpt1 (2026-03-11)
```

**Got:**
```
Linux version 3.2.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.6.3 (Debian 4.6.3-14) ) #1 SMP Debian 3.2.68-1+deb7u1
```

---

### `cat /etc/os-release` — deterministic

- output mismatch

**Expected:**
```
PRETTY_NAME="Debian GNU/Linux 13 (trixie)"
NAME="Debian GNU/Linux"
VERSION_ID="13"
VERSION="13 (trixie)"
VERSION_CODENAME=trixie
DEBIAN_VERSION_FULL=13.4
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```

**Got:**
```
```

---

### `cat /etc/debian_version` — deterministic

- output mismatch

**Expected:**
```
13.4
```

**Got:**
```
```

---

### `cat /etc/issue` — deterministic

- output mismatch

**Expected:**
```
Debian GNU/Linux 13 \n \l

```

**Got:**
```
Debian GNU/Linux 7 \n \l
```

---

### `lscpu` — deterministic

- output mismatch

**Expected:**
```
Architecture:                            aarch64
CPU op-mode(s):                          32-bit, 64-bit
Byte Order:                              Little Endian
CPU(s):                                  4
On-line CPU(s) list:                     0-3
Vendor ID:                               ARM
Model name:                              Cortex-A76
Model:                                   1
Thread(s) pe... [+2189B]```

**Got:**
```
Architecture:          x86_64
CPU op-mode(s):        32-bit, 64-bit
Byte Order:            Little Endian
CPU(s):                2
On-line CPU(s) list:   0-1
Thread(s) per core:    1
Core(s) per socket:    2
Socket(s):             1
NUMA node(s):          1
Vendor ID:             GenuineIntel
CPU family:            6
Model:                 23
Stepping:              6
CPU MHz:               2200.000... [+197B]```

---

### `lsb_release -a` — deterministic

- output mismatch

**Expected:**
```
Distributor ID:	Debian
Description:	Debian GNU/Linux 13 (trixie)
Release:	13
Codename:	trixie
```

**Got:**
```
-bash: lsb_release: command not found
```

---

### `uptime` — deterministic

- output mismatch

**Expected:**
```
 11:26:28 up 19:35,  5 users,  load average: 0.00, 0.00, 0.00
```

**Got:**
```
11:52:05  up 59 min,  1 user,  load average: 0.00, 0.00, 0.00
```

---

### `date` — deterministic

- output mismatch

**Expected:**
```
Thu 23 Apr 11:26:28 EDT 2026
```

**Got:**
```
Thu Apr 23 15:52:06 UTC 2026
```

---

### `free -m` — deterministic

- output mismatch

**Expected:**
```
               total        used        free      shared  buff/cache   available
Mem:           16218         432       15429          12         488       15786
Swap:           2047           0        2047
```

**Got:**
```
              total        used        free      shared  buff/cache   available
Mem:          16604         396       15899          13         308       16125
Swap:          2097           0        2097
```

---

### `free -h` — deterministic

- output mismatch

**Expected:**
```
               total        used        free      shared  buff/cache   available
Mem:            15Gi       432Mi        15Gi        12Mi       488Mi        15Gi
Swap:          2.0Gi          0B       2.0Gi
```

**Got:**
```
              total        used        free      shared  buff/cache   available
Mem:            16G        395M         15G         13M        308M         16G
Swap:            2G          0B          2G
```

---

### `df -h` — deterministic

- output mismatch

**Expected:**
```
Filesystem      Size  Used Avail Use% Mounted on
udev            7.9G     0  7.9G   0% /dev
tmpfs           3.2G   13M  3.2G   1% /run
/dev/mmcblk0p2  117G  4.1G  109G   4% /
tmpfs           8.0G     0  8.0G   0% /dev/shm
tmpfs           5.0M   48K  5.0M   1% /run/lock
tmpfs           1.0M     0  1.0M   0% /run/credentials/systemd-journald.service
tmpfs           8.0G     0  8.0G   0% /tmp
/dev/mm... [+258B]```

**Got:**
```
Filesystem                                              Size  Used Avail Use% Mounted on
rootfs                                                  4.7G  731M  3.8G  17% /
udev                                                     10M     0   10M   0% /dev
tmpfs                                                    25M  192K   25M   1% /run
/dev/disk/by-uuid/65626fdc-e4c5-4539-8745-edc212b9b0af  4.7G  731... [+190B]```

---

### `df -i` — deterministic

- output mismatch

**Expected:**
```
Filesystem      Inodes IUsed   IFree IUse% Mounted on
udev            516397   507  515890    1% /dev
tmpfs           519006   924  518082    1% /run
/dev/mmcblk0p2 7775376 73111 7702265    1% /
tmpfs           519006     1  519005    1% /dev/shm
tmpfs           519006     5  519001    1% /run/lock
tmpfs             1024     1    1023    1% /run/credentials/systemd-journald.service
tmpfs          ... [+318B]```

**Got:**
```
Filesystem                                              Size  Used Avail Use% Mounted on
rootfs                                                  4.7G  731M  3.8G  17% /
udev                                                     10M     0   10M   0% /dev
tmpfs                                                    25M  192K   25M   1% /run
/dev/disk/by-uuid/65626fdc-e4c5-4539-8745-edc212b9b0af  4.7G  731... [+190B]```

---

### `mount` — deterministic

- output mismatch

**Expected:**
```
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,relatime)
udev on /dev type devtmpfs (rw,nosuid,relatime,size=8262352k,nr_inodes=516397,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=600,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,nodev,noexec,relatime,size=3321648k,mode=755)
/dev/mmcblk0p2 on / type ext4 (rw,noatime)
sec... [+1912B]```

**Got:**
```
/dev/sda1 on / type ext3 (rw,errors=remount-ro)
tmpfs on /lib/init/rw type tmpfs (rw,nosuid,mode=0755)
proc on /proc type proc (rw,noexec,nosuid,nodev)
sysfs on /sys type sysfs (rw,noexec,nosuid,nodev)
udev on /dev type tmpfs (rw,mode=0755)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
devpts on /dev/pts type devpts (rw,noexec,nosuid,gid=5,mode=620)
```

---

### `ps aux` — variable

- line count far off (178 expected, 77 got)

**Expected:**
```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0  25472 14960 ?        Ss   Apr22   0:04 /sbin/init
root           2  0.0  0.0      0     0 ?        S    Apr22   0:00 [kthreadd]
root           3  0.0  0.0      0     0 ?        S    Apr22   0:00 [pool_workqueue_release]
root           4  0.0  0.0      0     0 ?        I<   Apr22   0:00 [kworker/R... [+15567B]```

**Got:**
```
USER         PID   %CPU       %MEM       VSZ       RSS       TTY     STAT  START
root         1     0.0        0.89       180281344 4587520   ?       Ss    Jul22
root         2     0.0        0.0        0         0         ?       S<    Jul22
root         3     0.0        0.0        0         0         ?       S<    Jul22
root         5     0.0        0.0        0         0         ?       D<    J... [+5837B]```

---

### `ps -ef` — variable

- line count far off (178 expected, 3 got)

**Expected:**
```
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 Apr22 ?        00:00:04 /sbin/init
root           2       0  0 Apr22 ?        00:00:00 [kthreadd]
root           3       2  0 Apr22 ?        00:00:00 [pool_workqueue_release]
root           4       2  0 Apr22 ?        00:00:00 [kworker/R-kvfree_rcu_reclaim]
root           5       2  0 Apr22 ?        00:00:00 [kwork... [+12893B]```

**Got:**
```
PID   TTY     TIME  COMMAND                     
7153  pts/0   0:00  -bash                        
7155  pts/0   0:00  ps -ef                          
```

---

### `top -bn1` — variable

- line count far off (184 expected, 1 got)

**Expected:**
```
top - 11:26:28 up 19:35,  5 users,  load average: 0.00, 0.00, 0.00
Tasks: 177 total,   1 running, 176 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.0 us,  0.0 sy,  0.0 ni,100.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st 
MiB Mem :  16218.9 total,  15426.5 free,    436.2 used,    488.8 buff/cache     
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.  15782.7 avail Mem 

    PID USER      PR  NI ... [+14157B]```

**Got:**
```
E82: Cannot allocate any buffer, exiting...
```

---

### `ls /` — deterministic

- output mismatch

**Expected:**
```
bin
boot
dev
etc
home
lib
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```

**Got:**
```
bin        boot       dev        etc        home       initrd.img lib        
lost+found media      mnt        opt        proc       root       run        
sbin       selinux    srv        sys        test2      tmp        usr        
var        vmlinuz    
```

---

### `ls -la /` — deterministic

- output mismatch

**Expected:**
```
total 64
drwxr-xr-x  18 root root  4096 Apr 12 20:06 .
drwxr-xr-x  18 root root  4096 Apr 12 20:06 ..
lrwxrwxrwx   1 root root     7 Mar  2 16:50 bin -> usr/bin
drwxr-xr-x   3 root root  4096 Apr 12 20:13 boot
drwxr-xr-x  16 root root  4200 Apr 23 10:37 dev
drwxr-xr-x  95 root root  4096 Apr 23 10:36 etc
drwxr-xr-x   3 root root  4096 Apr 12 20:06 home
lrwxrwxrwx   1 root root     7 Mar  2 16:50 l... [+662B]```

**Got:**
```
drwxr-xr-x 1 root root  4096 2013-04-05 08:03 .
drwxr-xr-x 1 root root  4096 2013-04-05 08:03 ..
drwxr-xr-x 1 root root  4096 2013-04-05 07:53 bin
drwxr-xr-x 1 root root  4096 2013-04-05 08:02 boot
drwxr-xr-x 1 root root  3060 2013-04-05 08:03 dev
drwxr-xr-x 1 root root  4096 2013-04-05 08:06 etc
drwxr-xr-x 1 root root  4096 2013-04-05 08:02 home
lrwxrwxrwx 1 root root    32 2013-04-05 07:53 initr... [+947B]```

---

### `ls /home` — deterministic

- output mismatch

**Expected:**
```
pi
```

**Got:**
```
phil 
```

---

### `ls /tmp` — deterministic

- output mismatch

**Expected:**
```
systemd-private-b384a3a8d40c4ca9b688908a728ddf54-bluetooth.service-5iy5tq
systemd-private-b384a3a8d40c4ca9b688908a728ddf54-polkit.service-mWUU9f
systemd-private-b384a3a8d40c4ca9b688908a728ddf54-systemd-hostnamed.service-2G3KqR
systemd-private-b384a3a8d40c4ca9b688908a728ddf54-systemd-logind.service-pHDZ3U
```

**Got:**
```
```

---

### `ls -la /tmp` — deterministic

- output mismatch

**Expected:**
```
total 4
drwxrwxrwt 10 root root  200 Apr 23 11:26 .
drwxr-xr-x 18 root root 4096 Apr 12 20:06 ..
drwxrwxrwt  2 root root   40 Apr 22 15:15 .font-unix
drwxrwxrwt  2 root root   40 Apr 22 15:15 .ICE-unix
drwx------  3 root root   60 Apr 22 15:15 systemd-private-b384a3a8d40c4ca9b688908a728ddf54-bluetooth.service-5iy5tq
drwx------  3 root root   60 Apr 23 11:23 systemd-private-b384a3a8d40c4ca9b688908a... [+380B]```

**Got:**
```
drwxrwxrwt 1 root root 4096 2013-04-05 08:17 .
drwxr-xr-x 1 root root 4096 2013-04-05 08:03 ..
drwxrwxrwt 1 root root 4096 2013-04-05 08:03 .ICE-unix
drwxrwxrwt 1 root root 4096 2013-04-05 08:03 .X11-unix
```

---

### `ls /var/log` — deterministic

- output mismatch

**Expected:**
```
alternatives.log
apt
bootstrap.log
btmp
cloud-init.log
cloud-init-output.log
dpkg.log
journal
lastlog
private
README
runit
wtmp
wtmp.db
```

**Got:**
```
alternatives.log apt              aptitude         auth.log         
btmp             daemon.log       debug            dmesg            
dmesg.0          dpkg.log         faillog          fsck             
installer        kern.log         lastlog          lpr.log          
mail.err         mail.info        mail.log         mail.warn        
messages         news             syslog           user... [+32B]```

---

### `ls /etc` — deterministic

- output mismatch

**Expected:**
```
adduser.conf
alternatives
apparmor
apparmor.d
apt
avahi
bash.bashrc
bash_completion
bash_completion.d
bindresvport.blacklist
binfmt.d
bluetooth
ca-certificates
ca-certificates.conf
chatscripts
cifs-utils
cloud
console-setup
credstore
credstore.encrypted
cron.d
cron.daily
cron.hourly
cron.monthly
crontab
cron.weekly
cron.yearly
dbus-1
dconf
debconf.conf
debian_version
debuginfod
default
deluser.con... [+1236B]```

**Got:**
```
X11                       acpi                      adduser.conf              
alternatives              apt                       bash.bashrc               
bash_completion.d         bindresvport.blacklist    blkid.tab                 
blkid.tab.old             calendar                  console-setup             
cron.d                    cron.daily                cron.hourly               
cron.... [+3129B]```

---

### `cat /etc/passwd` — deterministic

- output mismatch

**Expected:**
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool... [+999B]```

**Got:**
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/sh
bin:x:2:2:bin:/bin:/bin/sh
sys:x:3:3:sys:/dev:/bin/sh
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/bin/sh
man:x:6:12:man:/var/cache/man:/bin/sh
lp:x:7:7:lp:/var/spool/lpd:/bin/sh
mail:x:8:8:mail:/var/mail:/bin/sh
news:x:9:9:news:/var/spool/news:/bin/sh
uucp:x:10:10:uucp:/var/spool/uucp:/bin/sh
proxy:x:13:13:... [+468B]```

---

### `cat /etc/group` — deterministic

- output mismatch

**Expected:**
```
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:pi
tty:x:5:
disk:x:6:
lp:x:7:
mail:x:8:
news:x:9:
uucp:x:10:
man:x:12:
proxy:x:13:
kmem:x:15:
dialout:x:20:pi
fax:x:21:
voice:x:22:
cdrom:x:24:pi
floppy:x:25:
tape:x:26:
sudo:x:27:pi
audio:x:29:pi
dip:x:30:
www-data:x:33:
backup:x:34:
operator:x:37:
list:x:38:
irc:x:39:
src:x:40:
shadow:x:42:
utmp:x:43:
video:x:44:pi
sasl:x:45:
plugdev:x:46:pi
staff:... [+345B]```

**Got:**
```
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:
tty:x:5:
disk:x:6:
lp:x:7:
mail:x:8:
news:x:9:
uucp:x:10:
man:x:12:
proxy:x:13:
kmem:x:15:
dialout:x:20:
fax:x:21:
voice:x:22:
cdrom:x:24:phil
floppy:x:25:phil
tape:x:26:
sudo:x:27:
audio:x:29:phil
dip:x:30:phil
www-data:x:33:
backup:x:34:
operator:x:37:
list:x:38:
irc:x:39:
src:x:40:
gnats:x:41:
shadow:x:42:
utmp:x:43:
video:x:44:phil
sasl:x:45:
pl... [+138B]```

---

### `cat /etc/hosts` — deterministic

- output mismatch

**Expected:**
```
# Your system has configured 'manage_etc_hosts' as True.
# As a result, if you wish for changes to this file to persist
# then you will need to either
# a.) make changes to the master file in /etc/cloud/templates/hosts.debian.tmpl
# b.) change or remove the value of 'manage_etc_hosts' in
#     /etc/cloud/cloud.cfg or cloud-config from user-data
#
127.0.1.1 raspberrypi raspberrypi
127.0.0.1 localho... [+149B]```

**Got:**
```
127.0.0.1	localhost
127.0.1.1	nas3

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

---

### `cat /etc/resolv.conf` — deterministic

- output mismatch

**Expected:**
```
# Generated by NetworkManager
nameserver 1.1.1.1
nameserver 8.8.8.8
```

**Got:**
```
nameserver 8.8.8.8
nameserver 8.8.4.4
```

---

### `cat /etc/shadow` — deterministic

- output mismatch

**Expected:**
```
cat: /etc/shadow: Permission denied
```

**Got:**
```
root:$6$4aOmWdpJ$/kyPOik9rR0kSLyABIYNXgg/UqlWX3c1eIaovOLWphShTGXmuUAMq6iu9DrcQqlVUw3Pirizns4u27w3Ugvb6.:15800:0:99999:7:::
daemon:*:15800:0:99999:7:::
bin:*:15800:0:99999:7:::
sys:*:15800:0:99999:7:::
sync:*:15800:0:99999:7:::
games:*:15800:0:99999:7:::
man:*:15800:0:99999:7:::
lp:*:15800:0:99999:7:::
mail:*:15800:0:99999:7:::
news:*:15800:0:99999:7:::
uucp:*:15800:0:99999:7:::
proxy:*:15800:0:999... [+350B]```

---

### `stat /etc/passwd` — deterministic

- output mismatch

**Expected:**
```
  File: /etc/passwd
  Size: 1399      	Blocks: 8          IO Block: 4096   regular file
Device: 179,2	Inode: 32353       Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2026-04-12 20:13:39.206010996 -0400
Modify: 2026-04-12 20:13:39.206010996 -0400
Change: 2026-04-12 20:13:39.214010996 -0400
 Birth: 2026-04-12 20:13:39.206010996 -0400
```

**Got:**
```
-bash: /usr/bin/stat: cannot execute binary file: Exec format error
```

---

### `stat /root` — deterministic

- output mismatch

**Expected:**
```
  File: /root
  Size: 4096      	Blocks: 8          IO Block: 4096   directory
Device: 179,2	Inode: 25          Links: 3
Access: (0700/drwx------)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2026-04-12 20:13:33.405015589 -0400
Modify: 2026-04-12 20:04:55.241557368 -0400
Change: 2026-04-12 20:12:20.241663720 -0400
 Birth: 2026-04-12 20:12:20.089662988 -0400
```

**Got:**
```
-bash: /usr/bin/stat: cannot execute binary file: Exec format error
```

---

### `ip a` — deterministic

- output mismatch

**Expected:**
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DO... [+476B]```

**Got:**
```
-bash: /sbin/ip: cannot execute binary file: Exec format error
```

---

### `ip addr show` — deterministic

- output mismatch

**Expected:**
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DO... [+476B]```

**Got:**
```
-bash: /sbin/ip: cannot execute binary file: Exec format error
```

---

### `ip route` — deterministic

- output mismatch

**Expected:**
```
default via 10.4.27.1 dev wlan0 proto dhcp src 10.4.27.33 metric 600 
10.4.27.0/24 dev wlan0 proto kernel scope link src 10.4.27.33 metric 600 
```

**Got:**
```
-bash: /sbin/ip: cannot execute binary file: Exec format error
```

---

### `ip link` — deterministic

- output mismatch

**Expected:**
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN mode DEFAULT group default qlen 1000
    link/ether 88:a2:9e:1d:74:e9 brd ff:ff:ff:ff:ff:ff
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_cod... [+104B]```

**Got:**
```
-bash: /sbin/ip: cannot execute binary file: Exec format error
```

---

### `arp -a` — deterministic

- output mismatch

**Expected:**
```
bash: line 1: arp: command not found
```

**Got:**
```
-bash: /usr/sbin/arp: cannot execute binary file: Exec format error
```

---

### `ss -tulpn` — deterministic

- output mismatch

**Expected:**
```
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
udp   UNCONN 0      0            0.0.0.0:52553      0.0.0.0:*          
udp   UNCONN 0      0            0.0.0.0:5353       0.0.0.0:*          
udp   UNCONN 0      0                  *:52245            *:*          
udp   UNCONN 0      0                  *:5353             *:*          
tcp   LISTEN 0      128        127.0.0.1... [+248B]```

**Got:**
```
-bash: /bin/ss: cannot execute binary file: Exec format error
```

---

### `netstat -tulpn` — deterministic

- output mismatch

**Expected:**
```
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:6010          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 ::1:6010                :::*      ... [+552B](Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
```

**Got:**
```
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 *:ssh                   *:*                     LISTEN
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN
Active UNIX domain sockets (only servers)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  2      [ ACC ]     STR... [+301B]```

---

### `hostname -I` — deterministic

- output mismatch

**Expected:**
```
10.4.27.33 
```

**Got:**
```
```

---

### `ls -la /etc/cron.d` — deterministic

- output mismatch

**Expected:**
```
total 16
drwxr-xr-x  2 root root 4096 Apr 12 20:05 .
drwxr-xr-x 95 root root 4096 Apr 23 10:36 ..
-rw-r--r--  1 root root  188 Mar  9 18:53 e2scrub_all
-rw-r--r--  1 root root  102 Jun 13  2025 .placeholder
```

**Got:**
```
drwxr-xr-x 1 root root 4096 2013-04-05 07:52 .
drwxr-xr-x 1 root root 4096 2013-04-05 08:06 ..
-rw-r--r-- 1 root root  102 2013-04-05 07:52 .placeholder
```

---

### `ls -la /etc/crontab` — deterministic

- output mismatch

**Expected:**
```
-rw-r--r-- 1 root root 1042 Jun 13  2025 /etc/crontab
```

**Got:**
```
-rw-r--r-- 1 root root 722 2013-04-05 07:52 /etc/crontab
```

---

### `ls -la /etc/cron.daily` — deterministic

- output mismatch

**Expected:**
```
total 28
drwxr-xr-x  2 root root 4096 Apr 12 20:07 .
drwxr-xr-x 95 root root 4096 Apr 23 10:36 ..
-rwxr-xr-x  1 root root 1478 Jun 24  2025 apt-compat
-rwxr-xr-x  1 root root  123 Dec 15 19:50 dpkg
-rwxr-xr-x  1 root root  377 Apr  7  2025 logrotate
-rwxr-xr-x  1 root root 1395 May  2  2025 man-db
-rw-r--r--  1 root root  102 Jun 13  2025 .placeholder
```

**Got:**
```
drwxr-xr-x 1 root root  4096 2013-04-05 08:01 .
drwxr-xr-x 1 root root  4096 2013-04-05 08:06 ..
-rw-r--r-- 1 root root   102 2013-04-05 07:52 .placeholder
-rwxr-xr-x 1 root root 14985 2013-04-05 07:52 apt
-rwxr-xr-x 1 root root   314 2013-04-05 07:52 aptitude
-rwxr-xr-x 1 root root   355 2013-04-05 07:52 bsdmainutils
-rwxr-xr-x 1 root root   256 2013-04-05 07:52 dpkg
-rwxr-xr-x 1 root root    89 ... [+133B]```

---

### `crontab -l` — deterministic

- output mismatch

**Expected:**
```
no crontab for pi
```

**Got:**
```
no crontab for root
```

---

### `systemctl list-units --type=service --no-pager` — deterministic

- output mismatch

**Expected:**
```
  UNIT                                                        LOAD   ACTIVE SUB     DESCRIPTION
  alsa-restore.service                                        loaded active exited  Save/Restore Sound Card State
  avahi-daemon.service                                        loaded active running Avahi mDNS/DNS-SD Stack
  bluetooth.service                                           loaded active runnin... [+4833B]```

**Got:**
```
-bash: systemctl: command not found
```

---

### `systemctl list-timers --no-pager` — deterministic

- output mismatch

**Expected:**
```
NEXT                            LEFT LAST                              PASSED UNIT                         ACTIVATES
Thu 2026-04-23 14:04:27 EDT 2h 37min Wed 2026-04-22 22:22:00 EDT      13h ago apt-daily.timer              apt-daily.service
Thu 2026-04-23 16:06:05 EDT 4h 39min Wed 2026-04-22 16:06:05 EDT      19h ago systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Thu 2026-04-23 18:51... [+942B]```

**Got:**
```
-bash: systemctl: command not found
```

---

### `ls /etc/systemd/system/` — deterministic

- output mismatch

**Expected:**
```
bluetooth.target.wants
cloud-config.target.wants
cloud-init.target.wants
dbus-fi.w1.wpa_supplicant1.service
dbus-org.bluez.service
dbus-org.freedesktop.Avahi.service
dbus-org.freedesktop.nm-dispatcher.service
dbus-org.freedesktop.timesync1.service
default.target
getty.target.wants
graphical.target.wants
multi-user.target.wants
network-online.target.wants
sockets.target.wants
sshd.service
sshd.serv... [+125B]```

**Got:**
```
multi-user.target.wants sockets.target.wants    syslog.service          
```

---

### `cat /etc/rc.local` — deterministic

- output mismatch

**Expected:**
```
cat: /etc/rc.local: No such file or directory
```

**Got:**
```
ELF          >    x @     @       �           @ 8  @                   @       @     y       y               � .shstrtab .text                                                                                    x @     x                                                           y                                     
```

---

### `dpkg -l` — deterministic

- output mismatch

**Expected:**
```
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                                 Version                              Architecture Description
+++-====================================-====================================-============-==========================... [+86943B]```

**Got:**
```
-bash: /usr/bin/dpkg: cannot execute binary file: Exec format error
```

---

### `which python3` — deterministic

- output mismatch

**Expected:**
```
/usr/bin/python3
```

**Got:**
```
```

---

### `which nc` — deterministic

- output mismatch

**Expected:**
```
/usr/bin/nc
```

**Got:**
```
/bin/nc
```

---

### `which strace` — deterministic

- output mismatch

**Expected:**
```
/usr/bin/strace
```

**Got:**
```
```

---

### `command -v bash` — deterministic

- output mismatch

**Expected:**
```
/usr/bin/bash
```

**Got:**
```
-bash: command: command not found
```

---

### `bash --version` — deterministic

- output mismatch

**Expected:**
```
GNU bash, version 5.2.37(1)-release (aarch64-unknown-linux-gnu)
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

**Got:**
```
```

---

### `ls /etc/ssh/` — deterministic

- output mismatch

**Expected:**
```
moduli
ssh_config
ssh_config.d
sshd_config
sshd_config.d
ssh_host_ecdsa_key
ssh_host_ecdsa_key.pub
ssh_host_ed25519_key
ssh_host_ed25519_key.pub
ssh_host_rsa_key
ssh_host_rsa_key.pub
ssh_import_id
```

**Got:**
```
moduli                 ssh_config             ssh_host_dsa_key       
ssh_host_dsa_key.pub   ssh_host_ecdsa_key     ssh_host_ecdsa_key.pub 
ssh_host_rsa_key       ssh_host_rsa_key.pub   sshd_config            
```

---

### `cat /etc/ssh/sshd_config` — deterministic

- output mismatch

**Expected:**
```

# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.

# This sshd was compiled with PATH=/usr/local/bin:/usr/bin:/bin:/usr/games

# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented.  Uncommented options override the
# default val... [+3024B]```

**Got:**
```
```

---

### `nmap` — deterministic

- output mismatch

**Expected:**
```
bash: line 1: nmap: command not found
```

**Got:**
```
-bash: nmap: command not found
```

---

### `ncat` — deterministic

- output mismatch

**Expected:**
```
bash: line 1: ncat: command not found
```

**Got:**
```
-bash: ncat: command not found
```

---

### `nonexistentcmd12345` — deterministic

- output mismatch

**Expected:**
```
bash: line 1: nonexistentcmd12345: command not found
```

**Got:**
```
-bash: nonexistentcmd12345: command not found
```

---

### `cat /root/nothere` — deterministic

- output mismatch

**Expected:**
```
cat: /root/nothere: Permission denied
```

**Got:**
```
cat: /root/nothere: No such file or directory
```

---

### `ls /nothere` — deterministic

- output mismatch

**Expected:**
```
ls: cannot access '/nothere': No such file or directory
```

**Got:**
```
ls: cannot access /nothere: No such file or directory
```

---

### `cd /nothere` — deterministic

- output mismatch

**Expected:**
```
bash: line 1: cd: /nothere: No such file or directory
```

**Got:**
```
bash: cd: /nothere: No such file or directory
```

---

### `file /bin/bash` — deterministic

- output mismatch

**Expected:**
```
/bin/bash: ELF 64-bit LSB pie executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, BuildID[sha1]=bea6a154d9a9158114ee0a2a439045596615df14, for GNU/Linux 3.7.0, stripped
```

**Got:**
```
-bash: /usr/bin/file: cannot execute binary file: Exec format error
```

---

### `readlink -f /bin/sh` — deterministic

- output mismatch

**Expected:**
```
/usr/bin/dash
```

**Got:**
```
-bash: /bin/readlink: cannot execute binary file: Exec format error
```

---

### `find / -perm -4000 -type f 2>/dev/null` — deterministic

- output mismatch

**Expected:**
```
/usr/lib/polkit-1/polkit-agent-helper-1
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/sbin/pppd
/usr/sbin/mount.cifs
/usr/bin/chfn
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/ntfs-3g
/usr/bin/gpasswd
/usr/bin/su
/usr/bin/mount
/usr/bin/newgrp
/usr/bin/sudo
/usr/bin/umount
/usr/bin/fusermount3
```

**Got:**
```
```

---

### `find / -writable -type d 2>/dev/null` — deterministic

- output mismatch

**Expected:**
```
/var/tmp
/tmp
/tmp/.font-unix
/tmp/.XIM-unix
/tmp/.ICE-unix
/tmp/.X11-unix
/dev/mqueue
/dev/shm
/run/user/1000
/run/user/1000/dbus-1
/run/user/1000/dbus-1/services
/run/user/1000/gnupg
/run/user/1000/systemd
/run/user/1000/systemd/generator.late
/run/user/1000/systemd/generator.late/xdg-desktop-autostart.target.wants
/run/user/1000/systemd/units
/run/user/1000/systemd/propagate
/run/user/1000/syst... [+2553B]```

**Got:**
```
```

---

### `grep -r password /etc 2>/dev/null` — deterministic

- output mismatch

**Expected:**
```
/etc/profile.d/sshpwd.sh:	echo $"SSH is enabled and the default password for the 'pi' user has not been changed."
/etc/profile.d/sshpwd.sh:	echo $"This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password."
/etc/ssh/sshd_config:#PermitRootLogin prohibit-password
/etc/ssh/sshd_config:# To disable tunneled clear text passwords, change to "no" here!
/etc/ssh/sshd... [+4683B]```

**Got:**
```
usage: grep [-abcDEFGHhIiJLlmnOoPqRSsUVvwxZ] [-A num] [-B num] [-C[num]]
	[-e pattern] [-f file] [--binary-files=value] [--color=when]
	[--context[=num]] [--directories=action] [--label] [--line-buffered]
	[--null] [pattern] [file ...]
```

---

### `apt list --installed 2>/dev/null` — deterministic

- output mismatch

**Expected:**
```
Listing...
7zip/stable,now 25.01+dfsg-1~deb13u1 arm64 [installed,automatic]
adduser/stable,stable,now 3.152 all [installed]
alsa-topology-conf/stable,stable,now 1.2.5.1-3 all [installed,automatic]
alsa-ucm-conf/stable,stable,now 1.2.14-1 all [installed,automatic]
alsa-utils/stable,now 1.2.14-1+rpt1 arm64 [installed,automatic]
apparmor/stable,now 4.1.0-1 arm64 [installed,automatic]
apt-listchanges/... [+39044B]```

**Got:**
```
```

---

### `du -sh /home/*` — deterministic

- output mismatch

**Expected:**
```
44K	/home/pi
```

**Got:**
```
28K     .
```

---

