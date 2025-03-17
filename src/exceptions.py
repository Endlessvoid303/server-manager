import logging

logger = logging.getLogger(__name__)

class BaseError(Exception):
    def __init__(self, message, data):
        if data is None:data = {}
        logger.error(F"`{message}` with data: `{data}`")

class UserAlreadyReviewedError(BaseError):
    def __init__(self, message = "User can't be reviewed twice", data=None):
        super().__init__(message, data)

class PasswordRequirementError(BaseError):
    def __init__(self, message = "Password Requires 9 to 36 characters, must include uppercase and lowercase letters, and numbers", data=None):
        super().__init__(message, data)

class UserExistsError(BaseError):
    def __init__(self, message = "User already exists", data=None):
        super().__init__(message, data)

class MessageNotFoundError(BaseError):
    def __init__(self, message = "Message not found", data=None):
        super().__init__(message, data)

class UserDoesNotExistError(BaseError):
    def __init__(self, message = "User does not exist", data=None):
        super().__init__(message, data)