# -*- coding: utf-8 -*-
"""
@author: Manasseh Madu
A simple Image Manipulation application
"""

import os
import sys
import time
import platform
from PyQt5.QtGui import (QBrush, QPixmap, QPainter)
from PyQt5.QtWidgets import (QColorDialog, QDialog, QLabel, QSpinBox, QComboBox, QPushButton, QDialogButtonBox, QGridLayout)
from PyQt5.QtCore import (Qt, QVariant)

class NewImageDlg(QDialog):
	"""docstring for NewImageDlg"""
	def __init__(self, parent=None):
		super(NewImageDlg, self).__init__(parent)

		self.color = Qt.red
		self.setMinimumWidth(300)

		widthLabel = QLabel('&Width: ')
		self.widthSpinBox = QSpinBox()
		widthLabel.setBuddy(self.widthSpinBox)
		self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
		self.widthSpinBox.setRange(10, 4000)
		self.widthSpinBox.setValue(100)
		self.widthSpinBox.setSuffix(' px')

		heightLabel = QLabel('&Height: ')
		self.heightSpinBox = QSpinBox()
		heightLabel.setBuddy(self.heightSpinBox)
		self.heightSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
		self.heightSpinBox.setRange(10, 4000)
		self.heightSpinBox.setValue(100)
		self.heightSpinBox.setSuffix(' px')

		brushLabel = QLabel('&Brush Pattern: ')
		self.brushComboBox = QComboBox()
		for value, text in (
			(Qt.SolidPattern, "Solid"),
			(Qt.Dense1Pattern, "Dense #1"),
			(Qt.Dense2Pattern, "Dense #2"),
			(Qt.Dense3Pattern, "Dense #3"),
			(Qt.Dense4Pattern, "Dense #4"),
			(Qt.Dense5Pattern, "Dense #5"),
			(Qt.Dense6Pattern, "Dense #6"),
			(Qt.Dense7Pattern, "Dense #7"),
			(Qt.HorPattern, "Horizontal"),
			(Qt.VerPattern, "Vertical"),
			(Qt.CrossPattern, "Cross"),
			(Qt.BDiagPattern, "Backward Diagonal"),
			(Qt.FDiagPattern, "Forward Diagonal"),
			(Qt.DiagCrossPattern, "Diagonal Cross")):
			self.brushComboBox.addItem(text, QVariant(value))
		brushLabel.setBuddy(self.brushComboBox)

		colorLabel = QLabel('&Color: ')
		self.colorButton = QPushButton('&Color...')
		colorLabel.setBuddy(self.colorButton)
		self.colorMap = QLabel()
		self.colorMap.setMinimumSize(60, 40)
		self.colorMap.setAlignment(Qt.AlignCenter)

		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)

		layout = QGridLayout()
		layout.addWidget(widthLabel, 0, 0)
		layout.addWidget(self.widthSpinBox, 0, 1)
		layout.addWidget(heightLabel, 1, 0)
		layout.addWidget(self.heightSpinBox, 1, 1)
		layout.addWidget(brushLabel, 2, 0)
		layout.addWidget(self.brushComboBox, 2, 1, 1, 2)
		layout.addWidget(colorLabel, 3, 0)
		layout.addWidget(self.colorMap, 3, 1)
		layout.addWidget(self.colorButton, 3, 2)
		layout.addWidget(buttonBox, 4, 1, 1, 2)
		self.setLayout(layout)

		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		self.colorButton.clicked.connect(self.getColor)
		self.brushComboBox.activated.connect(self.setColor)

		self.setColor()
		self.widthSpinBox.setFocus()
		self.setWindowTitle('Image Resizer - New Image')
		
	def getColor(self):
		color = QColorDialog().getColor(self.color, self)
		if color.isValid():
			self.color = color
			self.setColor()

	def setColor(self):
		pixmap = self._makePixmap(60, 30)
		self.colorMap.setPixmap(pixmap)

	def image(self):
		pixmap = self._makePixmap(self.widthSpinBox.value(), self.heightSpinBox.value())
		return QPixmap.toImage(pixmap)

	def _makePixmap(self, width, height):
		pixmap =QPixmap(width, height)
		style = self.brushComboBox.itemData(self.brushComboBox.currentIndex())
		brush = QBrush(self.color, Qt.BrushStyle(style))
		painter = QPainter(pixmap)
		painter.fillRect(pixmap.rect(), Qt.white)
		painter.fillRect(pixmap.rect(), brush)
		return pixmap

# if __name__ == '__main__':
# 	app = QApplication(sys.argv)
# 	form = NewImageDlg()
# 	form.show()
# 	app.exec_()
