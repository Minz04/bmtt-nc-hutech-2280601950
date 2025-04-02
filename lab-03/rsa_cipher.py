import sys
import os  
import requests

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_MainWindow 


class RSAGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.btn_gen_keys.clicked.connect(self.generate_keys)
        self.ui.btn_encrypt.clicked.connect(self.encrypt_message)
        self.ui.btn_decrypt.clicked.connect(self.decrypt_message)
        self.ui.btn_sign.clicked.connect(self.sign_message)
        self.ui.btn_verify.clicked.connect(self.verify_signature)

    def generate_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate-keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                QMessageBox.information(self, "Success", "Keys generated successfully")
            else:
                QMessageBox.critical(self, "Error", f"Server returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def encrypt_message(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_input_message.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_encrypted_message.setText(data['encrypted_message'])
                QMessageBox.information(self, "Success", "Message encrypted successfully")
            else:
                QMessageBox.critical(self, "Error", f"Server returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def decrypt_message(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_encrypted_message.toPlainText(),
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_decrypted_message.setText(data['decrypted_message'])
                QMessageBox.information(self, "Success", "Message decrypted successfully")
            else:
                QMessageBox.critical(self, "Error", f"Server returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def sign_message(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_message_to_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_signature.setText(data['signature'])
                QMessageBox.information(self, "Success", "Message signed successfully")
            else:
                QMessageBox.critical(self, "Error", f"Server returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def verify_signature(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_message_to_sign.toPlainText(),
            "signature": self.ui.txt_signature.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data['verified']:
                    QMessageBox.information(self, "Success", "Signature verified successfully")
                else:
                    QMessageBox.warning(self, "Failed", "Signature verification failed")
            else:
                QMessageBox.critical(self, "Error", f"Server returned status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))


def suppress_qt_warnings():
    os.environ["QT_LOGGING_RULES"] = "qt.qpa.fonts=false"


if __name__ == "__main__":
    suppress_qt_warnings()
    app = QApplication(sys.argv)
    window = RSAGUI()
    window.show()
    sys.exit(app.exec_())
