# ansible role for monitoring plugins

installs an set of `monitoring-` or `nagios-plugins`


## debian based

```
monitoring_plugins_debian:
  - monitoring-plugins-standard
  - monitoring-plugins-basic
  - monitoring-plugins-common
```

## redhat based

```
monitoring_plugins_redhat:
  - nagios-plugins
  - nagios-plugins-disk
  - nagios-plugins-dns
  - nagios-plugins-file_age
  - nagios-plugins-fping
  - nagios-plugins-http
  - nagios-plugins-icmp
  - nagios-plugins-ldap
  - nagios-plugins-load
  - nagios-plugins-mailq
  - nagios-plugins-mysql
  - nagios-plugins-ntp
  - nagios-plugins-ping
  - nagios-plugins-procs
  - nagios-plugins-sensors
  - nagios-plugins-smtp
  - nagios-plugins-snmp
  - nagios-plugins-ssh
  - nagios-plugins-swap
  - nagios-plugins-tcp
  - nagios-plugins-time
  - nagios-plugins-uptime
  - nagios-plugins-users
```

### monitoring_plugins_blacklist

remove blugins from list.

`nagios-plugins-mysql` and MariaDB from epel are not compatible in CentoOS 8. (see https://github.com/Icinga/icinga2/issues/7927)

Here you can remove modules from the site if necessary. 

```
monitoring_plugins_blacklist:
  - nagios-plugins-mysql
```

### extra plugins

```
monitoring_plugins_extra:
  - restart_service
  - check_hostname
  - check_diskstat.sh
  - check_uptime.sh
  - check_mem
  - check_requiered_reboot.sh
```

### download external plugins

```
monitoring_plugins_download:
  - url: 'https://gitlab.com/coremedia-as-code/monitoring/monitoring-plugins/raw/master/icinga2/check_coremedia_licenses.py'
    dest: 'check_coremedia_licenses.py'
    checksum: ''
    validate: false
  - url: 'https://raw.githubusercontent.com/bodsch/check_arch_updates/1.0/check_arch_updates'
    dest: 'check_arch_updates'
    checksum: 'sha256:7afa562aaedb63f6e93cfebfa4a9a3ea49fecda62d4dae3d8ff919b76c117c41'
```
