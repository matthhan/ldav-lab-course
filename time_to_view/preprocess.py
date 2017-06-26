#!/usr/bin/python3

import datetime as dt
import functools as ft
import re as re
import sys

#Models requests for easier handling
class Request:
    def __init__(self,datetime,method,userid):
        self.datetime = datetime
        self.method = method
        self.userid = userid
#Two Way dictionary that allows for translation to ints
class TwoWayDict:
    def __init__(self):
        self.string_to_number = dict()
        self.number_to_string = dict()
        self.counter = 0
    def insert(self,string):
        if(string in self.string_to_number):
            return self.numberOf(string)
        self.string_to_number[string] = self.counter
        self.number_to_string[self.counter] = string
        self.counter += 1
        return self.counter - 1
    def numberOf(self,string):
        return self.string_to_number[string]
    def stringOf(self,number):
        return self.number_to_string[number]

#filters applied to urls before processing
from_right_semester = lambda s: re.search(r"/(16ws-[0-9]*)/",s)
is_a_structured_material = lambda s: re.search(r"/StructuredMaterials/.*",s)
is_not_the_form = lambda s: not re.search(r"/StructuredMaterials/Forms",s)
is_not_layout = lambda s: not re.search(r"/_layouts/",s)
filters = [
    is_a_structured_material, 
    from_right_semester, 
    is_not_the_form,
    is_not_layout 
]

#Extract relevant information from the line
def extract_datetime(line):
    parts = line.split(",")
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    if '.' not in parts[1]:
        parts[1] += '.0'
    return dt.datetime.strptime(parts[1],date_format)
def extract_course(url):
    return re.search(r"/(16ws-[0-9]*)/",url).group(1)
def extract_document(url):
    return re.search(r"/StructuredMaterials/(.*)",url).group(1)
def extract_url(line):
    parts = line.split(",")
    return ft.reduce(lambda a,b: a+b,parts[3:])
def url_is_interesting(url):
    return all(fil(url) for fil in filters)
def extract_method(line):
    return line.split(",")[2]
def extract_userid(line):
    return line.split(",")[0]

requests = list()
documents = TwoWayDict()
courses = TwoWayDict()
userids = TwoWayDict()

atfirstline = True
for line in open(sys.argv[1]):
    if(atfirstline):
        atfirstline = False
        continue

    url = extract_url(line)

    by_course_and_doc = dict()
    if(url_is_interesting(url)):
        course = courses.insert(extract_course(url))
        if(not course in by_course_and_doc):
            by_course_and_doc[course] = dict()
        doc = documents.insert(extract_document(url))
        if(not doc in by_course_and_doc[course]):
            by_course_and_doc[course][doc] = dict()
        datetime = extract_datetime(line)
        method = extract_method(line)
        userid = userids.insert(extract_userid(line))

        new_request = Request(datetime, method, userid)
        by_course_and_doc[course][doc] = new_request

def times_to_view(requests_for_document):
    timedeltas = list()
    initial_post = (request in requests_for_document if request.method == "POST")[0]
    requests_after_initial_post = (request in requests_for_document if request.datetime > initial_post.datetime)
    userid = lambda x: x.userid
    for userid,requests in groupby(sorted(requests_after_initial_post,userid),userid):
        timedelta = initial_post.datetime - sorted(requests,lambda x: x.time)[0].datetime
        timedeltas.append(timedelta)
    return timedeltas
for course, documents in by_course_and_doc:
    for document, requests in documents:
        ttv = times_to_view(requests)
        summary = summarize(ttv)
        by_course_and_doc[course][doc] = summary
#TODO implement summary function




