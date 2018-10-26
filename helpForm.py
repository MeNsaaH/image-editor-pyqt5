# -*- coding: utf-8 -*-
"""
@author: Manasseh Madu
A simple Image Manipulation application
"""

import os
import sys
from PyQt5.QtWidgets import (QAction, QApplication, QLabel, QTextBrowser, QToolBar, QVBoxLayout, QDialog)
from PyQt5.QtGui import (QIcon, QKeySequence)
from PyQt5.QtCore import (QUrl, Qt)


class HelpForm(QDialog):
	"""docstring for HelpForm"""
	def __init__(self, page, parent=None):
		super(HelpForm, self).__init__(parent)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setAttribute(Qt.WA_GroupLeader)

		backAction = QAction(QIcon(':/back.png'), '&Back', self)
		backAction.setShortcut(QKeySequence.Back)
		homeAction = QAction(QIcon(':/home.png'), '&Home', self)
		homeAction.setShortcut("Home")

		self.pageLabel = QLabel()

		toolBar = QToolBar()
		toolBar.addAction(backAction)
		toolBar.addAction(homeAction)
		toolBar.addWidget(self.pageLabel)

		self.textBrowser = QTextBrowser()

		layout = QVBoxLayout()
		layout.addWidget(toolBar)
		layout.addWidget(self.textBrowser, 1)
		self.setLayout(layout)

		backAction.triggered.connect(self.textBrowser.backward)
		homeAction.triggered.connect(self.textBrowser.home)
		self.textBrowser.sourceChanged.connect(self.updatePageTitle)

		self.textBrowser.setSearchPaths([':/help'])
		self.textBrowser.setSource(QUrl(page))
		self.resize(400, 600)
		self.setWindowTitle('{0} - Help'.format(QApplication.applicationName()))

	def updatePageTitle(self):
		self.pageLabel.setText(self.textBrowser.documentTitle())


# if __name__ == '__main__':
# 	app = QApplication(sys.argv)
# 	form = HelpForm('index.html')
# 	form.show()
# 	app.exec_()