#!/bin/bash

# Reinstall nfstream from local source code
cd /Users/ppopiolek/Documents/NFCache/nfstream
pip install -e .

# run listerner.py
python /Users/ppopiolek/Documents/NFCache/nfstream/tests/scripts/listener.py

