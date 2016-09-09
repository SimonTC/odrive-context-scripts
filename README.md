# Odrive scripts
A collection of Python scripts to use with the Odrive CLI Agent.

Introduction thread: https://forum.odrive.com/t/odrive-sync-agent-a-cli-scriptable-interface-for-odrives-progressive-sync-engine-for-linux-os-x-and-windows

# Installation
## Linux - 32-bit
od="$HOME/.odrive-agent/bin" && curl -L "https://dl.odrive.com/odrive-py" --create-dirs -o "$od/odrive.py" && curl -L "https://dl.odrive.com/odriveagent-lnx-32" | tar -xvzf- -C "$od/" && curl -L "https://dl.odrive.com/odrivecli-lnx-32" | tar -xvzf- -C "$od/"

## Linux - 64-bit
Run the following command in your terminal to download and install the odrive Sync Agent to ~/.odrive-agent. This will download the odrive Agent service, the odrive Agent python client, and the odrive Agent binary client.
od="$HOME/.odrive-agent/bin" && curl -L "http://dl.odrive.com/odrive-py" --create-dirs -o "$od/odrive.py" && curl -L "http://dl.odrive.com/odriveagent-lnx-64" | tar -xvzf- -C "$od/" && curl -L "http://dl.odrive.com/odrivecli-lnx-64" | tar -xvzf- -C "$od/"

## Run server
To run the odrive Sync Agent server in the background, use the following command in your terminal:
nohup "$HOME/.odrive-agent/bin/odriveagent">/dev/null&

## Setup server to start at reboot
Add the following line to you cron tab (crontab -e)
@reboot ~/.odrive-agent/bin/odriveagent &

## Make it easier to give commands
Add the following line to your ~/.bashrc file:
alias odrive='python "$HOME/.odrive-agent/bin/odrive.py"'
Now just use odrive <command> when issuing odrive commands

## Add context menu
Source: https://help.ubuntu.com/community/NautilusScriptsHowto
1. copy odrive_scripts.py to the odrive installation folder (~/.odrive-agent)
2. copy the scripts folder to ~/.local/share/nautilus/scripts/
3. make all the scripts executable by either right-clicking each script and select 'Properties → Permissions → Allow executing file as program' or use the following command in the terminal:
  chmod +x <name-of-script>
4. You might need to open the scripts folder before the scripts become active as part of the context menu

# Logging
Currently a very basic logging feature is implemented where the output of a script is written to "$HOME/.odrive-agent/log/scripts.log.
The log is overwritten each time a script is called and it does not capture all errors such as trying to unsync a folder when the user is not a premium user or when using one of the scripts on a file/folder that is not inside an odrive mount
