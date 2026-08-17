
import hashlib

def encrypt_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def decrypt_password(password , hashed_pw):
    entered_hash = hashlib.sha256(password.encode()).hexdigest()

    if entered_hash == hashed_pw:

        return True
    else:

        return False


