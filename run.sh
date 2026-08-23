source /Users/mokarahan/path/to/venv/bin/activate
FILE_NAME=ReadModelData.py

if [[ $# -eq 1 ]]; 
then
  FILE_NAME=$1
fi

python3 $FILE_NAME

