from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import pandas as pd
import threading
from linkedin_scraper import get_jobs_linkedin

class GUI(QMainWindow):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.initiateGUI()

    def LoginBtnClicked(self):
        self.password = self.PasswordInput.text()
        self.userName = self.UserInput.text()
        self.jobTitle = self.JobTitleInput.text()
        self.jobLocation = self.JobLocationInput.text()
        self.searchNumber = self.NumberOfJobsInput.text()

        isUserFilled = (len(self.userName) > 0)
        isPassFilled = (len(self.password) > 0)

        if not(isUserFilled) and not(isPassFilled):
            self.StatusLabel.setText('Status: Input Fields cannot be null ')
        elif not(isUserFilled):
            self.StatusLabel.setText('Status: UserName cannot be null ')
        elif not(isPassFilled):
            self.StatusLabel.setText('Status: Password cannot be null ')
        else:
            self.StatusLabel.setText('Status: Searching for jobs')
            try:
                threading.Timer(2, self.runScraper).start()
            except:
                print('Exception Happened')

    def runScraper(self):
        msg = get_jobs_linkedin(self.userName, self.password, int(self.searchNumber), self.jobTitle, self.jobLocation, self.StatusLabel)
        QtWidgets.QMessageBox.information(self, 'Scraping Ended', 'Excel File saved to: \n '+ msg)

    def initiateGUI(self):
        fontLabel = QtGui.QFont('Times', 12, italic=True)
        fontTitle = QtGui.QFont('Times', 15, italic=True)

        self.setWindowTitle('Python Program')
        self.setGeometry(100, 100, 350, 480)  # xpos, ypos, width, heigth

        self.TitleLabel = QtWidgets.QLabel(self)
        self.TitleLabel.setText('LinkedIn Scraper')
        self.TitleLabel.setGeometry(25, 15, 300, 30)
        self.TitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TitleLabel.setFont(fontTitle)

        self.UserLabel = QtWidgets.QLabel(self)
        self.UserLabel.setText('User Name')
        self.UserLabel.move(25, 50)
        self.UserLabel.setFont(fontLabel)

        self.UserInput = QtWidgets.QLineEdit(self)
        self.UserInput.setGeometry(25, 80, 300, 30)

        self.PasswordLabel = QtWidgets.QLabel(self)
        self.PasswordLabel.setText('Password')
        self.PasswordLabel.move(25, 125)
        self.PasswordLabel.setFont(fontLabel)

        self.PasswordInput = QtWidgets.QLineEdit(self)
        self.PasswordInput.setGeometry(25, 155, 300, 30)
        self.PasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)

        self.JobTitleLabel = QtWidgets.QLabel(self)
        self.JobTitleLabel.setText('Job Title')
        self.JobTitleLabel.move(25, 200)
        self.JobTitleLabel.setFont(fontLabel)

        self.JobTitleInput = QtWidgets.QLineEdit(self)
        self.JobTitleInput.setGeometry(25, 230, 300, 30)

        self.JobLocationLabel = QtWidgets.QLabel(self)
        self.JobLocationLabel.setText('Job Location')
        self.JobLocationLabel.move(25, 280)
        self.JobLocationLabel.setFont(fontLabel)

        self.JobLocationInput = QtWidgets.QLineEdit(self)
        self.JobLocationInput.setGeometry(25, 310, 300, 30)

        self.NumberOfJobsLabel = QtWidgets.QLabel(self)
        self.NumberOfJobsLabel.setText('Number of jobs to be searched')
        self.NumberOfJobsLabel.setGeometry(25, 350, 300, 30)
        self.NumberOfJobsLabel.setFont(fontLabel)

        self.NumberOfJobsInput = QtWidgets.QLineEdit(self)
        self.NumberOfJobsInput.setGeometry(25, 380, 80, 30)

        self.LoginButton = QtWidgets.QPushButton(self)
        self.LoginButton.setText('Start Search')
        self.LoginButton.move(125, 420)
        self.LoginButton.clicked.connect(self.LoginBtnClicked)
        self.LoginButton.setFont(fontLabel)

        self.StatusLabel = QtWidgets.QLabel(self)
        self.StatusLabel.setText('Status:')
        self.StatusLabel.setGeometry(25, 450, 300, 30)


def Main():
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    Main()
