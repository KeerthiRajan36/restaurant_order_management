class AlreadyExistsException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class NotFoundException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class UnauthorizedException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class ForbiddenException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class ValidationException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class BusinessException(Exception):
    def __init__(self, detail: str):
        self.detail = detail