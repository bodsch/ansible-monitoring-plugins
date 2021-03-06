

installs an set of `monitoring-` or `nagios-plugins` on various systems.


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-monitoring-plugins/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-monitoring-plugins)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-monitoring-plugins)][releases]

[ci]: https://github.com/bodsch/ansible-monitoring-plugins/actions
[issues]: https://github.com/bodsch/ansible-monitoring-plugins/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-monitoring-plugins/releases

## Requirements & Dependencies

not known

### Operating systems

Tested on

* Debian 9 / 10
* Ubuntu 18.04 / 20.04
* CentOS 7 / 8
* OracleLinux 8
* ArchLinux

## configuration

### archlinux based

```
monitoring_plugins_arch:
  - monitoring-plugins
```

### debian based

```
monitoring_plugins_debian:
  - monitoring-plugins-standard
  - monitoring-plugins-basic
  - monitoring-plugins-common
```

### redhat based

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

### remove monitoring plugins from list

`nagios-plugins-mysql` and MariaDB from epel are not compatible in CentoOS 8. ([read this issue](https://github.com/Icinga/icinga2/issues/7927))

If necessary, some of the plugins can be removed from the previously defined list:

```
monitoring_plugins_blacklist:
  - nagios-plugins-mysql
```

### extra plugins

This role provides some small monitoring plugins.
These are located in the [files](./files) directory:

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

To install external plugins from other git repositories, you can use `monitoring_plugins_download`:

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
