from typing import Any


class FastAPITemplateException(Exception):
    pass


class ForbiddenException(FastAPITemplateException):
    def __init__(self, *args: object) -> None:
        self.msg = ""
        super().__init__(self.msg)


class InvalidID(FastAPITemplateException):
    pass


class UserAlreadyExists(FastAPITemplateException):
    pass


class UserNotExists(FastAPITemplateException):
    pass


class UserInactive(FastAPITemplateException):
    pass


class UserAlreadyVerified(FastAPITemplateException):
    pass


class InvalidVerifyToken(FastAPITemplateException):
    pass


class InvalidResetPasswordToken(FastAPITemplateException):
    pass


class InvalidPasswordException(FastAPITemplateException):
    def __init__(self, reason: Any) -> None:
        self.reason = reason
