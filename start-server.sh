#!/bin/bash
export PYTHONPATH="src:libsrc:$PYTHONPATH" 
python src/vcdm/server.py
