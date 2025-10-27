from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class AESEncryption:
    def __init__(self):
        self.key = get_random_bytes(16)
    
    def encrypt_message(self, message):
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
        encrypted_data = cipher.nonce + tag + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_message(self, encrypted_data):
        try:
            data = base64.b64decode(encrypted_data)
            nonce = data[:16]
            tag = data[16:32]
            ciphertext = data[32:]
            
            cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            decrypted = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted.decode('utf-8')
        except Exception as e:
            return f"Decryption error: {str(e)}"