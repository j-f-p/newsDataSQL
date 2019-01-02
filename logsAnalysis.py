# Logs Analysis
import datetime, psycopg2

def topThreeArticles():
  """List the most popular three articles of all time"""
  conn = psycopg2.connect("dbname=news")
  cursor = conn.cursor()
  cursor.execute( "select sub1.path, count(sub1.path) as num from "
    + "(select concat('/article/', slug) as path from articles) as sub1, "
    + "(select path from log where path like '/article/%') as sub2 "
    + "where sub1.path = sub2.path "
    + "group by sub1.path order by num desc limit 3" )
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

print("{0:>32}{1:>32}".format("Article","Views"))
for article in topThreeArticles():
    print("{0:>32}{1:>32}".format(article[0], article[1]))
