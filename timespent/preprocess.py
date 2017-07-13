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
inpfilename= sys.argv[1]
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
def subcategorize_learning_material(url):
    rest = re.search(r"/StructuredMaterials(.*)",url).group(1)
    subcategories = parse_path_items(rest)
    res = ["Learning Material"]
    res.extend(subcategories)
    return res

def categorize_request(url):
    if(re.search(r"/StructuredMaterials/",url)):
        return subcategorize_learning_material(url)
    elif(re.search(r"/LA_Assignments/",url) or re.search(r"/LA_AssignmentDocuments/",url)):
        return ["Assignment"]
    elif(re.search(r"/MediaLibrary/",url)):
        return ["Media Item"]
    elif(re.search(r"/eTests_IFrame.aspx",url)):
        return ["E-Test"]
    elif(re.search(r"/DiscussionForum/",url)):
        return ["Discussion Forum"]
    elif(re.search(r"/LA_SampleSolutions/",url)):
        return ["Sample Solution"]
    elif(re.search(r"/LiteratureDocuments/",url)):
        return ["Literature Document"]
    elif(re.search(r"/SharedDocuments/",url)):
        return ["Shared Document"]
    elif(re.search(r"Dynexite_IFrame.aspx",url)):
        return ["Dynexite"]
    elif(re.search(r"/GWS_[^/]*/",url)):
        return ["Group Workspace"]
    elif(re.search(r"/WikiList1/",url)):
        return ["Wiki"]
    return None

class Request: 
    def get_rest_categories(self):
        cp = copy.deepcopy(self)
        if(cp.category):
            cp.category = cp.category[1:]
        return cp


by_course = dict()
by_user = dict()
file_lines = os.stat(inpfilename).st_size / 200
i = 0
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

for user,requests in by_user.items():
    add_time_spent(requests)
res = dict()
for course, accesses in by_course.items():
    res[course] = summarize_accesses(accesses)
print(json.dumps(res))
