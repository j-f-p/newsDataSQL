# Logs Analysis
# SQL views here created are temporary. They are not saved to the database.

import datetime, psycopg2

def generateCommonViews(cursor):
    # These views are common to topThreeArticles() and topThreeAuthors().

    # Create articles view with path instead of slug so that this view can be
    # joined to a log view with path as the common column.
    cursor.execute(
        "create view v1 as "
      + "select id, author, title, concat('/article/', slug) as path "
      + "from articles;")

    # Create a view that joins components of the articles and log tables.
    # Note that since slug is unique, according to '\d articles',
    # path = concat('/article/', slug) is also unique. Thus, view v2 is formed
    # by counting in a way to guarantee unique articles are counted.
    cursor.execute(
        "create view v2 as "
      + "select v1.path, count(1) as views from v1, "
      + "(select path from log where path like '/article/%') as subs "
      + "where v1.path = subs.path "
      + "group by v1.path order by views desc" )

def topThreeArticles():
    """List the most popular three articles of all time"""
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()

    generateCommonViews(cursor)

    # Collect the relevant content in the expected order.
    cursor.execute(
        "select v1.title, v2.views from v2, v1 "
      + "where v2.path = v1.path order by views desc limit 3")

    topArticles = cursor.fetchall()
    conn.close()
    return topArticles

def topThreeAuthors():
    """List the most popular three authors of all time"""
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()

    generateCommonViews(cursor)

    # Create a view with a request count grouped by authors
    # from v2 joined with v1.
    cursor.execute(
        "create view v3 as "
      + "select v1.author, sum(v2.views) as \"Author Views\" "
      + "from v1, v2 where v1.path = v2.path "
      + "group by v1.author order by \"Author Views\" desc;" )

    # Collect the relevant content in the expected order.
    cursor.execute(
        "select authors.name, v3.\"Author Views\" "
      + "from authors, v3 "
      + "where authors.id = v3.author limit 3;")

    topAuthors = cursor.fetchall()
    conn.close()
    return topAuthors

def significantErrorDays():
    """List days when more than 1% of requests lead to errors"""
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()

    errorProneDays = cursor.fetchall()
    conn.close()
    return errorProneDays

def printTopThreeArticles():
    print("\n{0:^56}\n".format("Top 3 Viewed Articles"))
    print("{0:^40}{1:^16}".format("Article","Views"))
    for article in topThreeArticles():
        print("{0:^40}{1:^16}".format(article[0], article[1]))
    print

def printTopThreeAuthors():
    print("\n{0:^56}\n".format("Top 3 Viewed Authors"))
    print("{0:^40}{1:^16}".format("Author","Total Article Views"))
    for article in topThreeAuthors():
        print("{0:^40}{1:^16}".format(article[0], article[1]))
    print

# printTopThreeArticles()
printTopThreeAuthors()
