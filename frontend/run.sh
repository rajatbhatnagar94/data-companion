#!/usr/bin/env bash

NAME="toxicity-frontend"

# Activate the virtual environment
export PATH="/data/anaconda3/bin:$PATH"
. /data/anaconda3/etc/profile.d/conda.sh
conda activate rajat-ml-frontend

echo "Starting $NAME as `whoami`"

cd /home/rajat/repos/explanable-ml-frontend
yarn run build
/home/rajat/.yarn/bin/serve -s -l 3000 build
