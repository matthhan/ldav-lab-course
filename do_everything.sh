#!/bin/sh

mkdir base_data;
cd data_extraction;
#./download_everything.py $LDAVLAB_UN $LDAVLAB_PW;
cd ..;

cd sequential_access_patterns;
./do_everything.sh;
cd ..;
