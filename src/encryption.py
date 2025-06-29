import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

class AESCipher:
    def __init__(self, password):
        self.password = password.encode()
        
    def _derive_key(self, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key
    
    def encrypt(self, message):
        try:
            salt = os.urandom(16)
            key = self._derive_key(salt)
            f = Fernet(key)
            encrypted_message = f.encrypt(message.encode())
            result = base64.b64encode(salt + encrypted_message).decode()
            return result
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt(self, encrypted_message):
        try:
            encrypted_data = base64.b64decode(encrypted_message.encode())
            salt = encrypted_data[:16]
            encrypted_msg = encrypted_data[16:]
            key = self._derive_key(salt)
            f = Fernet(key)
            decrypted_message = f.decrypt(encrypted_msg).decode()
            return decrypted_message
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
