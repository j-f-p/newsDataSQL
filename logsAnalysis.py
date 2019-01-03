# Logs Analysis
import datetime, psycopg2

def topThreeArticles():
  """List the most popular three articles of all time"""
  conn = psycopg2.connect("dbname=news")
  cursor = conn.cursor()
  cursor.execute("create view av1 as select id, author, title, "
    + "concat('/article/', slug) as path from articles;")
  # Note that since slug is unique, according to '\d articles',
  # path = concat('/article/', slug) is also unique. Thus, first count
  # in a way to guarantee unique articles are counted.
  cursor.execute("create view av2 as "
    + "select av1.path, count(1) as views from av1, "
    + "(select path from log where path like '/article/%') as sub2 "
    + "where av1.path = sub2.path "
    + "group by av1.path order by views desc limit 3" )
  # Then, display the relevant content in the expected order.
  cursor.execute("select av1.title, av2.views from av2, av1 "
    + "where av2.path = av1.path order by views desc")
  topArticles = cursor.fetchall()
  conn.close()
  return topArticles

def topThreeAuthors(raw_content):
  """Add a post to the 'database' with the current timestamp."""
  sanitized_content = bleach.clean(raw_content)
  conn = psycopg2.connect("dbname=forum")
  cursor = conn.cursor()
  cursor.execute( "insert into posts (content) values(%s)",
          (sanitized_content,) )
  conn.commit()
  conn.close()

print
print("{0:^56}".format("Top 3 Viewed Articles"))
print
print("{0:^40}{1:^16}".format("Article","Views"))
for article in topThreeArticles():
    print("{0:^40}{1:^16}".format(article[0], article[1]))
print
