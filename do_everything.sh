#!/bin/sh

cd data_extraction;
./download_everything.py $LDAVLAB_UN $LDAVLAB_PW;
cd ..;
