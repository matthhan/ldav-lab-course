#!/usr/bin/python3

#This script reads data from the database and writes file with sessions
#Each of these sessions is represented by a line in the file.
#
#Additionally, there is some preprocessing being done: Namely, all accesses that
#occur less than a second after the last one are removed as likely not human generated.
#

import datetime as dt
import functools as ft
import re as re
import sys
import urllib.parse

#Read command line params
inpfile = sys.argv[1]
sharepoint = len(sys.argv) >= 3 and sys.argv[2] == "sharepoint"
#Session timeout constant
SESSION_TIMEOUT_SECS = 10
#Only urls for which all of the filters return true are considered
filters = [
        lambda s: "SiteAssets" not in s,
        lambda s: "_catalogs" not in s,
        lambda s: "_layouts" not in s,
        lambda s: "_vti_bin" not in s,
        lambda s: "_api" not in s,
        lambda s: '?' not in s,
        lambda s: re.search(r".*/[w|s]s[0-9][0-9]/[0-9][0-9][w|s]s-[0-9]*/(.)*",s),
        lambda s: not s.endswith(".css") and not s.endswith(".js"),
        lambda s: "Preview Images" not in s,
        lambda s: not s.endswith("SitePages"),
        lambda s: not s.endswith("GWSGroupsList"),
        lambda s: not s.endswith("Announcements"),
        lambda s: not s.endswith("LA_Assignments"),
        lambda s: not s.endswith("LA_Grades"),
        lambda s: not s.endswith("DiscussionForum"),
        lambda s: not s.endswith("WikiList1"),
        lambda s: not s.endswith("Forms"),
        lambda s: not s.endswith("StructuredMaterials"),
        lambda s: not s.endswith("Hyperlinks"),
        lambda s: not s.endswith("CS_MainSurveyList"),
        lambda s: not s.endswith("Emails"),
        lambda s: not s.endswith("Video"),
        lambda s: not s.endswith(".000"),
        lambda s: not "collaboration/Freigegebene Dokumente/images" in s,
        lambda s: not len(s) > 500,
        lambda s: not re.search(r"www.[^.]*.rwth-aachen.de",s)
]

compose = lambda f,g: (lambda x: g(f(x)))
def fixpoint(f):
    def blub(x):
        inp = x
        res = f(x)
        while not (inp == res):
            inp = res
            res = f(inp)
        return res
    return blub
        
#All of the transforms are applied to urls
transforms = ft.reduce(compose,[
        lambda s: s.translate({",":None}),
        lambda s: s.replace('"',''),
        lambda s: s.strip(),
        lambda s: re.search(r".*/[w|s]s[0-9][0-9]/[0-9][0-9][w|s]s-[0-9]*/(.*)",s).group(1),
        lambda s: re.sub(r"(GWS_)([^/]*)","\\1$NAME_OF_GROUP",s),

        lambda s: re.sub(r"/S[0-9]+","/SUBMISSION_NUMBER",s),
        lambda s: re.sub(r"/A[0-9]+","/TASK_NUMBER",s),
        
        lambda s: re.sub(r"(Freigegebene Dokumente)/[^/]+/",r"\1/FOLDERNAME/",s),
        #lambda s: re.sub(r"(DiscussionForum)/.+(?!.aspx)+",r"\1/THREADNAME",s),

        lambda s: re.sub(r"(DiscussionForum/)(.)*$",r"\1THREADNAME",s),
        lambda s: re.sub(r"(WikiList1/)(.)*$",r"\1WIKI_ARTICLE_NAME",s),
        fixpoint(lambda s: re.sub(r"(StructuredMaterials/(FOLDERNAME/)*)([^/]*)/",r"\1FOLDERNAME/",s)),
        fixpoint(lambda s: re.sub(r"(SharedDocuments/(FOLDERNAME/)*)([^/]*)/",r"\1FOLDERNAME/",s)),
        fixpoint(lambda s: re.sub(r"(MediaLibrary/(FOLDERNAME/)*)([^/]*)/",r"\1FOLDERNAME/",s)),
        fixpoint(lambda s: re.sub(r"(Freigegebene%20Dokumente/(FOLDERNAME/)*)([^/]*)/",r"\1FOLDERNAME/",s)),
        lambda s: re.sub(r"(StructuredMaterials/([^/]*/)*)[^/]+$",r"\1FILENAME/",s),
        lambda s: re.sub(r"(SharedDocuments/([^/]*/)*)[^/]+$",r"\1FILENAME/",s),
        lambda s: re.sub(r"(MediaLibrary/([^/]*/)*)[^/]+$",r"\1FILENAME/",s),
        lambda s: re.sub(r"(Freigegebene%20Dokumente/([^/]*/)*)[^/]+$",r"\1FILENAME/",s),
        fixpoint(lambda s: re.sub(r"/[^/]+\.([^.]*)$",r"/FILENAME",s) if not re.search(r".aspx$",s) else s),

])
def parse_date(inp): 
    tmg_date_format = "%Y-%m-%d %H:%M:%S.%f"
    sharepoint_date_format = "%Y-%m-%dT%H:%M:%S"
    if sharepoint:
        date_format =  sharepoint_date_format 
    else:
        date_format = tmg_date_format
        if '.' not in inp:
            inp += '.0'
    return dt.datetime.strptime(inp,date_format)
