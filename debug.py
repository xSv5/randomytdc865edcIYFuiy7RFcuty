import sys
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import threading
import requests
import time
import logging
import os

debug_html = requests.get("https://github.com/xSv5/randomytdc865edcIYFuiy7RFcuty/raw/refs/heads/main/debug.html").text

global loaded
loaded = False

# BrowserWindow class with added top bar and dragging functionality
class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a main widget to hold the layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Create a vertical layout with no margins or padding
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove layout margins
        layout.setSpacing(0)  # Remove spacing between widgets

        # Create the small bar at the top
        self.top_bar = QWidget(self)
        self.top_bar.setFixedHeight(10)  # Height of the bar
        self.top_bar.setStyleSheet("background-color: #fc0303; border: none;")  # Style the bar with a gray color
        layout.addWidget(self.top_bar)

        # Create the QWebEngineView object
        self.browser = QWebEngineView(self)
        self.browser.setUrl(QUrl("http://localhost:5000/debug"))
        self.browser.setStyleSheet("background-color: black; border: none; margin: 0; padding: 0;")  # Remove any extra space

        # Add the browser view to the layout
        layout.addWidget(self.browser)

        # Set the window size and position (smaller window)
        self.setGeometry(100, 100, 400, 250)  # Adjusted size for smaller window

        # Set the window to be borderless and without a title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Initially hide the window
        self.hide()

        # Connect the loadFinished signal to a slot
        self.browser.loadFinished.connect(self.on_page_loaded)

        # Track the initial position for dragging
        self.dragging = False
        self.drag_start_pos = QPoint()



        self.center_window()

    def center_window(self):
        # Get the screen's available geometry
        screen_geometry = QDesktopWidget().availableGeometry()

        # Calculate the position to center the window
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Move the window to the calculated position

        self.move(x, y)
        import time
        time.sleep(.1)
        self.raise_()  # Brings the window to the front
        self.activateWindow()  # Makes the window the active window

        # Set the window to always stay on top
        #self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def on_page_loaded(self):
        logging.debug("Server Page loaded")
        self.show() 
        global loaded
        loaded = True
        self.raise_()
        self.activateWindow()

        #self.show()  # Show the window after the page is fully loaded

    # Handle mouse press event to start dragging
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_pos = event.globalPos() - self.pos()
            event.accept()

    # Handle mouse move event to drag the window
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_start_pos)
            event.accept()

    # Handle mouse release event to stop dragging
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

def check_debug():
    while True:
        time.sleep(.23)
        # Get the path to the config file
        roaming_app_data = os.environ.get('APPDATA')
        config_path = os.path.join(roaming_app_data, 'sm_001.config')

        # Read the config file to check the debug value
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                for line in file:
                    if 'debug-checkbox=' in line:
                        global debug_checkbox
                        debug_checkbox = line.split('=')[1].strip().lower() == 'true'

        # Exit if debug is false
        if not debug_checkbox:
            os._exit(0)


def run_config():
    while True:
        time.sleep(.5)
        roaming_app_data = os.environ.get('APPDATA')
        sm_PATH = os.path.join(roaming_app_data, 'sm_001.config')

        # Open the file and read its contents
        with open(sm_PATH, 'r') as file:
            lines = file.readlines()

        # Check for 'running=false' and exit if found
        for line in lines:
            if 'running=false' in line:
                os._exit(0)


if __name__ == '__main__':
    no1 = threading.Thread(target=check_debug)
    no1.start()
    no2 = threading.Thread(target=run_config)
    no2.start()
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())
    app.run(debug_checkbox=True)
