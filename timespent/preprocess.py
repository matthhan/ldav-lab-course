#!/usr/bin/python3

import datetime as dt
import functools as ft
import itertools as it
import re 
import sys
import copy
import json

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

by_course = dict()
atfirstline = True
for line in open(sys.argv[1]):
    if(atfirstline):
        atfirstline = False
        continue

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
    category = categorize_request(url)
    if(category):
        by_course[course].append(category)

def summarize_accesses(accesses):
    names = list(set([lis[0] for lis in accesses if lis]))
    
    res = list()
    for name in names:
        time_spent = len([x for x in accesses if x and x[0] == name ])
        children = summarize_accesses([x[1:] for x in accesses if x and x[0] == name ])
        res.append({
            'name':name,
            'seconds_spent':time_spent,
            'children':children
        })
    return res

res = dict()
for course, accesses in by_course.items():
    res[course] = summarize_accesses(accesses)
print(json.dumps(res))
