import random

def regularize_str(s):
    if not s:
        return None
    if isinstance(s, str) and len(s) == 0:
        return s
    
    s = str(s)
    words = s.split(' ')
    for i in xrange(len(words)):
        words[i] = words[i].lower().capitalize()
    
    return ' '.join(words)

def ok_response():
    return {'status': 'ok'}

def error_response(reason):
    return {'status': 'error', 'reason': str(reason)}

def get_identifier(strs):
    identifier = ''
    for s in strs:
        if not s: continue
        identifier += str(s)
    identifier = str(hash(identifier))
    return identifier

def cluster(result, filters):
    l = [
        {
            'col1' : [['name', 0.80], ['address', 0.55], ['gender', 0.23]],
            'col47': [['ssn', 0.90], ['race', 0.16]]
        },
        {
            'Name' : [['name', 0.98], ['address', 0.50], ['gender', 0.2]],
            'Continent23': [['marital', 0.68], ['address', 0.67]]
        },
        {
            'fn' : [['name', 0.5], ['age', 0.19]],
            'cool' : [['ip_address', 0.99], ['name', 0.05]]
        },
        {
            'addr': [['address', 0.87], ['ip_address', 0.82]],
            'number': [['ssn', 0.96]]
        },
        {
            'ssn': [['ssn', 1.0], ['age', 0.56]],
            'sex': [['gender', 1.0], ['marital', 0.45]]
        }
    ]
    return random.choice(l)

def reorganize(result, filter):
    score = 0
    for key in result.keys():
        answers = result[key]
        for answer in answers:
            if regularize_str(answer[0]) != regularize_str(filter): continue
            col_score = int(answer[1] * 100)
            score = max(score, col_score)
    return score
