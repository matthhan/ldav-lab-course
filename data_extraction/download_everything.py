#!/usr/bin/env python

tmg_table_names = ['October','November', 'December', 'Jan2017', 'Feb2017', 'Mar2017']


sharepoint_query = {'query':'SELECT `User Id` AS user, `Occurred (GMT)` AS time, Event, `Document Location` AS url FROM ldavlab.sharepoint', 'name': 'sharepoint'};

tmg_query_base = 'SELECT clientip AS user, logtime AS time, operation AS Event, uri AS url FROM TMG_';
tmg_queries = [{'query':tmg_query_base + table_name, 'name':table_name} for table_name in tmg_table_names]

def quote(thing):
    return '"' + thing + '"'
def make_script(thing):
    return "mysql --batch --quick --user=ldavlab_matthias --password=$MYSQL_PASSWORD --host=dolgi.informatik.rwth-aachen.de --database=ldavlab < " + "echo " + quote(thing['query']) +  " | tr '\\t' ',' > " + thing['name'] + '.csv'


scripts = [make_script(query) for query in [sharepoint_query] + tmg_queries]


for script in scripts:
    print(script)
