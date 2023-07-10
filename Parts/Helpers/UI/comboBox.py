# coding=ascii

from PySide2 import QtCore, QtWidgets


class ComboBox(QtWidgets.QWidget):
    
    changed = QtCore.Signal()
    
    def __init__(self, title: str, parent: QtWidgets.QWidget = None):
        super(ComboBox, self).__init__(parent)
        
        self._type = title
        self._master_layout = QtWidgets.QHBoxLayout(self)
        self._master_layout.setSpacing(0)
        self._master_layout.setContentsMargins(0, 0, 0, 0)
        
        self._label = QtWidgets.QLabel(title, self)
        self._master_layout.addWidget(self._label)
        
        self._combo_box = QtWidgets.QComboBox(self)
        self._combo_box.currentIndexChanged.connect(self.__on_index_changed)
        self._master_layout.addWidget(self._combo_box)
    
    def add_items(self, item_names: list):
        self._combo_box.addItems(item_names)
    
    @property
    def current_name(self) -> str:
        return self._combo_box.currentText()
    
    @property
    def type(self):
        return self._type
    
    @property
    def current_index(self) -> int:
        return self._combo_box.currentIndex()
    
    @current_index.setter
    def current_index(self, index: int) -> int:
        return self._combo_box.setCurrentIndex(index)

    def __on_index_changed(self, *args):
        self.changed.emit()