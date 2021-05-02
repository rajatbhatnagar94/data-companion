import praw
import time
import requests
import json
from db_client import conn_create, conn_close
from common import get_response_object, obtain_reddit_instance, TOXIC_HL, TOXIC

redditClient = obtain_reddit_instance()

def send_mod_message(comment):
	response_obj = get_response_object(comment, TOXIC_HL)
	subreddit_name = response_obj['source']
	subreddit = redditClient.subreddit(subreddit_name)
	## overriding temporarily
	subreddit = redditClient.redditor('rajatbhatnagar94')
	subject = "You have a new toxic message"
	url = f"http://detoxify.machineintheloop.com/reddit/{response_obj.get('source')}?subtask_type=toxic_hl&comment_id={response_obj.get('source_identifier')}"
	response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
	if response.status_code == 200:
		link = response.text
		message = f"This comment violates Rule 1. Go to - [link]({link}) if it's an error DetoxifyBot"
		body = ["We found a toxic comment. Here's the toxic comment - "]
		body += ["\n\n"]
		for rationale in response_obj['rationale']:
			if rationale.get('highlightType') == TOXIC:
				body += ["**{}**".format(rationale.get('text'))]
			else:
				body += [rationale.get('text')]
		body += ["\n\n\n\n\n"]
		info = ["More Information\n"]
		info += ['- Comment Link - [{0}]({0})'.format(response_obj.get('comment_url'))]
		info += [f"- This comment violates Rule 1. Go to - {url}, if its an error DetoxifyBot"]
		description = " ".join(body)
		description += "\n".join(info)
		subreddit.message(subject, description)


def report_comment(comment):
	redditOldClient = praw.Reddit(client_id='8LNDKl7HusySlQ', client_secret='bvNAk41kz5FW4bJvp_urp5prQbw', password='throwawayTester_blah', user_agent= 'throwawayTester_blah', username='throwawayTester_blah')
	response_obj = get_response_object(comment, TOXIC_HL)
	subreddit_name = response_obj['source']
	comment_id = comment.get('source_identifier')
	url = f"http://detoxify.machineintheloop.com/reddit/{subreddit_name}?subtask_type=toxic_hl&comment_id={comment_id}"
	response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
	if response.status_code == 200:
		link = response.text
		message = f"This comment violates Rule 1. Go to - {link} if it's an error -DetoxifyBot"
		redditComment = redditOldClient.comment(comment_id)
		redditComment.report(message)
		send_mod_message(comment)
		try:
		    conn, cur = conn_create()
		    cur.execute("update comment set reported = true where source_identifier = %s", (comment_id, ))
		    conn.commit()
		except Exception as e:
		    print(f"Exception occurred while updating report in db - {e}")


def process_comments(subreddits):
    reporting_allowed_subreddits = ['dragonfliesflaydrama', 'gatech']
    # process all unprocessed comments
    get_unprocessed_query = "select id, raw_text, source from comment where processing_status = 'init' and source in %s order by id limit 100"
    unprocessed_comments = None
    try:
        conn, cur = conn_create()
        # get all unprocessed comments
        cur.execute(get_unprocessed_query, (tuple(subreddits),))
        unprocessed_comments = cur.fetchall()
    except Exception as error:
        print("Error {0} occurred while fetching unprocessed comments to DB".format(error))
    finally:
        conn_close(conn)

    if unprocessed_comments is None or len(unprocessed_comments) == 0:
        print("No new comments to process")
        return

    predictions = {}
    try:
        for comment in unprocessed_comments:
            classify_comment_url = 'http://detoxify.machineintheloop.com/api/classify'
            response = requests.get(classify_comment_url,
                                    params={'text': comment['raw_text']})
            if response.status_code == 200:
                resp = json.loads(response.text)
                if resp and resp['status'] == 'success':
                    predictions[comment['id']] = {
                       'predicted_label': resp['predicted_label'],
                        'model_identifier': resp['model_identifier'],
                        'rationale': resp['rationale'],
                        'tokens': resp['tokens'],
                        'class_prob': resp['class_prob'],
                        'status': 'pending',
                        'source': comment['source']
                    }
                else:
                    print("failed to get data for comment_id - {}".format(comment['id']))
            elif response.status_code == 414:

                try:
                    conn, cur = conn_create()
                    sql = "update comment set processing_status='failed' where id=%s"
                    cur.execute(sql, (comment['id'], ))
                    conn.commit()
                except Exception as error:
                    print("Error {0} occurred while updating processed comment statuses to DB".format(error))
                finally:
                    conn_close(conn)
            else:
                print("response failed for comment_id - {}".format(comment['id']))

    except Exception as e:
        print("Error {0} occurred while computing prediction for comment".format(e))

    sql = "update comment set processing_status='processed'," \
          "predicted_label= %s, model_identifier=%s, status=%s, tokens=%s, rationale=%s, class_prob= %s where id=%s returning *"
    try:
        conn, cur = conn_create()
        # update comment status and predictions
        for key in predictions:
            cur.execute(sql, (predictions[key]['predicted_label'],
                              predictions[key]['model_identifier'],
                              predictions[key]['status'],
                              predictions[key]['tokens'],
                              predictions[key]['rationale'],
                              predictions[key]['class_prob'],
                              key))
            conn.commit()
            if predictions[key]['predicted_label'] == 1 and reporting_allowed_subreddits.index(predictions[key]['source']) > -1:
                comment_db = cur.fetchone()
                report_comment(comment_db)
        print("processed successfully, count - {0}".format(len(predictions)))
    except Exception as error:
        print("Error {0} occurred while updating processed comment statuses to DB".format(error))
    finally:
        conn_close(conn)

if __name__ == '__main__':
	subreddits = ['dragonfliesflaydrama', 'explainlikeimfive', 'changemyview', 'science', 'coronavirus', 'gatech']
	#subreddits = ['dragonfliesflaydrama']
	try:
		while True:
			process_comments(subreddits)
			print("sleeping.. ")
			time.sleep(2)
	except KeyboardInterrupt:
		print("keyboard interrupt.. existing")
