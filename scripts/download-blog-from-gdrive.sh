#!/usr/bin/env bash
export FOLDER_ID="1vOWBuAlm1z3Z53cO6C4HXw7fs76shk98"
which gdown || pip install gdown
gdown "https://drive.google.com/drive/folders/$FOLDER_ID" --folder -O .
