import sys, math, time

from scripts.rendering_images import file_chooser, randomizer, display_image
from scripts.configuration import configuration
from scripts.menu import Ui_Dialog as Menu

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import (
    QPixmap,
    QTransform,
    QPainter,
    QPen,
    QColor,
    QIcon,
)

from PyQt5.QtCore import Qt, QPoint, QSettings

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QColorDialog,
    QMenu,
)

class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.settings = QSettings("settings.ini", QSettings.IniFormat)
        configuration(self)

        self.previous_session.setText(self.settings.value("location1", "Previous session not found..."))
        self.previous_session_2.setText(self.settings.value("location2"))
        
    def file_chooser(self):
        file_chooser(self, "")

    def randomizer(self):
        randomizer(self)

    def display_image(self):
        display_image(self)

    def restore_session(self, path, button):
        if (self.settings.contains(button)):
            file_chooser(self, path)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            self.oldPosition = event.globalPos()
            self.move_window_press = 1
            
        if event.button() == QtCore.Qt.LeftButton and not QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            self.oldImagePosition = event.globalPos()
            self.move_image_press = 1

        if event.button() == QtCore.Qt.RightButton and QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            self.move_resize_press = 1
            self.rdragx = event.x()
            self.rdragy = event.y()        
            self.currentx = self.width()
            self.currenty = self.height()
            self.rightClick = True

    def mouseMoveEvent(self, event):
        if self.move_window_press == 1:
            delta_move = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta_move.x(), self.y() + delta_move.y())
            self.oldPosition = event.globalPos()

        if self.move_image_press == 1:
            if self.path != "null":
                image_delta = QPoint(event.globalPos() - self.oldImagePosition)
                QApplication.setOverrideCursor(Qt.ClosedHandCursor)
                self.canva.move(self.canva.x() + image_delta.x(), self.canva.y() + image_delta.y())
                self.oldImagePosition = event.globalPos()
                self.move_image_press == 0

        if self.rightClick == True:
            if self.path != "null":
                x = max(self.minimumWidth(), 
                    self.currentx + event.x() - self.rdragx)
                y = max(self.minimumHeight(), 
                    self.currenty + event.y() - self.rdragy)

                self.resize(x, y)

                self.screen_width = self.size().width()
                self.screen_height = self.size().height()

                self.welcome.move(math.ceil(self.screen_width //2 - (self.welcome.width()) // 2), math.ceil(self.screen_height // 2 - (self.welcome.height() // 2)))

                self.canva.resize(int(self.image_width * self.image_scale), int(self.image_height * self.image_scale))
                self.canva.move(math.ceil(self.screen_width //2 - ((self.image_width * self.image_scale)// 2)), math.ceil(self.screen_height // 2 - (self.image_height * self.image_scale) // 2))
                self.last_x, self.last_y = x, y

    def mouseReleaseEvent(self, event):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.rightClick = False
        self.move_image_press = 0
        self.move_window_press = 0

    def wheelEvent(self, event):
        if self.path != "null":
            if event.angleDelta().y() > 0:
                self.on_zoom_in()
            else:
                self.on_zoom_out()

    def on_zoom_in(self):
        if self.path != "null":
            self.image_scale *=  1.10
            if self.image_scale >= self.orginal_image_scale * 5:
                self.image_scale = self.orginal_image_scale * 5
            self.resize_image()

    def on_zoom_out(self):
        if self.path != "null":
            self.image_scale /= 1.10
            self.resize_image()
        if self.image_scale <= self.orginal_image_scale / 3:
            self.image_scale = self.orginal_image_scale / 3

    def resize_image(self):
        if self.path != "null":
            self.image_width = self.image_pixmap.width()
            self.image_height = self.image_pixmap.height()
            self.image_scaled = self.image_pixmap.scaled(int((self.image_width * self.image_scale)), int((self.image_height * self.image_scale)))
            self.image_rotated = self.image_scaled.transformed(QTransform().rotate(self.angle),QtCore.Qt.SmoothTransformation)
            self.image_reflected = self.image_rotated.transformed(QTransform().scale(self.side, 1))
            self.canva.setPixmap(self.image_reflected)

            if self.angle == 0 or self.angle == 360:
                self.canva.resize(int(self.image_width * self.image_scale), int(self.image_height * self.image_scale))
                self.canva.move(math.ceil(self.screen_width //2 - ((self.image_width * self.image_scale)// 2)), math.ceil(self.screen_height // 2 - (self.image_height * self.image_scale) // 2))

            else:
                self.canva.resize(int(self.image_diagonal * self.image_scale), int(self.image_diagonal * self.image_scale))
                self.canva.move(math.ceil(self.screen_width //2 - ((self.image_diagonal * self.image_scale)// 2)), math.ceil(self.screen_height // 2 - (self.image_diagonal * self.image_scale) // 2))


    def rotate_right(self):
        if self.side > 0:
            self.angle += 45
            if self.angle == 360:
                self.angle = 0
        else:
            if self.angle == 0:
                self.angle = 360
            self.angle -= 45

        self.rotate_image()

    def rotate_left(self):
        if self.side > 0:
            if self.angle == 0:
                self.angle = 360
            self.angle -= 45
        else:
            self.angle += 45
            if self.angle == 360:
                self.angle = 0
        self.rotate_image()

    def rotate_image(self):
        if self.path != "null":
            if self.angle == [0, 90, 180, 270, 360]:
                self.image_width = self.image_pixmap.width()
                self.image_height = self.image_pixmap.height()
                self.canva.resize(int(self.screen_width * self.image_scale), int(self.image_height * self.image_scale))
            else:
                self.image_width = self.image_pixmap.width()
                self.image_height = self.image_pixmap.height()
                self.image_diagonal = math.sqrt((math.pow(self.image_width, 2)) * (math.pow(self.image_height, 2)))
                self.canva.resize(int(self.image_diagonal * self.image_scale), int(self.image_diagonal * self.image_scale))

            size = self.image_pixmap.size()
            self.image_scaled = self.image_pixmap.scaled(self.image_scale * size)
            self.image_rotated = self.image_scaled.transformed(QTransform().rotate(self.angle),QtCore.Qt.SmoothTransformation)
            self.image_reflected = self.image_rotated.transformed(QTransform().scale(self.side, 1))
            self.canva.setPixmap(self.image_reflected)
            self.canva.move(math.ceil(self.screen_width //2 - ((self.image_diagonal * self.image_scale)// 2)), math.ceil(self.screen_height // 2 - (self.image_diagonal * self.image_scale) // 2))

    def reflect(self):
        if self.path != "null":
            if self.side < 0:
                self.side = 1
            elif self.side > 0:
                self.side = -1
            size = self.image_pixmap.size()
            self.image_rotated = self.image_scaled.transformed(QTransform().rotate(self.angle),QtCore.Qt.SmoothTransformation)
            self.image_reflected = self.image_rotated.transformed(QTransform().scale(self.side, 1))
            self.canva.setPixmap(self.image_reflected)

    def next_picture(self):
        if self.path != "null":
            if int(self.image_index) + 1 < self.count:
                self.image_index = int(self.image_index) + 1
            else:
                self.image_index = 0

            self.image_path = self.path + "/" + self.filenames[self.image_index]
            self.display_image()

    def back_picture(self):
        if self.path != "null":
            if (self.image_index) != 0:
                self.image_index = int(self.image_index) - 1
            else:
                self.image_index = (self.count) - 1

            self.image_path = self.path + "/" + self.filenames[self.image_index]
            self.display_image()

    def grayscale(self):
        if self.path != "null":
            if self.monochrome == 0:
                self.image_pixmap = QPixmap(self.image_path)
                Q_image = QtGui.QPixmap.toImage(self.image_pixmap)
                grayscale = Q_image.convertToFormat(QtGui.QImage.Format_Grayscale8)
                image = QtGui.QPixmap.fromImage(grayscale)
                self.image_pixmap = QPixmap(image)
                self.image_size = self.image_pixmap.size()
                self.image_scaled = self.image_pixmap.scaled(self.image_scale * self.image_size)
                self.image_rotated = self.image_scaled.transformed(QTransform().rotate(self.angle),QtCore.Qt.SmoothTransformation)
                self.image_reflected = self.image_rotated.transformed(QTransform().scale(self.side, 1))
                self.canva.setPixmap(self.image_reflected)
                self.monochrome = 1
            
            elif self.monochrome == 1:
                self.image_pixmap = QPixmap(self.image_path)
                self.image_size = self.image_pixmap.size()
                self.image_scaled = self.image_pixmap.scaled(self.image_scale * self.image_size)
                self.image_rotated = self.image_scaled.transformed(QTransform().rotate(self.angle),QtCore.Qt.SmoothTransformation)
                self.image_reflected = self.image_rotated.transformed(QTransform().scale(self.side, 1))
                self.canva.setPixmap(self.image_reflected)
                self.monochrome = 0
    
    def create_grid(self):
        if self.path != "null":
            self.image_pixmap = QPixmap(self.image_path)
            qp = QPainter(self.image_pixmap)
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            color = QColorDialog.getColor()
            pen = QPen(QColor(color), 5)
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            self.show()
            qp.setRenderHint(QPainter.Antialiasing)
            qp.setPen(pen)
            qp.drawLine(0, int((self.image_pixmap.height()) * 0.25), self.image_pixmap.width(), int((self.image_pixmap.height()) * 0.25))
            qp.drawLine(int((self.image_pixmap.width()) * 0.25), 0, int((self.image_pixmap.width()) * 0.25), self.image_pixmap.height())
            qp.drawLine(0, int((self.image_pixmap.height()) * 0.75), self.image_pixmap.width(), int((self.image_pixmap.height()) * 0.75))
            qp.drawLine(int((self.image_pixmap.width()) * 0.75), 0, int((self.image_pixmap.width()) * 0.75), self.image_pixmap.height())
            qp.end()

            if self.monochrome == 1:
                Q_image = QtGui.QPixmap.toImage(self.image_pixmap)
                grayscale = Q_image.convertToFormat(QtGui.QImage.Format_Grayscale8)
                image = QtGui.QPixmap.fromImage(grayscale)
                self.image_pixmap = QPixmap(image)

            self.canva.setPixmap(self.image_pixmap)
            self.image_size = self.image_pixmap.size()
            self.image_scaled = self.image_pixmap.scaled(self.image_scale * self.image_size)
            self.image_rotated = self.image_scaled.transformed(QTransform().rotate(self.angle),QtCore.Qt.SmoothTransformation)
            self.image_reflected = self.image_rotated.transformed(QTransform().scale(self.side, 1))
            self.canva.setPixmap(self.image_reflected)

    def contextMenuEvent(self, event):
        if QtWidgets.QApplication.keyboardModifiers() != QtCore.Qt.ControlModifier:
            contextMenu = QMenu(self)
            contextMenu.setToolTipsVisible(True)

            contextMenu.setStyleSheet("""
                QMenu {background-color: rgba(20, 20, 20, 250); color: #bbb; padding: 10; border-radius: 0px;}
                QMenu::item {
                    border-radius: 3px;
                    padding: 4px 25px 5px 10px;
                    margin: 2px 5px; 
                }
                QMenu:selected {background-color: rgba(10, 10, 10, 250); color: #fff;}
                """)

            openAct = contextMenu.addAction("Open folder...")
            openAct.setIcon(QIcon("assets/folder_icon.png"))
            openAct.setToolTip("Choose folder which contains images.")
            
            ranAct = contextMenu.addAction("Choose random image...")
            ranAct.setIcon(QIcon("assets/random_icon.png"))

            contextMenu.addSeparator()

            reflectMenu = contextMenu.addMenu("Reflect image...")
            reflectMenu.setIcon(QIcon("assets/reflect_hor_icon.png"))

            reflectVerAct = reflectMenu.addAction("Reflect image vertically...")
            reflectVerAct.setIcon(QIcon("assets/reflect_ver_icon.png"))

            reflectHorAct = reflectMenu.addAction("Reflect image horizontally...")
            reflectHorAct.setIcon(QIcon("assets/reflect_hor_icon.png"))

            contextMenu.addSeparator()

            quitAct = contextMenu.addAction("Quit")
            action = contextMenu.exec_(self.mapToGlobal(event.pos()))
            if action == openAct:
                self.file_chooser()
            if action == ranAct:
                self.randomizer()
            if action == reflectVerAct:
                self.reflect()
            if action == quitAct:
                quit()

    def timer(self):
        if self.timer_visibility == True:
            self.dock.resize(70, 70)
            self.timer_visibility = False
        else:
            window_h = self.height()
            self.dock.resize(70, window_h - 40)
            self.timer_visibility = True

    def timer_start(self, time, amount):
        if self.path != "null":
            global images_amount
            global images_timer
            self.dialog.ui = Menu()
            self.dialog.ui.setupUi(self.dialog)
            images_amount = amount
            images_timer = time
            self.thread[1] = ThreadClass(parent=None,index=1)
            self.thread[1].start()
            self.thread[1].any_signal.connect(self.randomizer)
            self.thread[1].timer_signal.connect(self.time_change)
       
    def time_change(self, counter):
        cnt = counter
        self.value = cnt
        self.menu_button.setText(str(self.value))

    def show_menu(self):
        self.dialog.ui = Menu()
        self.dialog.ui.setupUi(self.dialog)
        self.dialog.ui.pushButton.clicked.connect(lambda: self.timer_start(((self.dialog.ui.spinBox_2.value() * 3600) + (self.dialog.ui.spinBox_3.value() * 60) + self.dialog.ui.spinBox_4.value()), int(self.dialog.ui.spinBox.value())))
        self.dialog.exec_()
        self.dialog.show()


class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()
    timer_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None,index=0):
        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True
    def run(self):
        for i in range(0, int(images_amount)):
            cnt = int(images_timer)
            self.timer_signal.emit(cnt)
            for j in range(1, int(images_timer)):
                cnt -= 1
                self.timer_signal.emit(cnt)
                time.sleep(1)
            cnt = 0
            self.timer_signal.emit(cnt)
            self.any_signal.emit()
        self.is_running = False

app = QApplication(sys.argv)
window = Ui()
app.exec_()
