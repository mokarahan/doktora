#!/bin/bash

OS_TYPE=$(uname -s)

case "$OS_TYPE" in
    Linux*)
        echo "Running on Linux"
        PROJECT_HOME=$HOME/Dev/doktora
        source $HOME/.venv/bin/activate
        python3 $PROJECT_HOME/src/load_csv.py --filename $PROJECT_HOME/src/metadata.csv --data_dir $PROJECT_HOME/src/tmp --no-show_figures --no-generate_logs $1
        ;;
    Darwin*)
        echo "Running on macOS"
        # Insert Mac-specific commands here
        ;;
    *)
        echo "Unknown Operating System: $OS_TYPE"
        ;;
esac


