import sys
from PyQt5.QtCore import Qt, QUrl, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from flask import Flask, render_template
import threading
import requests
from playsound import playsound
import tkinter as tk
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QDesktopWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import logging
import logging.config
import os
import subprocess
from flask import request, jsonify

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
        time.sleep(1)
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


def create_loading_window():
    # Function to update the "Loading..." text with an animation
    def update_loading_text():
        nonlocal dots
        
        # Update the dots for animation
        if dots == '...':
            dots = ''
        else:
            dots += '.'
        label.config(text="Loading" + dots)
        
        # If the loading is complete, close the window
        if loaded:
            root.quit()  # Close the window
        else:
            # Keep checking until the loading is complete
            root.after(500, update_loading_text)  # Repeat the check every 500 ms

    # Create the main window
    root = tk.Tk()

    # Set the window color to #1E1E1E
    root.configure(bg='#1E1E1E')

    # Remove the window borders
    root.overrideredirect(True)

    # Set the window size (you can adjust the size as needed)
    window_width = 200
    window_height = 100

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to center the window on the screen
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set the window size and position
    root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

    # Create a label widget with the text "Loading..." and set the font and color
    dots = '.'
    label = tk.Label(root, text="Loading" + dots, font=("Helvetica", 24), fg="white", bg="#1E1E1E")
    label.pack(expand=True)

    # Variable to control when the window should close
    global loaded
    loaded = False  # Set this to True when loading is complete

    # Start the animation
    update_loading_text()

    # Simulate some loading operation, then set 'loaded' to True after a delay
    # For demo purposes, we set 'loaded' to True after 5 seconds
    #root.after(5000, lambda: globals().__setitem__('loaded', True))  # Set loaded = True after 5 seconds for demo

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())
    app.run(debug=True)
