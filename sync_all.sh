#!/bin/bash
# Source: https://forum.odrive.com/t/odrive-sync-agent-a-cli-scriptable-interface-for-odrives-progressive-sync-engine-for-linux-os-x-and-windows/499/13?
# Sync everything recursively in the folders sellected when the script was called.

for file in $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS; do
  output="go"
  while [ "$output" ]; do
    output=$(find "$file" -name "*.cloud*" -exec python "$HOME/.odrive-agent/bin/odrive.py" sync "{}" \;)
    echo $output
  done
done
