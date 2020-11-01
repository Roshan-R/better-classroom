import classroom
import drive


# file_id = posts[m.value]['id']
# title = posts[m.value]['title']
# x = Drive.downloadFile(fileId=file_id, fileName=title)
# x[0].GetContentFile(x[1])

import sys


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class BackEnd:
    def __init__(self):
        print("Logging in....")
        self.Classroom = classroom.Classroom()
        self.ClassroomStuff = classroom.GetClassroomStuff(classroom=self.Classroom)
        self.Drive = drive.GDrive()

        self.Classroom.initialize()

    def getCourseList(self):
        print("Fetching Course list")
        self.courses = self.ClassroomStuff.getCourses()
        return self.courses

    def getPosts(self, courseIndex):
        posts = []
        id = self.courses[courseIndex]['id']
        courseMaterials = self.ClassroomStuff.getPosts(courseId=id)
        for material in courseMaterials:
            posts.append(material)
        return posts


    


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(30, 10, 731, 491))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 42))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.populateWithCourse()
        
        self.listWidget.itemClicked.connect(self.doubleclicked)
        self.listWidget.itemEntered.connect(self.doubleclicked)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def doubleclicked(self,item):
        print("Clicked Me!")
        self.populateWithPosts(item)

    def populateWithCourse(self):
        self.gclass = BackEnd()
        self.courselist = self.gclass.getCourseList()
        self.coursenames = [course['name'] for course in self.courselist]
        self.listWidget.addItems(self.coursenames)
        self.state = "Course"

    def populateWithPosts(self, item):
        if self.state == "Course":
            courseIndex = self.coursenames.index(item.text())
            posts = self.gclass.getPosts(courseIndex)
            posts = [post['title'] for post in posts]
            self.listWidget.clear()
            self.listWidget.addItems(posts)
            self.state = "Posts"

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi




# if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # app.setApplicationName("Better Classroom")
    # listWidget = ListWidget()

    # courselist = getCourseList()
    # listWidget.addItems([course['name'] for course in courselist])
    # # listWidget.addItem("Item 1")
    # # listWidget.addItem("Item 2")
    # # listWidget.addItem("Item 3")
    # # listWidget.addItem("Item 4")
    # listWidget.setWindowTitle('QListwidget Example')
    # listWidget.itemClicked.connect(listWidget.clicked)

    # listWidget.show()
    # sys.exit(app.exec_())

if __name__ == "__main__":
    print("Setting up Ui")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
