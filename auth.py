from passlib.context import CryptContext
from crud import get_user_by_username, create_user

# Configurazione hashing (bcrypt è lo standard)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Cripta la password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Confronta password inserita e hash nel DB."""
    return pwd_context.verify(plain_password, hashed_password)

def signup(username, password):
    """Logica di registrazione."""
    hashed_pw = get_password_hash(password)
    return create_user(username, hashed_pw)

def login(username, password):
    """Logica di autenticazione."""
    user = get_user_by_username(username)
    if user and verify_password(password, user.password):
        return user
    return None