class AuthError(Exception):
    def __init__(self, description, code):
        self.description = description
        self.code = code


class EmptyEntityError(Exception):
    def __init__(self, description, code):
        self.description = description
        self.code = code
