from functools import wraps

from mt.config.schemas import Validator
from mt.lib.errors import MtApiInternalError


def validate_schema(func, schema, arg_key='data'):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            data = kwargs[arg_key]
        except KeyError:
            raise MtApiInternalError(i18n='tbd', message=f'keyword')

        Validator(schema).validate(data)
        return func(*args, **kwargs)

    return wrapped