import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow
import requests



class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_gen_keys.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)
    
    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            
    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        pay_load = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=pay_load)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data["encrypted_message"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encryption Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            
    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        pay_load = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=pay_load)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data["decrypted_message"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText( "Decryption Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            
    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        pay_load = {
            "message": self.ui.txt_info.toPlainText()
        }
        try:
            response = requests.post(url, json=pay_load)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setPlainText(data["signature"])
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            
    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        pay_load = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=pay_load)
            if response.status_code == 200:
                data = response.json()
                print("Dữ liệu phản hồi từ API:", data)  # In ra toàn bộ dữ liệu phản hồi để kiểm tra
                
                # Kiểm tra key 'is_verify' trong phản hồi
                if "is_verify" in data:
                    if data["is_verify"]:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Verification Successful")
                        msg.exec_()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Verification Failed")
                        msg.exec_()
                else:
                    print("Lỗi: 'is_verify' key không có trong phản hồi")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Lỗi: 'is_verify' key không có trong phản hồi")
                    msg.exec_()
            else:
                print("Lỗi khi gọi API")
        except requests.exceptions.RequestException as e:
            print(f"Lỗi: {str(e)}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
