# -*- coding: utf-8 -*-
"""
@author: Manasseh Madu
A simple Image Manipulation application
"""

import os
import sys
import platform
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QDialog, QDockWidget, QFileDialog, QFrame, QInputDialog, QLabel, QListWidget, QMainWindow, QMessageBox, QSpinBox)
from PyQt5.QtGui import (QIcon, QImage, QImageReader, QImageWriter, QKeySequence, QPixmap, QPainter)
from PyQt5.QtPrintSupport import (QPrinter, QPrintDialog)
from PyQt5.QtCore import (PYQT_VERSION_STR, QFile, QFileInfo, QSettings,QT_VERSION_STR, QTimer, QVariant, Qt, pyqtSlot)

import qrc_resources
import resizeDlg
import helpForm as hp
import newImageDlg

__version__ = '1.0.0'

class MainWindow(QMainWindow):
	"""docstring for MainWindow"""
	def __init__(self, parent=None):

		super(MainWindow, self).__init__(parent)
		self.image = QImage()
		self.dirty = False
		self.filename = None
		self.mirroredVertically = False
		self.mirroredHorizontally = False

		#Central Widgets
		self.imageLabel = QLabel()
		self.imageLabel.setMinimumSize(200, 200)
		self.imageLabel.setAlignment(Qt.AlignCenter)
		self.imageLabel.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.setCentralWidget(self.imageLabel)

		#Docks at side
		logDockWidget =QDockWidget('Log', self)
		logDockWidget.setObjectName('LogDockWidget')
		logDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
		self.listWidget = QListWidget()
		logDockWidget.setWidget(self.listWidget)
		self.addDockWidget(Qt.RightDockWidgetArea, logDockWidget)

		self.printer = None

		#Status bar below
		self.sizeLabel = QLabel()
		self.sizeLabel.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
		status = self.statusBar()
		status.setSizeGripEnabled(False)
		status.addPermanentWidget(self.sizeLabel)
		status.showMessage('Ready', 5000)

		#file Menu Options
		fileNewAction = self.createAction('&New...', self.fileNew, QKeySequence.New, 'filenew', 'Create a new Image File' )
		fileQuitAction = self.createAction('&Quit...', self.close, 'Ctrl + Q', 'filequit', 'Close the Application' )
		fileOpenAction = self.createAction('&Open...', self.fileOpen, QKeySequence.Open, 'fileopen', 'open an existing image file')
		fileSaveAction = self.createAction('&Save...', self.fileSave, QKeySequence.Save, 'filesave', 'save image file')
		fileSaveAsAction = self.createAction('Save &As...', self.fileSaveAs, QKeySequence.SaveAs, 'filesaveas', 'save image file using a new name')
		filePrintAction = self.createAction('&Print...', self.filePrint, QKeySequence.Print, 'fileprint', 'print image')
		#Edit Menu options
		editZoomAction = self.createAction('&Zoom', self.editZoom, 'Alt + Z', 'editzoom','zoom the image')
		editInvertAction = self.createAction('&Invert', self.editInvert, 'Ctrl + I', 'editinvert','Invert the images Color', True, 'toggled')
		editSwapRedAndBlueAction = self.createAction('S&wap red and blue', self.editSwapRedAndBlue, 'Ctrl + W', 'editswap','swap the images red and blue components', True, 'toggled')
		editResizeAction = self.createAction('&Resize', self.editResize, 'Ctrl + R', 'editresize', 'resizes the image')
		#Mirror Groups
		mirrorGroup = QActionGroup(self)
		editUnMirrorAction = self.createAction('&Unmirror', self.editUnMirror, 'Ctrl + U', 'editunmirror', 'Unmirror the image', True, 'toggled')
		mirrorGroup.addAction(editUnMirrorAction)
		editMirrorHorizontalAction = self.createAction('Mirror &Horizontally', self.editMirrorHorizontal, 'Ctrl + H', 'editmirrorhoriz', 'Horizontally Mirror the image', True, 'toggled')
		mirrorGroup.addAction(editMirrorHorizontalAction)
		editMirrorVerticalAction = self.createAction('Mirror &Vertically', self.editMirrorVertical, 'Ctrl + V', 'editmirrorvert', 'Vertically Mirror the image', True, 'toggled')
		mirrorGroup.addAction(editMirrorVerticalAction)
		editUnMirrorAction.setChecked(True)

		#help Menu Options
		helpAboutAction = self.createAction('&About Image Editor', self.helpAbout)
		helpHelpAction = self.createAction('&Help', self.helpHelp, QKeySequence.HelpContents)

		#add Menus to menu bar
		#fileMenu
		self.fileMenu = self.menuBar().addMenu('&File')
		self.fileMenuActions = (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction, None, filePrintAction, fileQuitAction)
		self.fileMenu.aboutToShow.connect(self.updateFileMenu)

		#edit Menu
		editMenu = self.menuBar().addMenu('&Edit')
		self.addActions(editMenu, (editZoomAction, editInvertAction, editSwapRedAndBlueAction, editResizeAction))
		mirrorMenu = editMenu.addMenu(QIcon(':/editmirror.png'), '&Mirror')
		self.addActions(mirrorMenu, (editUnMirrorAction, editMirrorVerticalAction, editMirrorHorizontalAction))
		#help Menu
		helpMenu = self.menuBar().addMenu('&Help')
		self.addActions(helpMenu, (helpAboutAction, helpHelpAction))

		#Tool bars
		#File Tool Bars
		fileToolBar = self.addToolBar('File')
		fileToolBar.setObjectName('FileToolBar')
		self.addActions(fileToolBar, (fileNewAction, fileOpenAction, fileSaveAction, fileSaveAsAction))

		#Edit Tool Bars
		editToolBar = self.addToolBar('Edit')
		editToolBar.setObjectName('EditToolBar')
		self.addActions(editToolBar, (editInvertAction, editSwapRedAndBlueAction, editUnMirrorAction, editMirrorVerticalAction, editMirrorHorizontalAction, editResizeAction))

		self.zoomSpinBox = QSpinBox()
		self.zoomSpinBox.setRange(1, 400)
		self.zoomSpinBox.setSuffix(' %')
		self.zoomSpinBox.setValue(100)
		self.zoomSpinBox.setToolTip('Zoom the Image')
		self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
		self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)
		self.zoomSpinBox.valueChanged.connect(self.showImage)
		editToolBar.addWidget(self.zoomSpinBox)

		self.addActions(self.imageLabel, (editInvertAction, editSwapRedAndBlueAction, editUnMirrorAction, editMirrorVerticalAction, editMirrorHorizontalAction, editResizeAction))
		self.resettableActions = ((editInvertAction, False),
                                 (editSwapRedAndBlueAction, False),
                                 (editUnMirrorAction, True))
		settings = QSettings()
		if settings.value('recentFiles') is not None:
			self.recentFiles = settings.value('recentFiles')
			self.restoreGeometry(settings.value('Geometry'))
			self.restoreState(settings.value('MainWindow/State'))
		else:
			self.recentFiles = list()
		self.updateFileMenu()
		self.setWindowTitle('Image Editor')
		QTimer.singleShot(0, self.loadInitialFile)
		
	def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal='triggered'):
		action = QAction(text, self)
		if icon is not None:
			action.setIcon(QIcon(':/%s.png' % icon))
		if shortcut is not None:
			action.setShortcut(shortcut)
		if tip is not None:
			action.setToolTip(tip)
			action.setStatusTip(tip)
		if slot is not None:
			action.triggered.connect(slot)
		if checkable:
			action.setCheckable(True)
		return action

	def addActions(self, target, actions):
		for action in actions:
			if action is None:
				target.addSeparator()
			else:
				target.addAction(action)

	def loadInitialFile(self):
		settings = QSettings()
		if settings.value('LastFile'):
			fname = str(settings.value('LastFile'))
			if fname and QFile.exists(fname):
				self.loadFile(fname)

	def closeEvent(self, event):
		if self.okToContinue():
			settings = QSettings()
			filename = QVariant(str(self.filename)) if self.filename is not  None else QVariant()
			settings.setValue('LastFile', filename)
			recentFiles = QVariant(self.recentFiles) if self.recentFiles else QVariant()
			settings.setValue('recentFiles', recentFiles)
			settings.setValue('Geometry', QVariant(self.saveGeometry()))
			settings.setValue('MainWindow/State', QVariant(self.saveState()))
		else:
			event.ignore()

	def okToContinue(self):
		if self.dirty:
			reply = QMessageBox.question(self, 'Image Editor - Unsaved Changes',
					'Save Unsaved Changes?', QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel)
			if reply == QMessageBox.Cancel:
				return False
			elif reply == QMessageBox.Yes:
				self.fileSave()
		return True

	def updateFileMenu(self):
		self.fileMenu.clear()
		self.addActions(self.fileMenu, self.fileMenuActions[:-1])
		current = str(self.filename) if self.filename is not None else None
		recentFiles = []
		if self.recentFiles:
			for fname in self.recentFiles:
				if fname != current and QFile.exists(fname):
					recentFiles.append(fname)
		if recentFiles:
			self.fileMenu.addSeparator()
			for i, fname in enumerate(recentFiles):
				action = QAction(QIcon(":/icon.png"), '&%d %s' % (i + 1, QFileInfo(fname).fileName()), self)
				action.setData(QVariant(fname))
				action.triggered.connect(self.loadFile)
				self.fileMenu.addAction(action)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.fileMenuActions[-1])

	@pyqtSlot(str)
	def on_Select_file(self, value):
		self.loadFile(value)


	def addRecentFiles(self, fname):
		if fname is None:
			return
		if self.recentFiles is not None:
			if not fname in self.recentFiles:
				self.recentFiles.insert(0, fname)
				while len(self.recentFiles) > 9:
					self.recentFiles.pop(len(self.recentFiles)-1)

	def fileNew(self):
		if not self.okToContinue():
			return
		dialog = newImageDlg.NewImageDlg(self)
		if dialog.exec_():
			self.addRecentFiles(self.filename)
			self.image = QImage()
			for action, check in self.resettableActions:
				action.setChecked(check)
			self.image = dialog.image()
			self.filename = None
			self.dirty = True
			self.showImage()
			self.sizeLabel.setText('{0} {1}'.format(self.image.width(), self.image.height()))
			self.updateStatus('Created New Image')

	def updateStatus(self, message):
		self.statusBar().showMessage(message, 5000)
		self.listWidget.addItem(message)
		if self.filename is not None:
			self.setWindowTitle('Image Editor - {0}[*]'.format(os.path.basename(self.filename)))
		elif not self.image.isNull():
			self.setWindowTitle('Image Editor - Unnamed[*]')
		else:
			self.setWindowTitle('Image Editor[*]')
		self.setWindowModified(self.dirty)

	def fileOpen(self):
		if not self.okToContinue():
			return
		dir = os.path.dirname(self.filename) if self.filename is not None else '.'
		formats = ['{0}'.format(str(format).lower()) for format in QImageReader.supportedImageFormats()]
		formats = ['*.{0}'.format(format[2:5]) for format in formats]
		fname,_ = QFileDialog.getOpenFileName(self, 'Image Editor - Choose Image', dir, 'Image File ({0})'.format(" ".join(formats)))
		if fname:
			self.loadFile(fname)

	def loadFile(self, fname):
		#print(fname)
		if fname is None:
			action = self.sender()
			if isinstance(action, QAction):
				fname = str(action.data().toString)
				if not self.okToContinue():
					return
			else:
				return
		if fname:
			self.filename = None
			image = QImage(fname)
			if image.isNull():
				message = 'failed to read {0}'.format(fname)
			else:
				self.addRecentFiles(fname)
				self.image = QImage()
				for action, check in self.resettableActions:
					action.setChecked(check)
				self.image = image
				self.filename = fname
				self.showImage()
				self.dirty = False
				self.sizeLabel.setText('{0} x {1}'.format(image.width(), image.height()))
				message = 'Loaded {0}'.format(os.path.basename(fname))
			self.updateStatus(message)
			
	def fileSave(self):
		if self.image.isNull():
			return
		if self.filename is None:
			self.fileSaveAs()
		else:
			if self.image.save(self.filename, None):
				self.updateStatus('Saved as {0}'.format(self.filename))
				self.dirty = False
			else:
				self.updateStatus('Failed to save {0}'.format(self.filename))

	def fileSaveAs(self):
		if self.image.isNull():
			return
		fname = self.filename if self.filename else '.'
		formats = ['{0}'.format(str(format).lower()) for format in QImageWriter.supportedImageFormats()]
		formats = ['*.{0}'.format(format[2:5]) for format in formats]
		fname,_ = QFileDialog.getSaveFileName(self, 'Image Editor - Save Image', fname, 'Image files ({0})'.format(' '.join(formats)))
		if fname:
			if '.' not in fname:
				fname += '.png'
			self.addRecentFiles(fname)
			self.filename = fname
			self.fileSave()

	def filePrint(self):
		pass

	def editZoom(self):
		if self.image.isNull():
			return
		percent, ok = QInputDialog.getInt(self, 'Image Editor - Zoom', 'Percent', self.zoomSpinBox.value(), 1, 400)
		if ok:
			self.zoomSpinBox.setValue(percent)

	def editInvert(self, on):
		if self.image.isNull():
			return
		self.image.invertPixels()
		self.showImage()
		self.dirty = True
		self.updateStatus('Inverted' if on else 'UnInverted')

	def editUnMirror(self):
		if self.image.isNull():
			return
		if self.mirroredHorizontally:
			self.editMirrorHorizontal(False)
		if self.mirroredVertically:
			self.editMirrorVertical(False)

	def editMirrorVertical(self, on):
		if self.image.isNull():
			return
		self.image = self.image.mirrored(False, True)
		self.showImage()
		self.mirroredVertically = not self.mirroredVertically
		self.dirty = True
		self.updateStatus('Mirrorred Vertically' if on else 'Unmirrored Vertically')


	def editMirrorHorizontal(self, on):
		if self.image.isNull():
			return
		self.image = self.image.mirrored(True, False)
		self.showImage()
		self.mirroredHorizontally = not self.mirroredHorizontally
		self.dirty = True
		self.updateStatus('Mirrorred Horizontally' if on else 'Unmirrored Horizontally')

	def editSwapRedAndBlue(self, on):
		if self.image.isNull():
			return
		self.image = self.image.rgbSwapped()
		self.showImage()
		self.dirty = True
		self.updateStatus('Swapped Red and Blue' if on else 'Unswapped Red and Blue')

	def editResize(self):
		if self.image.isNull():
			return
		form = resizeDlg.ResizeDialog(self.image.width(), self.image.height(), self)
		if form.exec_():
			width, height = form.result()
			if (width == self.image.width() and height == self.image.height()):
				self.updateStatus('Resized to the same Size')
			else:
				self.image = self.image.scaled(width, height)
				self.showImage()
				self.dirty = True 
				size = '{0} x {1}'.format(self.image.width(), self.image.height())
				self.sizeLabel.setText(size)
				self.updateStatus('Resized to {0}'.format(size))

	def helpAbout(self):
		QMessageBox.about(self, 'About Image Editor', '''<b>Image Editor v %s 
			<p>Copyright &copy; 2018 Qtrac Ltd. All rights reserved
			<p>This is an application used to perform simple image manipulations
			<p>Python %s - Qt %s - PyQt %s on %s''' % (__version__, platform.python_version(), QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

	def helpHelp(self):
		form = hp.HelpForm('index.html', self)
		form.show()

	def showImage(self, percent=None):
		if self.image.isNull():
			return
		if percent is None:
			percent = self.zoomSpinBox.value()
		factor = percent/100.0
		width = self.image.width() * factor
		height = self.image.height() * factor
		image = self.image.scaled(width, height, Qt.KeepAspectRatio)
		self.imageLabel.setPixmap(QPixmap.fromImage(image))

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Editor")
    app.setWindowIcon(QIcon(":/icon.png"))
    
    form = MainWindow()
    form.show()
    app.exec_()


main()

