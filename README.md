# Learning Data Analytics and Visualization Lab Course

## What this is
I wrote this code in 2017 as part of the course "Learning Data Analytics and Visualization". It Fetches Data from a non-public MySQL database containing web server logs from an e-learning platform that is based on SharePoint and produces three visualizations:

* The first visualization shows frequent sequential patterns in the requests that people made to the web server. This was intended to find places where the usability of the page could be improved by adding more direct links to the things that people want to access.
* The second visualization shows a hierarchical pie chart (like the baobab software) of which parts of the system the learners spent their time in. The time spent is approximated from the dates of the requests by using a simple heuristic.
* The third visualization shows what fraction of the students took how long to view a particular learning material after it was uploaded into the system. This is intended to show how fast the learners can respond to new material.

## How to Run

 * Install *Python*, *sbt*, *npm* and the *mysql* command line tool.
 * Have roughly 8gb or more of RAM, ~50GB of free disk space and a good internet connection.
 * Have LDAVLAB_UN and LDAVLAB_PW environment variables set to your username and password for the mysql database.
 * execute `do_everything.sh` in project root.
 * Wait for roughly a day or two.
 * Final vis resides in `vis/build` just open the `index.html` file in a browser of your choice.

