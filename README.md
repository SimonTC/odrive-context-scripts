# Odrive scripts
A collection of Python scripts to use with the Odrive CLI Agent.

# Installing odrive and setting up the scripts.
Original installation instructions can be found [here]. (https://forum.odrive.com/t/odrive-sync-agent-a-cli-scriptable-interface-for-odrives-progressive-sync-engine-for-linux-os-x-and-windows)
If odrive already is installed and working you can jump directly to step 8. 
### 1. Install the odrive sync agent
Run the following command in your terminal to download and install the odrive Sync Agent to `~/.odrive-agent`. This will download the odrive Agent service, the odrive Agent python client, and the odrive Agent binary client.
#### Linux - 32-bit
`od="$HOME/.odrive-agent/bin" && curl -L "https://dl.odrive.com/odrive-py" --create-dirs -o "$od/odrive.py" && curl -L "https://dl.odrive.com/odriveagent-lnx-32" | tar -xvzf- -C "$od/" && curl -L "https://dl.odrive.com/odrivecli-lnx-32" | tar -xvzf- -C "$od/"`

#### Linux - 64-bit
`od="$HOME/.odrive-agent/bin" && curl -L "http://dl.odrive.com/odrive-py" --create-dirs -o "$od/odrive.py" && curl -L "http://dl.odrive.com/odriveagent-lnx-64" | tar -xvzf- -C "$od/" && curl -L "http://dl.odrive.com/odrivecli-lnx-64" | tar -xvzf- -C "$od/"`

### 2. Create alias for the agent
Add the following line to your `~/.bashrc` file:
`alias odrive='python "$HOME/.odrive-agent/bin/odrive.py"'`

### 3. Create an odrive account 
Got to https://www.odrive.com/ and register
### 4. Create an auth key for the odrive Agent
Go to https://www.odrive.com/account/authcodes and click on "Create Auth Key" to create an auth key.
### 5. Authenticate the agent
Execute the following in your terminal where `[auth key]` is the key you got in step 4:
`odrive authenticate [auth key]`

### 6. Start server
To run the odrive Sync Agent server in the background, use the following command in your terminal:
`nohup "$HOME/.odrive-agent/bin/odriveagent">/dev/null&`

### 7. Setup server to start at reboot
Add the following line to you cron tab (crontab -e)
`@reboot ~/.odrive-agent/bin/odriveagent &`

### 8. Add scripts to context menu
Read more about Nautilus scripts [here] (https://help.ubuntu.com/community/NautilusScriptsHowto)
1. copy odrive_scripts.py to the odrive installation folder (`~/.odrive-agent`)
2. copy the odrive folder to `~/.local/share/nautilus/scripts/`
3. make all the scripts executable by either right-clicking each script and select 'Properties → Permissions → Allow executing file as program' or use the following command in the terminal:
  `chmod +x <name-of-script>`
4. You might need to open the scripts folder before the scripts become active as part of the context menu

# Logging
Currently a very basic logging feature is implemented where the output of a script is written to `"$HOME/.odrive-agent/log/scripts.log`
The log is overwritten each time a script is called and it does not capture all errors such as trying to unsync a folder when the user is not a premium user or when using one of the scripts on a file/folder that is not inside an odrive mount.
