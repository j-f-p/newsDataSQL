## Logs Analysis

### Description

This is a script that gathers information from a database of a news website. The database contains information about news articles, authors of these articles and the history of internet requests to view the articles from a recent time period. The script returns three tables: the most popular three articles from the database, all the article authors listed in order of author article views, and the days on which more than 1% of article view requests fail.

This script was written for a Udacity course about SQL with Python and Postgresql.

### Execution

The development environment for developing the script is a Linux virtual machine run by Vagrant 2.2.2 and VirtualBox 6.0 with files from https://github.com/udacity/fullstack-nanodegree-vm . The script is compatible with Python 3 and executed in the project environment as follows:
```
$ python logsAnalysis.py
```
