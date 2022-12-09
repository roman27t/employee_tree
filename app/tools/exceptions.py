class InValidException(Exception):
    def __init__(self, status_code: int, code: str, message: str = ''):
        self.code = code
        self.message = message
        self.status_code = status_code
