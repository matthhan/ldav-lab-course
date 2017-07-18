#!/bin/sh

mkdir base_data;
cd data_extraction;
./download_everything.py $LDAVLAB_UN $LDAVLAB_PW;
cd ..;

cd sequential_access_patterns;
./do_everything.sh;
cd ..;
mv sequential_access_patterns/data.json vis/src/sequential_access_patterns/data.json;


cd time_to_view;
./do_everything.sh;
cd ..;
mv time_to_view/data.json vis/src/time_to_view/data.json;


cd timespent;
./do_everything.sh;
cd ..;
mv timespent/data.json vis/src/timespent/data.json;

cd vis;
./do_everything.sh;
cd ..;

