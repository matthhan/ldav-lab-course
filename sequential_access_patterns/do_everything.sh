#!/bin/bash

./preprocess.py ../base_data/Jan2017.csv
cd prefixspan; sbt package; cd ..;
scala prefixspan/target/scala-2.11/prefixspan_2.11-0.1.0.jar ./sessions.csv 100 > data.json
