'''

This module has 3 tasks:

1) On reading, update the views in approved_articles 
2) On liking the article, append a record in user_history and update the likes in approved_articles by incrementing it by 1
3) On unliking an article, delete the row from user_history and update the likes in approved_articles by decrementing it by 1

'''

from datetime import datetime
from dotenv import load_dotenv   
load_dotenv()
import os
import pymysql

a=os.environ.get('host')
b=os.environ.get('user')
c=os.environ.get('password')	
d=os.environ.get('database')



#Server 2 send Server 4 the article id of the article opened by the user
#let us assume a value in this case
#article_id = 'abc0123 2021-08-23 01:49:30'
#user_id='abc123'


def onread(article_id,user_id):

     mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
     mycursor=mydb.cursor()

     instruction ="update iicblogdatabase.approved_articles set views =views+1 where article_id=%s"
     data=(article_id,)
     mycursor.execute(instruction,data)
     mydb.commit()


     instruction="select * from iicblogdatabase.user_history where user_id =%s and article_id = %s"
     data=(user_id,article_id)
     mycursor.execute(instruction,data)
     result=mycursor.fetchone()
     if result==None:
          k=1
     else:
          k=2

     m=datetime.now()
     if k==1:
          instruction="insert into iicblogdatabase.user_history (article_id, user_id, like_status,date) values (%s,%s,%s,%s)"
          data=(article_id,user_id,0,m)
     elif k==2:
          instruction="update iicblogdatabase.user_history set date = %s where user_id=%s and article_id=%s"
          data=(m,user_id,article_id)

     mycursor.execute(instruction,data)
     mydb.commit()

     mydb.close()

def onlike(article_id,user_id):

     mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
     mycursor=mydb.cursor()

     instruction="update iicblogdatabase.user_history set like_status = 1 where article_id = %s and user_id = %s"
     data=(article_id,user_id)
     mycursor.execute(instruction,data)
     mydb.commit()

     instruction="update iicblogdatabase.approved_articles set likes=likes+1 where article_id=%s"
     data=(article_id,)
     mycursor.execute(instruction,data)
     mydb.commit()

     mydb.close()

def onunlike(article_id,user_id):

     mydb=pymysql.connect(host=a,user=b,password=c,database=d,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
     mycursor=mydb.cursor()

     instruction="update iicblogdatabase.user_history set like_status = 0 where user_id =%s and article_id = %s"
     data=(user_id,article_id)
     mycursor.execute(instruction,data)

     instruction="update iicblogdatabase.approved_articles set likes=likes-1 where article_id=%s"
     data=(article_id,)
     mycursor.execute(instruction,data)
     mydb.commit()

     mydb.close()


