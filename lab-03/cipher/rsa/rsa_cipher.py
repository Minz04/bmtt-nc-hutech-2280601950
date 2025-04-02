import rsa, os

# Đảm bảo thư mục chứa các khóa tồn tại
if not os.path.exists('cipher/rsa/keys'):
    os.makedirs('cipher/rsa/keys')

class RSACipher:
    def __init__(self):
        pass

    # Phương thức tạo khóa RSA (khóa công khai và khóa riêng)
    def generate_keys(self):
        (public_key, private_key) = rsa.newkeys(1024)
        # Lưu khóa công khai
        with open('cipher/rsa/keys/publicKey.pem', 'wb') as p:
            p.write(public_key.save_pkcs1('PEM'))
        # Lưu khóa riêng
        with open('cipher/rsa/keys/privateKey.pem', 'wb') as p:
            p.write(private_key.save_pkcs1('PEM'))

    # Phương thức tải khóa RSA (khóa công khai và khóa riêng)
    def load_keys(self):
        with open('cipher/rsa/keys/publicKey.pem', 'rb') as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())
        with open('cipher/rsa/keys/privateKey.pem', 'rb') as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())
        return private_key, public_key

    # Phương thức mã hóa một thông điệp bằng khóa công khai
    def encrypt(self, message, key):
        try:
            return rsa.encrypt(message.encode('utf-8'), key)
        except Exception as e:
            print(f"Lỗi mã hóa: {e}")
            return None

    # Phương thức giải mã một thông điệp đã mã hóa bằng khóa riêng
    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('utf-8')
        except Exception as e:
            print(f"Lỗi giải mã: {e}")
            return False

    # Phương thức ký một thông điệp bằng khóa riêng
    def sign(self, message, key):
        try:
            return rsa.sign(message.encode('utf-8'), key, 'SHA-1')
        except Exception as e:
            print(f"Lỗi ký: {e}")
            return None

    # Phương thức xác thực chữ ký của một thông điệp bằng khóa công khai
    def verify(self, message, signature, key):
        try:
            # Kiểm tra chữ ký
            rsa.verify(message.encode('utf-8'), signature, key)
            return True
        except rsa.VerificationError:
            print("Xác thực chữ ký không thành công")
            return False
        except Exception as e:
            print(f"Lỗi xác thực: {e}")
            return False
