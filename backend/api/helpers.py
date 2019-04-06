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
