#!/bin/bash
for lib in `ls libsrc`; do
    if [ -e libsrc/$lib/src ]; then 
        PYTHONPATH=libsrc/${lib}/src:$PYTHONPATH
    else
        PYTHONPATH=libsrc/${lib}:$PYTHONPATH
    fi
done
PYTHONPATH=src:$PYTHONPATH
export PYTHONPATH

python src/vcdm/daemon.py
