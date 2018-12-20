# OpenHAB 2 Prometheus Exporter
A simple and straightforward script for exposing OpenHAB 2 items as Prometheus metrics.
Note that the steps below have been based on a Raspberry PI 2 with Raspbian installed.

## Requirements
- Python 3.5 or higher
- Gunicorn3

## Installation
Typically you'd install this script on the same server that runs OpenHAB 2.

- Install `python3` and `gunicorn3` packages. Make sure `python3` is version 3.5 or higher
  - You can check this by running `python3 --version`
- Place `openhab2-exporter.py` in a directory of choice
  - For example in `/opt/openhab2-exporter`
- Save `openhab2-exporter.service.template` as `/etc/systemd/system/openhab2-exporter.service`
  - Open the file, and update the template:
    - Change the listening port `99999` to a port of your choice
    - If you chose to place the script in a different directory described in this doc, 
	  modify the `WorkingDirectory` property accordingly
- Start the service
  - `systemctl start openhab2-exporter.service`

You can check if everything's working correctly by opening `http://servername:port`, where `servername` is the
name or ip of the server that runs the script, and `port` is the port you chose to run the service on. If all
went well you should see the raw metrics appear.

Also don't forget to add this location to your scrape targets in Prometheus!