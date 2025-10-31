from passlib.context import CryptContext

# Use bcrypt_sha256 to avoid the native bcrypt 72-byte password limit.
pwd_context = CryptContext(schemes=['bcrypt_sha256'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)