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
    return {'col1' : [['Name', 0.80], ['Address', 0.55]],
            'col47': [['Ssn', 0.90]]
            }

def reorganize(result, filter):
    score = 0
    for key in result.keys():
        answers = result[key]
        for answer in answers:
            if regularize_str(answer[0]) != regularize_str(filter): continue
            col_score = int(answer[1] * 100)
            score = max(score, col_score)
    return score