#Model of action
class Action:
    def __init__(self,url,time,event):
        self.time = time
        self.event = event
        self.url = url


urls = set()
#reads the file accesses.csv, parsing dates into objects
byuser = dict()
for line in open(inpfile):
    parts = line.split(",")
    if(parts[0] == "user"):
        continue
    if not parts[0] in byuser:
        byuser[parts[0]] = list()

    if not len(parts) >= 4:
        continue
    url = ft.reduce(lambda a,b: a+b,parts[3:])
    if(all(fil(url) for fil in filters)):
        #Remove commas from urls. also remove trailing whitespace
        url = transforms(url)
        time = parse_date(parts[1])
        event = parts[2]
        byuser[parts[0]].append(Action(url,time,event))
        urls.add(url)

#This function is used to split sessions. It generally splits a into sublists.
#A split is made whenever fun returns true for list elements i and i+1
def split_lis_at(lis,fun):
    res = list()
    prevsplit = 0
    for i, item in enumerate(lis):
        is_at_end = i == (len(lis) -1)
        should_split = is_at_end or fun(lis[i],lis[i + 1]) 
        if(should_split):
            res.append(lis[prevsplit:i])
            prevsplit = i + 1
    return res
sessions = list()
for actions in byuser.values():
    actions.sort(key=lambda action:action.time)
    this_user_sessions = split_lis_at(actions, lambda a,b: (b.time-a.time).seconds > SESSION_TIMEOUT_SECS)
    sessions.extend(this_user_sessions)


#Filter out where two requests happen at the same time
sessions_no_dup_requests = [[action for (i,action) in enumerate(session) if (i == 0) or not session[i].time == session[i-1].time] for session in sessions]
sessions_only_human_accesses = [session for session in sessions_no_dup_requests if len(session) < 20]

resultfile = open('sessions.csv','w')
for session in sessions_only_human_accesses:
    if len(session) > 1:
        resultfile.write(",".join([str(action.url) for action in session]) + '\n')

#Some statistics on number of session and click length
#print("numusers" + str(len(byuser.keys())))
#print("numsessions" + str(len(sessions)))
#print("avglensessions" + str(sum(len(session) for session in sessions) / len(sessions)))
#print the average time between requests for each session
#for session in sessions_only_human_accesses:
    #times = list()
    #for i, action in enumerate(session):
        #if not i == (len(session)-1):
            #times.append((session[i+1].time - action.time).seconds)
    #if(len(session) > 1):
        #print(sum(times) / len(times))

