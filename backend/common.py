import time
import praw

MODEL_PATH = '/home/rajat/repos/reddit_toxicity_classifier/output_512_modern/'
CORONAVIRUS_MODEL_PATH = '/home/rajat/repos/reddit_toxicity_classifier/output_coronavirus_both'

SUBTASK_TYPES = {
    'toxic_hl': {
        'show_highlight': True
    },
    'toxic_no_hl': {
        'show_highlight': False
    },
    'all': {
        'show_highlight': False
    }
}
TOXIC_HL = 'toxic_hl'
TOXIC_NO_HL = 'toxic_no_hl'
ALL = 'all'

TOXIC = 'toxic'
NON_TOXIC = 'nontoxic'
DEFAULT = 'none'
SEPARATOR = '-#-'

def process_rationales_and_tokens(tokens, rationales):
    new_tokens, new_rationales = [], []
    for token, rationale in zip(tokens, rationales):
        if token == '[CLS]' or token == '[SEP]':
            pass
        elif token[:2] == '##':
            new_tokens[-1] = new_tokens[-1] + token[2:]
            new_rationales[-1] = new_rationales[-1] + rationale
        else:
            new_tokens += [token]
            new_rationales += [rationale]
    return new_tokens, new_rationales

def fill_highlight_type(zs, tokens, obj, threshold, row, subtask_type):
    length = len(zs)
    #topk = int((threshold * length))
    #sorted_attn_value = sorted(zs, reverse=True)
    threshold_attn = 1.0
    for idx, (token, z) in enumerate(zip(tokens, zs)):
        highlight_type = DEFAULT
        if SUBTASK_TYPES.get(subtask_type) and SUBTASK_TYPES.get(subtask_type).get('show_highlight') and z >= threshold_attn:
            highlight_type = TOXIC
            #topk -= 1
        obj['rationale'].append({
            'id': obj['unique_id'] + SEPARATOR + str(idx),
            'text': token,
            'highlightType': highlight_type,
            'modifiedAt': int(time.time() * 1000)
        })

def get_response_object(row, subtask_type, threshold=0.2):
    tokens = row['tokens']
    zs = row['rationale']
    if zs is not None and tokens is not None:
        tokens, zs = process_rationales_and_tokens(tokens, zs)
    str_task_id = '0'
    str_comment_id = str(row.get('id'))
    if row.get('task_id') is not None:
        str_task_id = str(row['task_id'])

    obj = {
        'comment_id': str_comment_id,
        'unique_id': str_task_id + ',' + str_comment_id,
        'task_id': str_task_id,
        'rationale': [],
        'raw_text': row['raw_text'],
        'source_identifier': row['source_identifier'],
        'source': row['source'],
        'comment_url': '',
        'created_at': '',
        'author_icon_img': '',
        'author_name': '',
        'predicted_label': row.get('predicted_label'),
        'initial_time': time.time()
    }
    if row['data'] is not None:
        obj['created_at'] = row['data'].get('created_at')
        obj['author_icon_img'] = row['data'].get('author_icon_img')
        obj['comment_url'] = 'https://www.reddit.com' + row['data'].get('comment_url')
        obj['author_name'] = row['data'].get('author_name')

    if zs is not None and len(zs) == len(tokens):
        fill_highlight_type(zs, tokens, obj, threshold, row, subtask_type)
    return obj

def obtain_reddit_instance():
    reddit = praw.Reddit(client_id='J6CT1UgxdzHgaQ', client_secret='ssDGkXdCVvmjSHElltyazhSRgcY', username='DetoxifyBot', password='machineintheloop@7066',  user_agent='bot')
    return reddit
