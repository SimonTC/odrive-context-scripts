#!/bin/bash

for file in $NAUTILUS_SCRIPT_SELECTED_FILE_PATHS; do
  if [ ${file: -6} == ".cloud" ] || [ ${file: -7} == ".cloudf" ]; then
    python "$HOME/.odrive-agent/bin/odrive.py" sync file
  fi
done
