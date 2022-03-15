# StrongBox Security :closed_lock_with_key:

StrongBox encrypts passwords before storing them on the given database. It uses
[Fernet](https://cryptography.io/en/latest/fernet/) module (a Python implementation
of symmetric authenticated cryptography) to achieve this.

```python
def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password, "utf-8")))
    return key
```
Function extracted from [encryption.py](https://github.com/dylannalex/strongbox) file.

## :key: Passwords storage

All passwords are stored in _vaults_. Each _vault_ has a _vault_id_, a _vault_salt_
and a _hashed_vault_password_.

The _hashed_vault_password_ is the _vault_password_ hashed, which is a string given by
the user which, combined with the _vault_salt_, is used for encrypting and decrypting
the password in a _vault_.

```python
def generate_hash(vault_password: str) -> str:
    return sha256(vault_password.encode()).hexdigest()
```

- _vault_password_ should be a long string of characters (ideally random)
- Two _vaults_ cannot have the same _vault_password_

When you enter a _vault_password_, StrongBox hashes it and compares it with all vaults
_hashed_vault_password_.

If it matches any then it access to that _vault_, and uses the _vault_password_ (salted)
to decrypt all passwords stored in that _vault_ and to encrypt all new passwords stored.

If it does not find any matches StrongBox will ask if the user wants to create a
new _vault_ with that _vault_password_. If the user accepts, a random _vault_salt_ and
_vault_id_ is generated and stored, beside the _hashed_vault_password_.