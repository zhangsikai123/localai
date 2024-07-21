class NotFoundException(Exception):
    def __init__(self, msg, error_type=None):
        Exception.__init__(self, msg)
        self.error_type = error_type
