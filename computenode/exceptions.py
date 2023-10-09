class ExceptionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class MaxIterationError(ExceptionError):
    def __init__(self, max_iterations):
        message = f"Досягнуто максимальну кількість ітерацій: {max_iterations}"
        super().__init__(message)



