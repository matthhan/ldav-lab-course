#!/bin/bash

./preprocess.py ../base_data/November.csv
cd prefixspan; sbt package; cd ..;
scala -J-Xmx6g prefixspan/target/scala-2.11/prefixspan_2.11-0.1.0.jar ./sessions.csv 100 > data.json
