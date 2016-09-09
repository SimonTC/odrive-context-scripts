# Installation
Source: https://forum.odrive.com/t/odrive-sync-agent-a-cli-scriptable-interface-for-odrives-progressive-sync-engine-for-linux-os-x-and-windows/499?u=simon.clement

## Linux - 64-bit
Run the following command in your terminal to download and install the odrive Sync Agent to ~/.odrive-agent. This will download the odrive Agent service, the odrive Agent python client, and the odrive Agent binary client.
od="$HOME/.odrive-agent/bin" && curl -L "http://dl.odrive.com/odrive-py" --create-dirs -o "$od/odrive.py" && curl -L "http://dl.odrive.com/odriveagent-lnx-64" | tar -xvzf- -C "$od/" && curl -L "http://dl.odrive.com/odrivecli-lnx-64" | tar -xvzf- -C "$od/"

## Run server
To run the odrive Sync Agent server in the background, use the following command in your terminal:
nohup "$HOME/.odrive-agent/bin/odriveagent">/dev/null&


## Start server at reboot
Add the following line to you cron tab (crontab -e)
@reboot ~/.odrive-agent/bin/odriveagent &

## Make it easier to give commands
Add the following line to your ~/.bashrc file:
alias odrive='python "$HOME/.odrive-agent/bin/odrive.py"'

## Install odrive.py as a module to be used by the scripts


## Add right click commands
Source: https://help.ubuntu.com/community/NautilusScriptsHowto
Copy any of the scripts in the script folder to ~/.local/share/nautilus/scripts/
Make them  executable by running the command
chmod +x name-of-script
You might need to open the folder before the become active as part of the right menu
