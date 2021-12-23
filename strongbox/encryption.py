from os import urandom
import base64
from hashlib import sha256
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def encrypt_password(fernet: Fernet, password: str) -> str:
    return fernet.encrypt(password.encode()).decode("utf-8")


def generate_hash(vault_password: str) -> str:
    return sha256(vault_password.encode()).hexdigest()


def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password, "utf-8")))
    return key


def decode_salt(encoded_salt: bytes) -> str:
    return encoded_salt.decode("latin-1")


def encode_salt(decoded_salt: str) -> bytes:
    return bytes(decoded_salt, "latin-1")
