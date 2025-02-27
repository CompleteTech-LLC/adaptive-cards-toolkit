"""Custom exceptions for the adaptive cards toolkit."""

class CardValidationError(Exception):
    """Raised when card validation fails."""
    
    def __init__(self, message, details=None):
        self.message = message
        self.details = details or []
        super().__init__(self.message)


class DeliveryError(Exception):
    """Raised when card delivery fails."""
    
    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class GenerationError(Exception):
    """Raised when card generation fails."""
    
    def __init__(self, message, details=None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
