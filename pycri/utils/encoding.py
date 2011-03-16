def smart_unicode(s, encoding='utf-8', errors='strict'):
    if isinstance(s, unicode):
        return s

    try:
        if not isinstance(s, basestring,):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                try:
                    s = unicode(str(s), encoding, errors)
                except UnicodeEncodeError:
                    s = ' '.join([smart_unicode(arg, encoding, errors) for arg in s])
        elif not isinstance(s, unicode):
            s = s.decode(encoding, errors)

    except UnicodeDecodeError:
        s = ' '.join([smart_unicode(arg, encoding, errors) for arg in s])

    return s

def smart_str(s, encoding='utf-8', errors='strict'):
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return ' '.join([smart_str(arg, encoding, errors) for arg in s])
            return unicode(s).encode(encoding, errors)

    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s
