# Logs Analysis
import datetime, psycopg2

def topThreeArticles():
    """List the most popular three articles of all time"""
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    # Views here created are temporary. They are not saved to the database.
    cursor.execute("create view av1 as "
    + "select id, author, title, concat('/article/', slug) as path "
    + "from articles;")
    # Note that since slug is unique, according to '\d articles',
    # path = concat('/article/', slug) is also unique. Thus, view av2 is formed
    # by counting in a way to guarantee unique articles are counted.
    cursor.execute("create view av2 as "
    + "select av1.path, count(1) as views from av1, "
    + "(select path from log where path like '/article/%') as subs "
    + "where av1.path = subs.path "
    + "group by av1.path order by views desc limit 3" )
    # Then, display the relevant content in the expected order.
    cursor.execute("select av1.title, av2.views from av2, av1 "
    + "where av2.path = av1.path order by views desc")
    topArticles = cursor.fetchall()
    conn.close()
    return topArticles

def topThreeAuthors():
    """List the most popular three authors of all time"""
    conn = psycopg2.connect("dbname=news")
    cursor = conn.cursor()
    # See comments in topThreeArticles() about views av1 and av2.
    cursor.execute("create view av1 as "
    + "select id, author, title, concat('/article/', slug) as path "
    + "from articles;")
    # View av2 is different here in that it includes all the articles.
    cursor.execute("create view av2 as "
    + "select av1.path, count(1) as views from av1, "
    + "(select path from log where path like '/article/%') as subs "
    + "where av1.path = subs.path "
    + "group by av1.path order by views desc;" )
    # Apply a count to av2 joined with av1 grouped by authors
    cursor.execute("create view av3 as "
    + "select av1.author, sum(av2.views) as \"Author Views\" "
    + "from av1, av2 where av1.path = av2.path "
    + "group by av1.author order by \"Author Views\" desc;" )
    cursor.execute("select authors.name, av3.\"Author Views\" "
    + "from authors, av3 "
    + "where authors.id = av3.author limit 3;")
    topAuthors = cursor.fetchall()
    conn.close()
    return topAuthors

def printTopThreeArticles():
    print
    print("{0:^56}".format("Top 3 Viewed Articles"))
    print
    print("{0:^40}{1:^16}".format("Article","Views"))
    for article in topThreeArticles():
        print("{0:^40}{1:^16}".format(article[0], article[1]))
    print

def printTopThreeAuthors():
    print
    print("{0:^56}".format("Top 3 Viewed Authors"))
    print
    print("{0:^40}{1:^16}".format("Author","Total Article Views"))
    for article in topThreeAuthors():
        print("{0:^40}{1:^16}".format(article[0], article[1]))
    print

# printTopThreeArticles()
printTopThreeAuthors()
