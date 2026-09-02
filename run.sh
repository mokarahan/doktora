source $HOME/.venv/bin/activate
PROJECT_HOME=$HOME/Dev/doktora

python3 $PROJECT_HOME/src/load_csv.py --filename $PROJECT_HOME/src/metadata.csv --data_dir $PROJECT_HOME/src/tmp --no-show_figures --no-generate_logs
