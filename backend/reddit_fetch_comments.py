import praw
from datetime import datetime
import json
from db_client import conn_create, conn_close
from threading import Thread
from common import obtain_reddit_instance

redditClient = obtain_reddit_instance()
bertUrl = 'http://bert:5000/toxicity'


def fetch_comments(subreddit_name):
    print("Starting for {}".format(subreddit_name))
    sql = """
        INSERT INTO comment (source_identifier, source, raw_text, processing_status, status, data)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    subreddit = redditClient.subreddit(subreddit_name)
    try:
        conn, cur = conn_create()
        # put in db
        for cmt in subreddit.stream.comments():
            try:
                data = {
                    'comment_url': cmt.permalink,
                    'created_at': str(datetime.utcfromtimestamp(cmt.created_utc)),
                    'author_name': cmt.author.name,
                    'author_icon_img': cmt.author.icon_img,
                    'subreddit_id': cmt.subreddit_id
                }
                select_same_comment_query = """
                    select * from comment where source = %s and source_identifier = %s
                """
                cur.execute(select_same_comment_query, (subreddit_name, cmt.id, ))
                row = cur.fetchone()  # verifying same reddit comment doesn't exist already
                if row is None:
                    processing_status = 'init'
                    if cmt.author.name == 'AutoModerator': # Not processing Auto moderator's comments
                        processing_status = 'failed'
                    cur.execute(sql, (cmt.id, subreddit_name, cmt.body, processing_status, 'init', json.dumps(data)))
                    print("comment saved successfully comment_id : {}, subreddit: {}".format(cmt.id, subreddit_name))
                    conn.commit()
                else:
                    print("entry already exists. skipping comment : {}, subreddit: {}".format(cmt.id, subreddit_name))
            except Exception as error:
                print("Exception {} occurred while executing for: {}".format(error, cmt.id))
        print("ending stream...")
    except Exception as error:
        print("Error {0} occurred while writing comments to DB".format(error))
    finally:
        conn_close(conn)


if __name__ == '__main__':
    subreddits = ['amITheAsshole']
    try:
        for subreddit_name in subreddits:
            Thread(target=fetch_comments, args=(subreddit_name, )).start()
    except KeyboardInterrupt:
        print("keyboard interrupt.. existing")
