import gorilla._utils


def decorator(wrapped):
    setattr(gorilla._utils.get_underlying_object(wrapped), 'test_attribute', 'awesome')
    return wrapped
