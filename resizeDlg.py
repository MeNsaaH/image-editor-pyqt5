# -*- coding: utf-8 -*-
"""
@author: Manasseh Madu
A simple Image Manipulation application
"""

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ResizeDialog(QDialog):
	"""docstring for ResizeDialog"""
	def __init__(self, width, height, parent=None):
		super(ResizeDialog, self).__init__(parent)
		self.width = width
		self.height = height
		self.parent = parent
		self.setMinimumWidth(235)

		widthLabel = QLabel('&Width: ')
		self.widthSpinBox = QSpinBox()
		widthLabel.setBuddy(self.widthSpinBox)
		self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
		self.widthSpinBox.setRange(4, 4*width)
		self.widthSpinBox.setValue(width)
		
		heightLabel = QLabel('&Height: ')
		self.heightSpinBox = QSpinBox()
		heightLabel.setBuddy(self.heightSpinBox)
		self.heightSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
		self.heightSpinBox.setRange(4, 4*height)
		self.heightSpinBox.setValue(height)

		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

		layout = QGridLayout()
		layout.addWidget(widthLabel, 0, 0)
		layout.addWidget(self.widthSpinBox, 0, 1)
		layout.addWidget(heightLabel, 1, 0)
		layout.addWidget(self.heightSpinBox, 1, 1)
		layout.addWidget(buttonBox, 2, 0, 1, 2)
		self.setLayout(layout)

		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)

		self.setWindowTitle('Image Editor - Resize')

	def result(self):
		return self.widthSpinBox.value(), self.heightSpinBox.value()

# if __name__ == '__main__':
# 	app = QApplication(sys.argv)
# 	form = ResizeDialog(64, 28)
# 	form.show()
# 	app.exec_()


