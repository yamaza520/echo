# echo
For controlling local devices with the Amazon Echo.

Instructions for installation and usage [available on Instructables here](http://www.instructables.com/id/Hacking-the-Amazon-Echo/)

Brought to you by [FabricateIO](http://fabricate.io)

## Quick Start

1. Create a [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
2. git clone *this_repo*
3. cd *this_repo*
4. pip install -r requirements.txt
4. python example-minimal.py
6. Tell Echo, "discover my devices"
7. Use Echo's "turn off device" and "device on" to see True/False script output

## custmize

use https://github.com/netbuffalo/irmcli

```
sudo python irmcli.py -c
sudo python irmcli.py -s -f light_on.json
sudo python irmcli.py -p -f light_on.json
```

## initd

```
cd /usr/local/src
sudo chown root.root echo.sh
sudo chmod 755 echo.sh
sudo cp echo.sh /etc/init.d/

sudo chmod 755 home.py

sudo /etc/init.d/echo.sh start
sudo /etc/init.d/echo.sh status
sudo /etc/init.d/echo.sh stop
```
