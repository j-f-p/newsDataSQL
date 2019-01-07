# Logs Analysis

## Objective
`./logsAnalysis.py` is a Python script that employs SQL to gather information from a database of a news website contained in `./newsdata.sql`. The Python script was written for a Udacity course about SQL with Python database APIs, including Postgresql.

## Description and Design
`newsdata.sql` contains information about news articles, authors of these articles and the history of internet requests to view the articles from a prior time period. `logsAnalysis.py` returns three tables of data processed from the database. The respective contents of the tables are:
<ul>
(Table 1) the most popular three articles from the database<br>
(Table 2) all the article authors listed in order of author article views<br>
(Table 3) the days on which more than 1% of article view requests failed
</ul>

The script is compatible with Python 3 and employs the psycopg2 Postgresql SQL database API. For each output table, there is a function for processing the data with SQL queries and a function for printing the results of the queries as a plain text table. In this way, the code is kept modular.

The SQL queries employ temporary views (they are not saved to the database) for reasons of convenience of human encoding and decoding. A couple of the views are employed to generate two of the output tables. Thus, they were created in a separate function. All of the SQL queries, including those for creating views, that are employed to generate the tables are listed below.

**First two views for processing Tables 1 and 2**
```SQL
create view v1 as
select id, author, title, concat('/article/', slug) as path
from articles;
```
```SQL
create view v2 as
select v1.path, count(1) as views from v1,
(select path from log where path like '/article/%') as subs
where v1.path = subs.path
group by v1.path order by views desc;
```

**Final query for collecting data for Table 1**
```SQL
select v1.title, v2.views from v2, v1
where v2.path = v1.path order by views desc limit 3;
```

**Third view for processing Table 2**
```SQL
create view v3 as
select v1.author, sum(v2.views) as \"Author Views\"
from v1, v2 where v1.path = v2.path
group by v1.author order by \"Author Views\" desc;
```

**Final query for collecting data for Table 2**
```SQL
select authors.name, v3.\"Author Views\"
from authors, v3
where authors.id = v3.author;
```

**Four views for processing Table 3**
```SQL
create view v1 as select status, substring(time::text from 1 for 10)
as date from log;
```
```SQL
create view v2 as select date, count(1) as requests from v1
group by date;
```
```SQL
create view v3 as select date, count(1) as errors from v1
where v1.status != '200 OK' group by date order by date;
```
```SQL
create view v4 as select v2.date, 100.0 * errors / requests
as \"% failed\" from v2, v3 where v2.date = v3.date;
```

**Final query for collecting data for Table 3**
```SQL
select date, \"% failed\" from v4 where \"% failed\" > 1;
```

## Environment
The development environment for developing `logsAnalysis.py` is a Linux virtual machine defined by the [Udacity FSND Virtual Machine][1] and provisioned by Vagrant 2.2.2 and VirtualBox 6.0.

## Execution
* Install [Vagrant](https://www.vagrantup.com/)
* Install [VirtualBox](https://www.virtualbox.org/)
* Clone or download the [Udacity FSND Virtual Machine][1], which is contained by a repo head directory with various files and subdirectories.
* Give the repo head directory a relevant name and place it in an appropriate location. The repo `vagrant/` subdirectory contains files that are shareable between the host and guest operating systems, hereafter referred to as the vagrant directory.
* Enter the vagrant directory through a Linux command line interface. Then, install and boot the virtual machine by:
```bash
$ vagrant up
```
* Log into the virtual machine by:
```bash
$ vagrant ssh
```
* Create a working subdirectory in the vagrant directory and add `newsdata.sql` and `logsAnalysis.py`.
* Enter the working directory and load the news database by:
```bash
$ psql -d news -f newsdata.sql
```
* Execute `logsAnalysis.py` by:
```bash
$ ./logsAnalysis.py
```

## Sample Output
Sample output is provided by `./output.txt`.

[1]: https://github.com/udacity/fullstack-nanodegree-vm
