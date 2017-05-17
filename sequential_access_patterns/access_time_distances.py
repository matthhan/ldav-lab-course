#!/usr/bin/python3

import datetime as dt
import functools as ft

class Action:
    def __init__(self,url,time,event):
        self.time = time
        self.event = event
        self.url = url


byuser = dict()
for line in open("./accesses.csv"):
    parts = line.split(",")
    if(parts[0] == "user"):
        continue
    if not parts[0] in byuser:
        byuser[parts[0]] = list()

    date_format = "%Y-%m-%dT%H:%M:%S"
    time = dt.datetime.strptime(parts[1],date_format)
    event = parts[2]
    url = ft.reduce(lambda a,b: a+b,parts[3:])

    byuser[parts[0]].append(Action(url,time,event))

def timestodifferences(listofaction):
    newlis = list()
    for i in range(0,len(listofaction)-1):
        newlis.append((listofaction[i+1].time - listofaction[i].time).seconds)
        #if((listofaction[i+1].time - listofaction[i].time).seconds == 0):
            #print("a" + str(listofaction[i+1].time))
            #print("b" + str(listofaction[i].time))
    return newlis

def flatten(lisoflist):
    res = list()
    for sublis in lisoflist:
        res.extend(sublis)
    return res

for actions in byuser.values():
    actions.sort(key=lambda action:action.time)

timedifferences = flatten([timestodifferences(x) for x in byuser.values()])


resultfile = open('res.csv','w')
for item in timedifferences:
    resultfile.write(str(item) + '\n')
