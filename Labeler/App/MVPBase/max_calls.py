# https://stackoverflow.com/questions/20923748/python-decorator-to-limit-number-of-calls

#
# Doesn't work as calls seems to be global on each object
#
from functools import wraps

def max_calls(num):
    """Decorator which allows its wrapped function to be called `num` times"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            calls = getattr(wrapper, 'calls', 0)
            calls += 1
            if calls > num:
                raise Warning(f"Maximum calls for {func} is {num}")
            setattr(wrapper, 'calls', calls)
            return func(*args, **kwargs)
        setattr(wrapper, 'calls', 0)
        return wrapper
    return decorator