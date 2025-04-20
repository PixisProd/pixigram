class UserAlreadyExistsException(Exception):
    def __str__(self):
        return "A user with such data already exists"
    

class IncorrectCredentialsException(Exception):
    def __str__(self):
        return "Incorrect login or password"


class UserNotFoundException(Exception):
    def __str__(self):
        return "User not found"
    

class DeactivatedUserException(Exception):
    def __str__(self):
        return "User deactivated"