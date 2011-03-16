def filesize(bytes):
    """Calculate human readable sive from given bytes"""
    if not isinstance(bytes, float):
        bytes = float(bytes)
    for x in ['bytes','KB','MB','GB','TB', 'PB', 'EB']:
        if bytes < 1024.0:
            return "{0:3.1f}{1}".format(bytes, x)
        bytes /= 1024.0
