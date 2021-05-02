from datetime import datetime
from psaw import PushshiftAPI
import json
import gzip
import time
import os

def find_latest_timestamp(filename):
    max_time = 0
    with gzip.open(filename, "rt") as fin:
        for line in fin:
            data = json.loads(line)
            if data["created_utc"] > max_time:
                max_time = data["created_utc"]
    return max_time

def write_results(filename, results):
    with gzip.open(filename, "at") as fout:
        for r in results:
            fout.write("%s\n" % json.dumps(r.d_))

def get_results(subreddit, start_time, end_time, output_file, comments=False):
    api = PushshiftAPI()
    if os.path.exists(output_file):
        start_time = find_latest_timestamp(output_file)
    while start_time < end_time:
        if comments:
            results = list(api.search_comments(subreddit=subreddit, after=start_time, before=end_time, limit=500, sort="asc"))
        else:
            results = list(api.search_submissions(subreddit=subreddit, after=start_time, before=end_time, limit=500, sort="asc"))
        if len(results) == 0:
            break
        write_results(output_file, results)
        start_time = max([d.created_utc for d in results])
        print(datetime.fromtimestamp(start_time), len(results))

if __name__ == "__main__":
    start_time = int(datetime(2015, 1, 1).timestamp())
    end_time = int(datetime(2020, 1, 10).timestamp())
    get_results("gatech", start_time, end_time,
            "gatech_comments.jsonlist.gz", comments=True)
    # get_results("changemyview", start_time, end_time,
    #         "cmv_comments.jsonlist.gz", comments=True)


