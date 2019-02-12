from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon, QPixmapCache
from PyQt5.QtWidgets import QApplication, QMessageBox


class App(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)
        self.setOrganizationName("UZH Zurich")
        self.setOrganizationDomain("http://www.bodenmillerlab.org")
        self.setApplicationName("HistoSlider")
        self.setWindowIcon(QIcon(":/icons/app.svg"))

        cache_size_in_kb = 700 * 10 ** 3
        QPixmapCache.setCacheLimit(cache_size_in_kb)

        f = QFile(":/style.qss")
        f.open(QFile.ReadOnly | QFile.Text)
        self.setStyleSheet(QTextStream(f).readAll())
        f.close()

    def report_error(self, message: str, detail: str):
        """
        Display an error in a modal

        :param message: A short description of the error
        :type message: str
        :param detail: A longer description
        :type detail: str
        """
        qmb = QMessageBox(QMessageBox.Critical, "Error", message)
        qmb.setDetailedText(detail)
        qmb.resize(400, qmb.size().height())
        qmb.exec_()
