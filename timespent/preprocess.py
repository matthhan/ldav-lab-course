#!/usr/bin/python3

import os
import copy
import datetime as dt
import functools as ft
import itertools as it
import re 
import sys
import copy
import json
import urllib.parse
from preprocess_courses_table import find_courses 

coursroomsfilename = sys.argv[1]
inpfilenames = sys.argv[2:]
courses = find_courses(coursroomsfilename)

#filters applied to urls before processing
is_not_a_form = lambda s: not re.search(r"/StructuredMaterials/Forms",s)
is_not_layout = lambda s: not re.search(r"/_layouts/",s)
not_none = lambda s: s
belongs_to_course = lambda s: re.search(r"/([0-9][0-9][ws]s-[0-9]*)/",s)
filters = [
    not_none,
    is_not_a_form,
    is_not_layout,
    belongs_to_course,
    lambda s: not re.search(r"/WebResource.axd",s),
    lambda s: not re.search(r"Dashboard.aspx$",s),
    lambda s: not re.search(r"AllItems.aspx$",s),
    lambda s: not re.search(r"/_vti_bin/",s)
]

#Extract relevant information from the line
def extract_course(url):
    return re.search(r"/([0-9][0-9][ws]s-[0-9]*)/",url).group(1)
def extract_url(line):
    parts = line.split(",")
    try:
        return ft.reduce(lambda a,b: a+b,parts[3:])
    except:
        return None
def url_is_interesting(url):
    return all(fil(url) for fil in filters)
def extract_method(line):
    return line.split(",")[2]
def extract_userid(line):
    return line.split(',')[1]
def extract_datetime(line):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    parts = line.split(',')
    return dt.datetime.strptime(parts[1] if '.' in parts[1] else parts[1] + '.0',date_format)
                                

def parse_path_items(path):
    if(path==""):
        return []
    match = re.match(r"/([^/]*)(.*)",path)
    first = match.group(1)
    rest = match.group(2)
    res = [first]
    res.extend(parse_path_items(rest))
    return res
def path_after(prefix,inp):
    return parse_path_items(re.search(prefix + r"(.*)",url).group(1))

def categorize_request(url):
    if(re.search(r"/StructuredMaterials/",url)):
        return ["Learning Material"] + path_after("/StructuredMaterials",url)
    elif(re.search(r"/LA_Assignments/",url)):
        return ["Assignment"] + path_after("/LA_Assignments",url)
    elif(re.search(r"/LA_AssignmentDocuments/",url)):
        return ["Assignment Document"] + path_after("/LA_AssignmentDocuments",url)
    elif(re.search(r"/MediaLibrary/",url)):
        return ["Media Item"] + path_after("/MediaLibrary",url)
    elif(re.search(r"/eTests_IFrame.aspx",url)):
        return ["E-Test"]
    elif(re.search(r"/DiscussionForum/",url)):
        return ["Discussion Forum"] + path_after("/DiscussionForum",url)
    elif(re.search(r"/LA_SampleSolutions/",url)):
        return ["Sample Solution"] + path_after("/LA_SampleSolutions",url)
    elif(re.search(r"/LiteratureDocuments/",url)):
        return ["Literature Document"] + path_after("/LiteratureDocuments",url)
    elif(re.search(r"/SharedDocuments/",url)):
        return ["Shared Document"] + path_after("/SharedDocuments",url)
    elif(re.search(r"Dynexite_IFrame.aspx",url)):
        return ["Dynexite"]
    elif(re.search(r"/GWS_[^/]*/",url)):
        return ["Group Workspace"] + path_after("/GWS_[^/]*",url)
    elif(re.search(r"/WikiList1/",url)):
        return ["Wiki"] + path_after("/WikiList1",url)
    return None

class Request: 
    def get_rest_categories(self):
        cp = copy.deepcopy(self)
        if(cp.category):
            cp.category = cp.category[1:]
        return cp


final_result = dict()
file_lines = sum([os.stat(inpfilename).st_size / 200 for inpfilename in inpfilenames])
i = 0
for inpfilename in inpfilenames:
    by_course = dict()
    by_user = dict()
    for line in open(inpfilename):
        i+= 1
        if(i == 1):
            continue
        if(i % 1000 == 0):
            print(str(((i/file_lines)*100)//1) + "% Done", end= '\r', file=sys.stderr)

        url = extract_url(line)
        if(not url):
            continue
        method = extract_method(line)
        
        if(not (method == 'GET')):
            continue
        if(not url_is_interesting(url)):
            continue

        course = extract_course(url)
        if(course not in by_course):
            by_course[course] = list()
        res = Request()
        res.category = categorize_request(url)
        res.time_spent = 1
        res.datetime = extract_datetime(line)
        res.userid = extract_userid(line)
        if(res.userid not in by_user):
            by_user[res.userid] = list()


        if(res.category):
            by_course[course].append(res)
            by_user[res.userid].append(res)
    default_time = 600
    def add_time_spent(one_users_requests):
        one_users_requests.sort(key=lambda request: request.datetime)
        for i, request in enumerate(one_users_requests):
            is_last_request = i == (len(one_users_requests)-1)
            if(is_last_request):
                request.time_spent = default_time
            else:
                next_request = one_users_requests[i+1]
                request.time_spent = calculate_time_spent(request,next_request)

    def calculate_time_spent(request,next_request):
        passed_time = (next_request.datetime - request.datetime).seconds
        two_hours = 7200 
        if(passed_time > two_hours):
            return default_time
        else:
            return passed_time


    def summarize_accesses(requests):
        first_level_names = list(set([request.category[0] for request in requests if request.category]))
        
        res = list()
        for name in first_level_names:
            time_spent = sum([request.time_spent for request in requests if request.category and request.category[0] == name ])
            children = summarize_accesses([request.get_rest_categories() for request in requests if request.category and request.category[0] == name ])
            res.append({
                'name':urllib.parse.unquote(name),
                'seconds_spent':time_spent,
                'children':children
            })
        return res

    def merge(old_accesses,new_accesses):
        for access in new_accesses:
            matching = [oldacc  for oldacc in old_accesses if oldacc['name'] == access['name']]
            if len(matching) > 0:
                matching[0]['seconds_spent'] += access['seconds_spent']
                merge(matching[0]['children'],access['children'])
            else: 
                old_accesses.append(access)
    for user,requests in by_user.items():
        add_time_spent(requests)
    for course, accesses in by_course.items():
        right_lv_number = [x for x in courses if (x['lv_number'] == course)]
        if(len(right_lv_number) > 0 ):
            coursobj = right_lv_number[0]
            if(course in final_result):
                merge(final_result[course]['accesses'],summarize_accesses(accesses))
            else:
                final_result[course] = {'accesses':summarize_accesses(accesses),'faculty':coursobj['faculty'],'title': coursobj['name'],'institute':coursobj['institute'],'semester':coursobj['semester']}

print(json.dumps(final_result))
