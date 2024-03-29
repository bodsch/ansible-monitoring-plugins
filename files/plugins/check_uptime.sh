#!/usr/bin/env bash
#
#
# USAGE :
# ./check_uptime.sh [Warning] [Critical]
#
# warning : number of days before warning
# critical : number of days before critical
#
# example :
# ./check_uptime.sh 365 730

# exit codes
E_OK=0
E_WARNING=1
E_CRITICAL=2
E_UNKNOWN=3

usage() {
  echo "This plugin check if the uptime is less than warning and critical"
  echo "Example: "
  echo "    $0 -c 10 -w 5"
  echo ""
}

while [ -n "$1" ]
do
  case $1 in
    -h|--help)
      usage
      exit "${E_UNKNOWN}"
      ;;
    -w|--warning)
      shift
      warning=${1}
      ;;
    -c|--critical)
      shift
      critical=${1}
      ;;
    *)
      unknown "invalid option: ${1}"
      ;;
  esac
  shift
done


if [ "$(uptime | grep -c day)" -eq 0 ]
then
  sortie=0
else
  sortie=$(uptime | awk '{print $3}')
fi

if [ "$(echo "${sortie}" | grep '^[[:digit:]]*$')" ]
then

  [ -z "${warning}" ]  && WARNING=$(("${sortie}"+1))  || WARNING=${warning}
  [ -z "${critical}" ] && CRITICAL=$(("${sortie}"+2)) || CRITICAL=${critical}

  if [ "${sortie}" -ge "${CRITICAL}" ]
  then
    echo "CRITICAL: you must reboot - Uptime: $(uptime --pretty)"
    exit "${E_CRITICAL}"
  elif [ "${sortie}" -ge "${WARNING}" ]
  then
    echo "WARNING: you should reboot - Uptime: $(uptime --pretty)"
    exit "${E_WARNING}"
  elif [ "${sortie}" -lt "${CRITICAL}" ]
  then
    echo "Uptime: $(uptime --pretty)"
    exit "${E_OK}"
  else
    usage
    exit "${E_UNKNOWN}"
  fi
fi

echo "${sortie}" | tr "\n" "\t"
exit "${E_UNKNOWN}"

