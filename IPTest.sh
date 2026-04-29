# Source - https://stackoverflow.com/a/14741910
# Posted by Anton Boritskiy
# Retrieved 2026-04-28, License - CC BY-SA 3.0

echo "Hostname: $HOSTNAME"
echo "--IP information--"
ifconfig -a
echo "--Linux Version: `uname -r`"
netstat
