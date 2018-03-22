#!/usr/bin/env bash

apt-get update

apt install libcairo2-dev
apt-get install libgirepository1.0-dev

virtualenv -p python3.6 venv
source venv/bin/activate

python -m pip install -r requirements.txt
