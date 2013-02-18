def str_conv(s, encoding='utf-8', errors='strict'):
    """Method for easy string convertion to proper encoding"""
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                return ' '.join([str_conv(arg, encoding, errors) for arg in s])
            return unicode(s).encode(encoding, errors)

    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s
