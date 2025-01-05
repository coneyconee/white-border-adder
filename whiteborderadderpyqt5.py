import os
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QSpinBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ImageBorderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('image border by Coen Peter Ng')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.srclabel = QLabel('source directory:')
        self.layout.addWidget(self.srclabel)

        self.srcbtn = QPushButton('select source directory')
        self.srcbtn.clicked.connect(self.selectsrc)
        self.layout.addWidget(self.srcbtn)

        self.destlabel = QLabel('destination directory:')
        self.layout.addWidget(self.destlabel)

        self.destbtn = QPushButton('select destination directory')
        self.destbtn.clicked.connect(self.selectdest)
        self.layout.addWidget(self.destbtn)

        self.canvaslabel = QLabel('canvas size (h * w):')
        self.layout.addWidget(self.canvaslabel)

        self.heightinput = QSpinBox()
        self.heightinput.setRange(1, 10000)
        self.heightinput.setValue(1080)

        self.widthinput = QSpinBox()
        self.widthinput.setRange(1, 10000)
        self.widthinput.setValue(1080)

        self.sizelayout = QHBoxLayout()
        self.sizelayout.addWidget(QLabel('height:'))
        self.sizelayout.addWidget(self.heightinput)
        self.sizelayout.addWidget(QLabel('width:'))
        self.sizelayout.addWidget(self.widthinput)

        self.layout.addLayout(self.sizelayout)

        self.borderlabel = QLabel('border size (in tens of pixels):')
        self.layout.addWidget(self.borderlabel)

        self.borderinput = QSpinBox()
        self.borderinput.setRange(1, 100)
        self.borderinput.setValue(7)
        self.layout.addWidget(self.borderinput)

        self.previewbtn = QPushButton('preview image')
        self.previewbtn.clicked.connect(self.preview)
        self.layout.addWidget(self.previewbtn)

        self.processbtn = QPushButton('process all images')
        self.processbtn.clicked.connect(self.process)
        self.layout.addWidget(self.processbtn)

        self.previewlabel = QLabel('image preview')
        self.previewlabel.setAlignment(Qt.AlignCenter)
        self.previewlabel.setStyleSheet('border: 1px solid black;')
        self.layout.addWidget(self.previewlabel)

        self.statuslabel = QLabel('')
        self.statuslabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.statuslabel)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.srcdir = None
        self.destdir = None

    def selectsrc(self):
        self.srcdir = QFileDialog.getExistingDirectory(self, 'select source directory')
        if self.srcdir:
            self.srclabel.setText(f'source directory: {self.srcdir}')

    def selectdest(self):
        self.destdir = QFileDialog.getExistingDirectory(self, 'select destination directory')
        if self.destdir:
            self.destlabel.setText(f'destination directory: {self.destdir}')

    def preview(self):
        if not self.srcdir:
            self.statuslabel.setText('select a source directory')
            return

        files = [f for f in os.listdir(self.srcdir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not files:
            self.statuslabel.setText('no valid files in directory')
            return

        srcpath = os.path.join(self.srcdir, files[0])
        canvash = self.heightinput.value()
        canvasw = self.widthinput.value()
        bordersize = self.borderinput.value() * 10

        srcimg = Image.open(srcpath)
        imgmaxh, imgmaxw = canvash - 2 * bordersize, canvasw - 2 * bordersize
        srcimg.thumbnail((imgmaxw, imgmaxh))

        canvas = Image.new('RGB', (canvasw, canvash), 'white')
        x, y = (canvasw - srcimg.width) // 2, (canvash - srcimg.height) // 2
        canvas.paste(srcimg, (x, y))

        previewpath = 'preview_tmp.jpg'
        canvas.save(previewpath, 'JPEG')

        pixmap = QPixmap(previewpath)
        self.previewlabel.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def process(self):
        if not self.srcdir or not self.destdir:
            self.statuslabel.setText('select source & destination directories')
            return

        os.makedirs(self.destdir, exist_ok=True)

        canvash = self.heightinput.value()
        canvasw = self.widthinput.value()
        bordersize = self.borderinput.value() * 10

        for file in os.listdir(self.srcdir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                srcpath = os.path.join(self.srcdir, file)
                destpath = os.path.join(self.destdir, f'border_{file}')

                srcimg = Image.open(srcpath)

                imgmaxh, imgmaxw = canvash - 2 * bordersize, canvasw - 2 * bordersize

                srcimg.thumbnail((imgmaxw, imgmaxh))

                canvas = Image.new('RGB', (canvasw, canvash), 'white')

                x, y = (canvasw - srcimg.width) // 2, (canvash - srcimg.height) // 2

                canvas.paste(srcimg, (x, y))

                canvas.save(destpath, 'JPEG')

        self.statuslabel.setText(f'all images saved in {self.destdir}.')


if __name__ == '__main__':
    app = QApplication([])
    window = ImageBorderApp()
    window.show()
    app.exec_()