from passlib.context import CryptContext

# Configuración para encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Genera el hash seguro de la contraseña"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verifica si una contraseña coincide con su hash"""
    return pwd_context.verify(password, hashed)
