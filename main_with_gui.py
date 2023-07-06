import os
import base64
import requests
import time
import urllib3
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KEYWORD = "LeagueClientUx.exe"
ACCEPT_ENDPOINT = "/lol-matchmaking/v1/ready-check/accept"
DELAY = 1

BASIC = "Basic"
AUTH_PREFIX = "riot:"
ACCEPT_HEADER = {"Accept": "application/json"}

logging.basicConfig(level=logging.INFO, format="%(message)s")
LOGGER = logging.getLogger(__name__)

class AutoAcceptWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto Accept")
        self.setGeometry(300, 300, 300, 200)

        self.status_label = QLabel("Auto Accept is not running.")
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_auto_accept)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_auto_accept)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.is_running = False

    def start_auto_accept(self):
        if self.is_running:
            return

        self.is_running = True
        self.status_label.setText("Auto Accept is running.")
        self.start_button.setEnabled(False)

        self.run_auto_accept()

    def stop_auto_accept(self):
        self.is_running = False
        self.status_label.setText("Auto Accept is not running.")
        self.start_button.setEnabled(True)

    def get_key_and_port(self):
        try:
            command = f"wmic process where \"caption='{KEYWORD}'\" get Caption,Processid,Commandline"
            result = os.popen(command).read()
            key = result.split("remoting-auth-token=")[1].split('"')[0]
            port = result.split("app-port=")[2].split('"')[0]
            return key, port
        except:
            LOGGER.error("Can't get key and port")
            return None, None

    def run_auto_accept(self):
        key, port = self.get_key_and_port()
        if key is None or port is None:
            LOGGER.error("Auto accept can't run. Be sure League of Legends is running.")
            return
        auth = f"{AUTH_PREFIX}{key}"
        auth_byte = auth.encode("ascii")
        auth_bsf_bytes = base64.b64encode(auth_byte)
        auth_encoded = auth_bsf_bytes.decode("ascii")
        LOGGER.info("Auto accept running.")
        while self.is_running:
            try:
                r = requests.post(
                    url=f"https://127.0.0.1:{port}{ACCEPT_ENDPOINT}",
                    headers={"Authorization": f"{BASIC} {auth_encoded}", **ACCEPT_HEADER},
                    verify=False,
                    data="",
                )
                if r.status_code == 204:
                    LOGGER.info("Auto accept running.")
                time.sleep(DELAY)
            except:
                LOGGER.error("Can't accept the match")
                break
        LOGGER.info("Auto accept stopped.")


if __name__ == "__main__":
    app = QApplication([])
    window = AutoAcceptWindow()
    window.show()
    app.exec_()
