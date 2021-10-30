# satisfactory_discord_bot

## Setup 

You will first need a satisfactory server using systemd, as in the [wiki](https://satisfactory.fandom.com/wiki/Dedicated_servers#.5BLinux.5D_SystemD), as well as a discord bot with channel write permisions, for example as following the first half of [this guide](https://realpython.com/how-to-make-a-discord-bot-python/#creating-an-application).

Install dependencies:

`python3 -m pip` or `apt install python3-pip`

`pip3 install venv`

`python3 -m venv env`

`./env/bin/activate`

`pip install -r requirements.txt`

Use the commented-out lines to find the id numbers for the token of your discord bot application, as well as your discord server, channel, and role. Put these in a .env file in the same folder as main.py. For example:

```
DISCORD_TOKEN=[token here]
SERVER_ID=[serverid here]
CHANNEL_ID=[channelid here]
ROLE_ID=[roleid here]
```

To test the app's ability to turn logs into discord messages, execute this test script, it should post a message saying "Unknown user 439304572947329445"

`python main.py "[2021.10.30-02.26.16:635][206]LogBeacon: Beacon Join FGServerBeaconClient STEAM:(STEAM)-439304572947329445"`

## Triggering the discord notifier with swatchdog

Install swatchdog on your server, more info here: https://www.tecmint.com/swatch-linux-log-file-watcher/. 

Configure swatchdog to look for the Beacon Join event in the logs, and to run main.py when it does. Create a file with the following contents at /home/myuser/.swatchdogrc

```
watchfor /Beacon Join .*/
    exec command /home/myuser/satisfactory_discord_bot/env/bin/python /home/myuser/satisfactory_discord_bot/main.py "$0"
```

You can now manually start the log watcher with `swatchdog -c /home/myuser/.swatchdogrc --daemon`, but you may wish to have it begin at startup, along with your satisfactory server.

Set up swatch also with systemd (instructions copied from [this nagios doc:](https://assets.nagios.com/downloads/nagiosxi/docs/Log-Monitoring-With-Swatch.pdf)):

Create a file at /etc/systemd/system/swatchdog.service with the following contents:

```
[Unit]
Description=Swatchdog Service
After=network-online.target

[Service]
Type=forking
Restart=on-failure
RestartSec=10
User=root
WorkingDirectory=/home/myuser/satisfactory_discord_bot
ExecStart=/usr/bin/swatchdog -c /home/myuser/.swatchdogrc --daemon

[Install]
WantedBy=multi-user.target
~                          
```

Refresh your systemd modules:
`systemctl daemon-reload` 

Enable it as a startup routine:

`systemctl enable swatchdog.service`

Start the service now:

`systemctl start swatchdog.service`

