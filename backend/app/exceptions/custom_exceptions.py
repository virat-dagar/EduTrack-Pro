"""Custom application exceptions."""


class AppException(Exception):
    """Base class for expected application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "APP_ERROR",
        errors: list[dict[str, str]] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.errors = errors or []
        super().__init__(message)


class AuthenticationError(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message, status_code=401, error_code="AUTHENTICATION_ERROR")


class AuthorizationError(AppException):
    """Raised when a user lacks permission."""

    def __init__(self, message: str = "You do not have permission to perform this action.") -> None:
        super().__init__(message, status_code=403, error_code="AUTHORIZATION_ERROR")


class NotFoundError(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found.") -> None:
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class ConflictError(AppException):
    """Raised when a unique or business constraint is violated."""

    def __init__(self, message: str = "Resource conflict.") -> None:
        super().__init__(message, status_code=409, error_code="CONFLICT")


class BusinessRuleError(AppException):
    """Raised when a business rule is violated."""

    def __init__(self, message: str = "Business rule violation.") -> None:
        super().__init__(message, status_code=400, error_code="BUSINESS_RULE_ERROR")
