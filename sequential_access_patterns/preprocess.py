#!/usr/bin/python

import datetime as dt

class Action:
    def __init__(self,url,time,event):
        self.time = time
        self.event = event
        self.url = url


byuser = dict()
for line in file("./accesses.csv"):
    parts = line.split(",")
    if(parts[0] == "user"):
        continue
    if not parts[0] in byuser:
        byuser[parts[0]] = list()

    date_format = "%Y-%m-%dT%H:%M:%S"
    time = dt.datetime.strptime(parts[1],date_format)
    event = parts[2]
    url = reduce(lambda a,b: a+b,parts[3:])

    byuser[parts[0]].append(Action(time,event,url))


for actions in byuser.values():
    actions.sort(key=lambda action:action.time)
