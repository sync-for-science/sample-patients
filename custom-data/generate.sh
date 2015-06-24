#!/bin/bash
set -e

for f in ./raw/*;
    do
        if [[ -d $f  ]]; then
	    cd $f;
	    python to-fhir.py > ../../${f##*/}.json;
	    cd - ;
	fi;
    done;
