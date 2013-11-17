"""
This program is licensed under the BSD license.

Copyright (c) 2013, Sanjeev Kumar
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, 
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, 
      this list of conditions and the following disclaimer in the documentation 
      and/or other materials provided with the distribution.
    * Neither the name of the Dino Interactive nor the names of its contributors 
      may be used to endorse or promote products derived from this software 
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR 
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from PyQt4 import QtGui,QtCore
import sys
import os


class SlideShowPics(QtGui.QWidget):
	"""docstring for SlideShowPics"""
	def __init__(self, path):
		super(SlideShowPics, self).__init__()
		# Centre UI
		screen = QtGui.QDesktopWidget().screenGeometry(self)
		size =  self.geometry()
		self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)
		QtGui.QWidget.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
		self._path = path
		self.setStyleSheet("QWidget{background-color: #000000;}")
		self.animFlag = True
		self.pause = False
		self.buildUi()
		self.showFullScreen()
		self.count = 0
		self.nextImage()
		self.updateTimer = QtCore.QTimer()
		self.connect(self.updateTimer, QtCore.SIGNAL("timeout()"), self.nextImage)
		self.playPause() 

	def allImages(self):
		return  tuple(os.path.join(self._path,each) for each in os.listdir(self._path) 
			if os.path.isfile(os.path.join(self._path,each)) and each.endswith('png') or each.endswith('jpg'))

	def nextImage(self):
		if self.allImages():
			if self.count != len(self.allImages()):
				image = QtGui.QImage(self.allImages()[self.count])
				pp = QtGui.QPixmap.fromImage(image)
				self.label.setPixmap(pp.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
			else:
				self.count = 0
			if self.animFlag:
				self.count += 1
			else:
				self.count -= 1
		else:
			message = "No Image found in %s" % os.getcwd()
			print message
			self.close()

	def keyPressEvent(self, keyevent):
		"""	Capture key to exit, next image, previous image,
			on Escape , Key Right and key left respectively.
		"""
		if keyevent.key() == QtCore.Qt.Key_Escape:
			self.close()
		if keyevent.key() == QtCore.Qt.Key_Left:
			self.animFlag = False
			self.nextImage()
		if keyevent.key() == QtCore.Qt.Key_Right:
			self.animFlag = True
			self.nextImage()
		if keyevent.key() == 32:
			self.pause = self.playPause()

	def playPause(self):
			if not self.pause:
				self.pause = True
				self.updateTimer.start(2500)
				return self.pause
			else:
				self.pause = False
				self.updateTimer.stop()

	def _openFolder(self):
		selectedDir = str(QtGui.QFileDialog.getExistingDirectory(
			self,"Select Directory to SlideShow",os.path.expanduser("~")))
		if selectedDir:
			return selectedDir

	def buildUi(self):
		filename = self._path
		self.layout = QtGui.QHBoxLayout()
		self.label = QtGui.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.layout.addWidget(self.label)
		self.setLayout(self.layout)


def main():
	curntPath = os.getcwd()
	if any(each.endswith('png') or each.endswith('jpg') for each in os.listdir(curntPath)):	
		app = QtGui.QApplication(sys.argv)
		window =  SlideShowPics(curntPath)
		window.show()
		window.raise_()
		app.exec_()
	else:
		print "No Image found in %s" % os.getcwd()

if __name__ == '__main__':
	main()
