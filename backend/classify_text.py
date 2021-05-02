from transformers import BertTokenizer, BertForSequenceClassification
import torch
from common import MODEL_PATH, CORONAVIRUS_MODEL_PATH
from pprint import pprint


path = CORONAVIRUS_MODEL_PATH
model = BertForSequenceClassification.from_pretrained(path)
tokenizer = BertTokenizer.from_pretrained(path)
model.eval()
model_identifier = path


def get_length(input_ids):
    length = 0
    for input_id in input_ids:
        if input_id == 0:
            break
        else:
            length += 1
    return length

def get_tokens(input_ids, text_length):
    input_ids = input_ids[:text_length]
    return tokenizer.convert_ids_to_tokens(input_ids)

def get_rationales(rationales, text_length):
    rationales = rationales[:text_length]
    rationales = [round(r.item(), 2) for r in rationales]
    return rationales

def classify_text(text, verbose=False):
    response = {
        'status': 'fail',
        'predicted_label': -1,
        'model_identifier': model_identifier,
        'rationale': [],
        'tokens': [],
        'class_prob': []
    }
    tokenized_text = tokenizer.encode_plus(text,
                                    max_length=512,
                                    add_special_tokens=True,
                                    pad_to_max_length=True,
                                    padding_side='right',
                                    return_tensors='pt',
                                    return_token_type_ids=True,
                                    return_attention_mask=True)

    input_ids = tokenized_text['input_ids']
    token_type_ids = tokenized_text['token_type_ids']
    attention_mask = tokenized_text['attention_mask']
    special_text_length = attention_mask.sum()
    non_special_text_length = special_text_length -1

    non_special_attention_mask =attention_mask.clone()
    non_special_attention_mask[:,0] = 0.0
    # non_special_attention_mask[:,special_text_length-1] = 0.0

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            token_type_ids=token_type_ids,
            attention_mask=attention_mask
        )
        logits, hidden_states_output, attention_mask_output = outputs

        overall_mean = torch.zeros_like(input_ids).float()
        variance_sum = torch.tensor(0.0)
        for layer_num, attention_layer in enumerate(attention_mask_output):
            if verbose:print('layer',layer_num)
            normalized = masked_softmax(attention_layer[:,:,0,:].mean(dim=1), non_special_attention_mask, dim=1) * non_special_text_length

            # layer_agg = attention_layer[:,:,0,:].mean(dim=1) #mean across heads for [cls] token
            # attention_mask[:,0] = 0
            normalized_mean = masked_mean(normalized, mask=non_special_attention_mask) #mean across tokens
            if verbose:print('\tmean:',normalized_mean)
            variance = masked_mean((normalized -normalized_mean).abs(), mask=non_special_attention_mask)
            variance_sum += variance
            if verbose: print('\tvariance:',variance)
            if verbose:print('\tNormalized mean across heads:',normalized[:,:20])
            # if verbose:print('\tNormalized:',normalized_layer_mean_mean[:,:20])
            overall_mean += normalized * variance

        overall_mean /= variance_sum

        if verbose:print('Overall mean')
        if verbose:print(overall_mean[:,:20])

        # best_layer = 9
        # best_head = 9
        # attention_layer = attention_mask_output[best_layer]
        # rationales = attention_layer[0][best_head][0]  # attention of [sentence, head, cls] token
        rationales = overall_mean[0]

        special_text_length = get_length(input_ids[0])
        response['predicted_label'] = torch.argmax(logits[0]).item()
        response['tokens'] = get_tokens(input_ids[0], special_text_length)
        response['rationale'] = get_rationales(rationales, special_text_length)
        response['model_identifier'] = model_identifier
        response['class_prob'] = torch.softmax(logits[0], dim=0).tolist()
        response['status'] = 'success'

    return response

def masked_softmax(t, mask, dim=None):
    exped = torch.exp(t)
    r= exped/torch.sum(exped * mask.float(), dim=dim)
    return r


def masked_mean(t, mask, dim=None):
    '''
	Calculate mean of only masked elements
	:param t: tensor
	:param mask: tensor of same shape as 2
	:param dim: optional dimension to perform mean over
	:return:
	'''
    mask = mask.float()
    # iprint(mask)
    if mask.mean() == 0:  # Otherwise we get a 0/0 NaN
        return mask.mean()
    else:
        if dim is None:
            return torch.sum(t * mask) / torch.sum(mask)
        else:
            return torch.sum(t * mask, dim) / torch.sum(mask, dim)



if __name__ == '__main__':

    response = classify_text('fuck off asshole')
    pprint(response, width=200)
    print('****************************************')

    response = classify_text('fuck off asshole fuck off asshole')
    pprint(response, width=200)
    print('****************************************')


    response = classify_text('i like ducks')
    pprint(response, width=200)
    print('****************************************')


    response = classify_text('i like ducks i like ducks')
    pprint(response, width=200)
    print('****************************************')


    response = classify_text('fuck off asshole i did not ask you to comment on my ideas')
    pprint(response, width=200)
    print('****************************************')


    response = classify_text('i did not ask you to comment on my ideas')
    pprint(response, width=200)
    print('****************************************')


    response = classify_text('i did not ask you to comment on my ideas so fuck off')
    pprint(response, width=200)
    print('****************************************')



pass
