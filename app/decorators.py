from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


# use functools.wraps to add decorators
# f is functions that could add decorators
# more knowledge about decorators is needed
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
