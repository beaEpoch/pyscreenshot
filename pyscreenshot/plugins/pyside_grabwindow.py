import logging

from PIL import Image

from pyscreenshot.plugins.backend import CBackend
from pyscreenshot.util import py2

if py2():
    import StringIO

    BytesIO = StringIO.StringIO
else:
    import io

    BytesIO = io.BytesIO


log = logging.getLogger(__name__)

# based on qt4 backend

app = None


class PySideGrabWindow(CBackend):
    name = "pyside"

    def __init__(self):
        pass

    def grab_to_buffer(self, buff, file_type="png"):
        from PySide import QtGui
        from PySide import QtCore

        QApplication = QtGui.QApplication
        QBuffer = QtCore.QBuffer
        QIODevice = QtCore.QIODevice
        QPixmap = QtGui.QPixmap

        global app
        if not app:
            app = QApplication([])
        qbuffer = QBuffer()
        qbuffer.open(QIODevice.ReadWrite)
        QPixmap.grabWindow(QApplication.desktop().winId()).save(qbuffer, file_type)
        # https://stackoverflow.com/questions/52291585/pyside2-typeerror-bytes-object-cannot-be-interpreted-as-an-integer
        buff.write(qbuffer.data().data())
        qbuffer.close()

    def grab(self, bbox=None):
        strio = BytesIO()
        self.grab_to_buffer(strio)
        strio.seek(0)
        im = Image.open(strio)
        if bbox:
            im = im.crop(bbox)
        return im

    def backend_version(self):
        import PySide

        return PySide.__version__
