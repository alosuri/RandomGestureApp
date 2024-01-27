from PyQt5 import uic
from PyQt5.QtGui import QKeySequence, QIcon, QFontDatabase, QFont

from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QShortcut,
    QPushButton,
    QFrame,
    QScrollArea,
    QDialog,
)

def configuration(parent):
    ## VARIABLES
    uic.loadUi("design.ui", parent)
    parent.previous = []
    parent.image_scale = 0.5
    parent.image_width, parent.image_height = 0, 0
    parent.screen_width, parent.screen_height = parent.size().width(), parent.size().height()
    parent.move_window_press, parent.move_image_press, parent.move_resize_press = 0, 0, 0
    parent.rightClick = False
    parent.angle, parent.side, parent.orginal_image_scale = 0, 1, 1
    parent.path = "null"
    parent.timer_visibility = True
    parent.extensions = ('.bmp', '.gif', 'jpg', '.jpeg', '.png', '.pbm', '.pgm', '.ppm', '.xbm', '.xpm', '.jfif')
    parent.thread={}

    ## WINDOW SETTINGS
    parent.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
    parent.setAttribute(Qt.WA_TranslucentBackground)

    ## WIDGETS
    parent.canva = parent.findChild(QLabel, "Canva")
    parent.canva.setHidden(True)
    parent.canva.setAlignment(Qt.AlignCenter)
    parent.welcome = parent.findChild(QLabel, "WelcomeImage")
    parent.previous_session = parent.findChild(QPushButton, "previous_session")
    parent.previous_session.clicked.connect(lambda: parent.restore_session(str(parent.settings.value("location1")), "location1"))

    parent.previous_session_2 = parent.findChild(QPushButton, "previous_session_2")
    parent.previous_session_2.clicked.connect(lambda: parent.restore_session(str(parent.settings.value("location2")), "location2"))

    if not (parent.settings.contains("location2")):
        parent.previous_session_2.setHidden(True)

    parent.dialog = QDialog()
    parent.dialog.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.Popup)
    parent.grid_lines = parent.findChild(QLabel, "Grid_lines")
    parent.menu_button = parent.findChild(QPushButton, "MenuButton")
    parent.menu_button.setIcon(QIcon("./main.png"))
    parent.menu_button.clicked.connect(parent.show_menu)
    parent.dock = parent.findChild(QFrame, "ScrollFrame")
    parent.dockscroll = parent.findChild(QScrollArea, "Dock")

    # SHORTCUTS
    parent.Grid = QShortcut(QKeySequence("Ctrl+G"), parent)
    parent.Grid.activated.connect(parent.create_grid)
    parent.Grayscale = QShortcut(QKeySequence("Ctrl+T"), parent)
    parent.Grayscale.activated.connect(parent.grayscale)
    parent.Quit = QShortcut(QKeySequence("Ctrl+Q"), parent)
    parent.Quit.activated.connect(QApplication.instance().quit)
    parent.Directory = QShortcut(QKeySequence("Ctrl+O"), parent)
    parent.Directory.activated.connect(parent.file_chooser)
    parent.Ran = QShortcut(QKeySequence("Ctrl+R"), parent)
    parent.Ran.activated.connect(parent.randomizer)
    parent.Zoom_In = QShortcut(QKeySequence('Ctrl+='), parent)
    parent.Zoom_In.activated.connect(parent.on_zoom_in)
    parent.Zoom_Out = QShortcut(QKeySequence('Ctrl+-'), parent)
    parent.Zoom_Out.activated.connect(parent.on_zoom_out)
    parent.Rotate_Right = QShortcut(QKeySequence('Ctrl+]'), parent)
    parent.Rotate_Right.activated.connect(parent.rotate_right)
    parent.Rotate_Left = QShortcut(QKeySequence('Ctrl+['), parent)
    parent.Rotate_Left.activated.connect(parent.rotate_left)
    parent.Next_Pic = QShortcut(QKeySequence('Right'), parent)
    parent.Next_Pic.activated.connect(parent.next_picture)
    parent.Back_Pic = QShortcut(QKeySequence('Left'), parent)
    parent.Back_Pic.activated.connect(parent.back_picture)

    parent.show()