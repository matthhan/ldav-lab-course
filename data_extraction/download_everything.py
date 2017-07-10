#!/usr/bin/env python
import os
import sys

if len(sys.argv) <= 1:
    print('download_everything.py was called without command line parameters. Usage: <command> <username> <password>')
    exit()
username = sys.argv[1]
password = sys.argv[2]
folder = '../base_data'
tmg_table_names = ['October','November', 'December', 'Jan2017', 'Feb2017', 'Mar2017']


sharepoint_query = {'query':'SELECT `User Id` AS user, `Occurred (GMT)` AS time, Event, `Document Location` AS url FROM ldavlab.sharepoint', 'name': 'sharepoint'};

tmg_query_base = 'SELECT clientip AS user, logtime AS time, operation AS Event, uri AS url FROM TMG_';
tmg_queries = [{'query':tmg_query_base + table_name, 'name':table_name} for table_name in tmg_table_names]

def quote(thing):
    return '"' + thing + '"'
def make_script(thing):
    mysql_invocation ="mysql --batch --quick --user=" + username + " --password=" + password + " --host=dolgi.informatik.rwth-aachen.de --database=ldavlab"
    translate_tabs_to_commas = "tr '\\t' ','"
    save_file = folder + '/' +thing['name'] + '.csv'

    return "echo " + quote(thing['query']) + ' |  ' + mysql_invocation + ' | ' +translate_tabs_to_commas + ' > ' + save_file

scripts = [make_script(query) for query in [sharepoint_query] + tmg_queries]


for script in scripts:
    print(script)
    os.system(script)
