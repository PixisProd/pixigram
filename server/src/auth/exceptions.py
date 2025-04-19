class UserAlreadyExistsException(Exception):
    def __str__(self):
        return "A user with such data already exists"