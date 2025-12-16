from passlib.context import CryptContext

# from passlib.exc import InvalidHashError

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"], default="argon2", deprecated="auto"
)


def hash_password(password: str) -> str:
    """Hash a password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a plain-text password matches a hashed password.

    Args:
        plain_password (str): The plain-text password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        return False


__all__ = ["hash_password", "verify_password"]
