#!/bin/bash

ModifyFile="ModifyBetweenRuns.py"
RunFile="RunAlgo.py"

# Check if an argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <argument>"
    exit 1
fi

# Store the input argument
input_arg="$1"

# Check if the input argument exists as a file, if yes, use it as the RunFile
if [ -e "$input_arg" ]; then
    RunFile=$input_arg
else
    # If the input argument is not a file, default to "RunAlgo.py"
    RunFile="RunAlgo.py"
fi


python3 "$ModifyFile" $input_arg "R1"

python3 "$RunFile" "$input_arg"

python3 "$ModifyFile" $input_arg "R2"

python3 "$RunFile" "$input_arg"

python3 "$ModifyFile" $input_arg "Reset"
