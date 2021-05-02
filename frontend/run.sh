#!/usr/bin/env bash

NAME="data-companion-frontend"

eval "$(/home/rajat/miniconda3/bin/conda shell.bash hook)"
conda activate rajat

echo "Starting $NAME as `whoami`"

cd /home/rajat/repos/data-companion/frontend
yarn run build
yarn serve -s -l 3000 build
