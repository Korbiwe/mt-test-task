class MtError(Exception):
    def __init__(self, i18n, message, **kwargs):
        self.i18n = i18n
        self.message = message
        self.params = kwargs

    @property
    def json_friendly(self):
        return {
            'i18n': self.i18n,
            'message': self.message,
            'params': self.params
        }


class MtApiError(MtError):
    pass


class MtApiUserError(MtApiError):
    pass


class MtApiInternalError(MtApiError):
    pass


class MtApiNotFound(MtApiUserError):
    pass


class MtUnauthorized(MtApiUserError):
    pass


class MtForbidden(MtApiUserError):
    pass
