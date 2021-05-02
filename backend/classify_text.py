from pprint import pprint
import requests
import json

def classify_text(text, verbose=False):
    classify_comment_url = 'http://detoxify.machineintheloop.com/api/classify'
    response = requests.get(classify_comment_url, params={'text': text})
    obj = {'status': 'fail'}
    if response.status_code == 200:
        resp = json.loads(response.text)
        if resp and resp['status'] == 'success':
            obj['predicted_label'] = resp['predicted_label']
    return obj

if __name__ == '__main__':
    response = classify_text('fuck off asshole')
    pprint(response, width=200)
