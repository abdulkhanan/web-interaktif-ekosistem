import base64
import hashlib
import hmac
import secrets


_HASH_PREFIX = "pbkdf2_sha256"
_ITERATIONS = 260000
_SALT_BYTES = 16
_KEY_BYTES = 32


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("utf-8").rstrip("=")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("utf-8"))


def hash_password(password: str) -> str:
    """Hash password dengan PBKDF2-HMAC-SHA256 tanpa dependensi tambahan."""
    if password is None:
        raise ValueError("Password tidak boleh kosong.")

    password = str(password)
    if len(password) < 6:
        raise ValueError("Password minimal 6 karakter.")

    salt = secrets.token_bytes(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _ITERATIONS,
        dklen=_KEY_BYTES,
    )
    return f"{_HASH_PREFIX}${_ITERATIONS}${_b64encode(salt)}${_b64encode(digest)}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verifikasi password terhadap hash PBKDF2 yang tersimpan."""
    if not password or not stored_hash:
        return False

    try:
        prefix, iterations_raw, salt_raw, digest_raw = str(stored_hash).split("$", 3)
        if prefix != _HASH_PREFIX:
            return False

        iterations = int(iterations_raw)
        salt = _b64decode(salt_raw)
        expected_digest = _b64decode(digest_raw)
        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            str(password).encode("utf-8"),
            salt,
            iterations,
            dklen=len(expected_digest),
        )
        return hmac.compare_digest(actual_digest, expected_digest)

    except Exception:
        return False
