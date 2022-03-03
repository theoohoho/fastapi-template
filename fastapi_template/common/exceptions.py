class FastAPITemplateException(Exception):
    pass


class ForbiddenException(FastAPITemplateException):
    def __init__(self, *args: object) -> None:
        self.msg = ""
        super().__init__(self.msg)
