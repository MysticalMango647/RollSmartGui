import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg



app = QApplication(sys.argv)
pg.plot(x = [0, 5, 6, 2], y = [1, 9, 10, 15])
status = app.exec_()
sys.exit(status)