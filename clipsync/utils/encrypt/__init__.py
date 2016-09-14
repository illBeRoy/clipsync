import Crypto.Cipher.AES


class Encrypt(object):

    def __init__(self, cipher, secret):
        self._secret = secret
        self._cipher = cipher

    def encrypt(self, value):
        normalized_value = Encrypt._normalize_length_to_power_of_16(value)
        return self._cipher.encrypt(normalized_value)

    def decrypt(self, value):
        decrypted_value = self._cipher.decrypt(value)
        return decrypted_value.strip()

    @staticmethod
    def _normalize_length_to_power_of_16(string):
        margin_from_16 = 16 - (len(string) % 16)
        margin_from_16 %= 16

        normalize_string = '{0}{1}'.format(string, ' ' * margin_from_16)

        return normalize_string

    @staticmethod
    def create(secret):
        normalized_secret = Encrypt._normalize_length_to_power_of_16(secret)[:16]
        cipher = Crypto.Cipher.AES.new(normalized_secret)
        return Encrypt(cipher, secret)
