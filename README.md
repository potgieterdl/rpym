rpym is the Raspberry Python Monitoring tool

It can log data via small python scripts to your statsd server.

See details from original fork [blog](http://blog.abarbanell.de/raspberry/2015/07/18/Raspberry-Pi-Monitoring-With-Statsd/)

script mon.py: to capture system related data like cpu usage, disk usage, and cpu temperature. The first ones work on any Linux like system, the CPU temperature only on a Raspberry Pi.

### Setup : NOTE *** This will install under /opt/rpimonitor and install the systemd unit
```
git clone https://github.com/potgieterdl/rpym
cd rpym
./setup.sh
```
once completed, you should be able to call the below and have expected output to match
```
$ systemctl status rpimonitor.service
● rpimonitor.service - Raspberry PI stats monitor
   Loaded: loaded (/root/rpym/rpimonitor.service; linked)
   Active: inactive (dead)

Oct 14 19:02:36 rpi-builder systemd[1]: rpimonitor.service: main process exited, code=exited, status=200/CHDIR
Oct 14 19:02:36 rpi-builder systemd[1]: Unit rpimonitor.service entered failed state.
Oct 14 19:06:06 rpi-builder systemd[1]: Starting Raspberry PI stats monitor...
Oct 14 19:06:06 rpi-builder systemd[1]: Started Raspberry PI stats monitor.

```



