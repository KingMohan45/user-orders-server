import shortuuid

def get_uuid():
    """Generate an uuid for all the primary keys."""
    pk = shortuuid.uuid()[:8]
    return str(pk)
