from functools import wraps
from utils import consts, rights


def version_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = kwargs['request']
        db = kwargs['db']
        version = request.headers.get(consts.Consts.HEADER_VERSION, None)
        rights.is_version_supported(db, version)
        return func(*args, **kwargs)
    return wrapper


def permission(permission_string):
    def decorator_auth(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs['request']
            db = kwargs['db']
            token = rights.retrieve_token_from_header(request)
            if permission_string == consts.Consts.PERMISSION_ADMIN:
                rights.is_admin(db, token)
            elif permission_string == consts.Consts.PERMISSION_ADMIN_OR_USER_OWNER:
                user_id = kwargs['user_id']
                rights.is_admin_or_user_owner(db=db, token=token, user_id=user_id)
            elif permission_string == consts.Consts.PERMISSION_ADMIN_OR_ITEM_OWNER:
                item_id = kwargs['item_id']
                rights.is_admin_or_item_owner(db=db, token=token, item_id=item_id)
            elif permission_string == consts.Consts.PERMISSION_USER:
                rights.is_authenticated(db=db, token=token)
            return func(*args, **kwargs)
        return wrapper
    return decorator_auth
