#!/usr/bin/env bash

python3 -m venv venv
. venv/bin/activate
pip install -r requirements/app.txt
pip install -r requirements/tests.txt
pip install pyinstaller
pip install -e .
