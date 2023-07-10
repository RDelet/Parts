# coding=ascii

from PySide2 import QtWidgets
from shiboken2 import wrapInstance

from maya import OpenMayaUI


class MayaWidget(QtWidgets.QMainWindow):

    def __init__(self, parent: QtWidgets.QWidget = None):
        if parent is None:
            parent = self.get_main_window()
        super(MayaWidget, self).__init__(parent)
        
        self._master_widget = QtWidgets.QWidget(self)
        self._master_layout = QtWidgets.QVBoxLayout(self._master_widget)
        self._master_layout.setSpacing(0)
        self._master_layout.setContentsMargins(0, 0, 0, 0)

        self.setCentralWidget(self._master_widget)
    
    @classmethod
    def get_main_window(cls):
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        return wrapInstance(int(ptr), QtWidgets.QWidget)
    
    def add_stretch(self):
        self._master_layout.addStretch()
