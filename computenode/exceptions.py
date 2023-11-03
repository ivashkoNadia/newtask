class Error(Exception):
    def __init__(self, message):
        super().__init__(message)


class MaxIterationError(Error):
    def __init__(self, max_iterations):
        message = f"Max iterations number exceed: {max_iterations}"
        super().__init__(message)


class CancelledError(Error):
    def __init__(self):
        message = f"Task has been cancelled"
        super().__init__(message)
