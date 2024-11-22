import sys
from PyQt5 import QtWidgets
from forgot_password import Ui_ForgotPasswordDialog
import requests

def forgot_password(email):
    url = 'http://127.0.0.1:8000/forgot_password'
    data = {
        "email": email
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print("Failed to send password reset email")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ForgotPasswordDialog = QtWidgets.QDialog()
    ui = Ui_ForgotPasswordDialog()
    ui.setupUi(ForgotPasswordDialog)

    # Connect button to forgot password function
    ui.confirmButton.clicked.connect(lambda: forgot_password(
        ui.emailInput.text()
    ))

    ForgotPasswordDialog.show()
    sys.exit(app.exec_())
