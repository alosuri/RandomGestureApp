import os, fnmatch, random, math

from os import walk
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (
    QPixmap,
    QIcon
)
from PyQt5.QtWidgets import (
    QFileDialog,
    QMessageBox, 
    QDialog,
    QPushButton,
    QLabel,
    QVBoxLayout
)

def file_chooser(parent, path_value):
        parent.count = 0
        if path_value == "":
            parent.path = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
        else:
             parent.path = str(path_value)
        if parent.path == '':
            parent.dialog.resize(400, 200)
            layout = QVBoxLayout()

            label = QLabel(parent.dialog)
            label.setText("You haven't selected any folder.")

            button = QPushButton("Ok", parent.dialog)
            button.clicked.connect(lambda: parent.dialog.reject())

            layout.addWidget(label)
            layout.addWidget(button)
            parent.dialog.setLayout(layout)

            parent.dialog.exec_()
            return
        else:
            parent.previous_session.setHidden(True)
            parent.previous_session_2.setHidden(True)
            parent.count_all = len(fnmatch.filter(os.listdir(parent.path), '*.*'))
            parent.all_filenames = next(walk(parent.path), (None, None, []))[2]
            parent.filenames = [file for file in parent.all_filenames if file.lower().endswith(parent.extensions)]
            parent.count = len(parent.filenames)
            parent.randomizer()
            
            if (parent.settings.value('location1') != parent.path and (parent.settings.contains("location1"))):
                parent.settings.setValue('location2', parent.settings.value('location1'))

            parent.settings.setValue('location1', parent.path)
            
        
        parent.canva.setHidden(False)
        parent.welcome.setHidden(True)
        parent.show()

def randomizer(parent):
        if parent.path != "null":
            finished = False
            while not finished:
                randomized_image = random.choice(parent.filenames)
                parent.image_index =  parent.filenames.index(randomized_image)
                parent.image_path = parent.path + "/" + randomized_image
                if (parent.image_path not in parent.previous):
                    parent.display_image()
                    finished = True
                    
        else:
            QMessageBox.information(parent, "Image Viewer", "You don't choose any folder! Press Ctrl + O to choose folder.")

def display_image(parent):
    parent.image_pixmap = QPixmap(parent.image_path)
    parent.image_size = parent.image_pixmap.size()
    parent.image_scaled = parent.image_pixmap.scaled(parent.image_scale * parent.image_size)
    parent.canva.setPixmap(parent.image_scaled)

    parent.angle, parent.side, parent.monochrome = 0, 1, 0
    if parent.image_width >= parent.image_height:
        parent.image_diagonal = parent.image_width
    else:
        parent.image_diagonal = parent.image_height
    parent.image_width = parent.image_pixmap.width()
    parent.image_height = parent.image_pixmap.height()
    parent.image_scale = ((parent.screen_width / parent.image_width) + (parent.screen_height / parent.image_height)) / 2
    parent.orginal_image_scale = parent.image_scale
    parent.previous.append(parent.image_path)
    
    if len(parent.previous) >= parent.count * 0.25:
        parent.previous = []
        parent.previous.append(parent.image_path)

    parent.resize_image()

    parent.canva.resize(int(parent.image_width * parent.image_scale), int(parent.image_height * parent.image_scale))
    parent.canva.move(math.ceil(parent.screen_width //2 - ((parent.image_width * parent.image_scale)// 2)), math.ceil(parent.screen_height // 2 - (parent.image_height * parent.image_scale) // 2))