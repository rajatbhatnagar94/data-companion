from db_client import conn_create, conn_close
from transformers import BertTokenizer
from common import SUBTASK_TYPES, TOXIC_HL, TOXIC_NO_HL, get_response_object, TOXIC
import time
import random

def get_query(predicted_label_filter, limit):
    base_query = """
        select c.* from comment c
        where c.source = %(source)s
        """ + predicted_label_filter + """
        order by c.created_at desc
        limit """ + str(limit) + """ offset %(offset)s
    """
    return base_query


def get_latest_comments(source: str, task_type: str, sub_task_type: str, limit: int = 10, offset: int = 0, prevIds: list = [], filters = {}):
    response = {'data': [], 'status': 'fail'}
    try:
        conn, cur = conn_create()
        queryParams = {
            'task_type': task_type,
            'source': source,
            'offset': offset
        }
        predicted_label_filter = ""
        if prevIds and len(prevIds) > 0:
            predicted_label_filter += " and c.id not in %(prevIds)s"
            queryParams['prevIds'] = tuple(prevIds)
        predicted_label_filter += " and c.status in %(comment_status)s"
        queryParams['comment_status'] = ('pending', 'recurring')
        get_new_comments_queries = [
            get_query(predicted_label_filter + " and c.predicted_label = 1 and c.class_prob[2] > 0.5 ", limit),
        ]
        results = []
        for get_new_comments_query in get_new_comments_queries:
            # print(cur.mogrify(get_new_comments_query, queryParams))
            cur.execute(get_new_comments_query, queryParams)
            result = cur.fetchall()
            results.extend(result)
        results = [dict(row) for row in results]
        for row in results:
            obj = get_response_object(row, sub_task_type)
            response['data'].append(obj)
        response['status'] = 'success'
    except Exception as e:
        print("Exception occurred. e: {0}, limit: {1},".format(e, limit))
    finally:
        conn_close(conn)
        return response


if __name__ == '__main__':
    response = get_latest_comments(10,  'explainlikeimfive', 'reddit_classify', 'toxic_no_hl', 30, 0, None, filters={'comment_id': 'g00qkal'})
    print(response)
