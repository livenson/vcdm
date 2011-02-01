#!/bin/bash
export PYTHONPATH="lib:src:$PYTHONPATH"
python src/vcdm/server/fuse/cloudfs.py $1
