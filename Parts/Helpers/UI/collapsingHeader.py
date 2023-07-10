
# coding=ascii

from PySide2 import QtCore, QtWidgets


class CollapsingHeader(QtWidgets.QWidget):

    def __init__(self, title, expended: bool = False,
                 header_color: list = [255, 137, 11], parent=None):
        super(CollapsingHeader, self).__init__(parent)

        self._expanded = expended
        
        self._master_layout = QtWidgets.QVBoxLayout(self)
        self._master_layout.setContentsMargins(0, 0, 0, 0)
        self._master_layout.setSpacing(0)

        # Header
        self._header = QtWidgets.QFrame()
        self._header.setObjectName('HeaderWidget')
        self._header.setFixedHeight(20)
        self._master_layout.addWidget(self._header)

        self._expand_button = QtWidgets.QToolButton()
        self._expand_button.setArrowType(QtCore.Qt.RightArrow)
        self._expand_button.setStyleSheet('QToolButton { border: none; }')
        self._expand_button.clicked.connect(self.__on_expand_clicked)

        self._header_label = QtWidgets.QLabel(title)
        self._header_label.setObjectName('HeaderLabel')
        self._header_label.setStyleSheet('font: bold;')

        header_layout = QtWidgets.QHBoxLayout(self._header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(self._expand_button)
        header_layout.addWidget(self._header_label)
        header_layout.addStretch()

        self._header.setStyleSheet(
            """
            #HeaderWidget {{
                padding-left: 4px;
                border-radius: 3px;
                background-color: rgb({0}, {1}, {2});
            }}
            """.format(*header_color)
        )

        # Main widget
        self._main_widget = QtWidgets.QWidget(self)
        self._main_widget.setVisible(self._expanded)
        self._master_layout.addWidget(self._main_widget)

        self._main_layout = QtWidgets.QVBoxLayout(self._main_widget)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

    def add_widget(self, widget: QtWidgets.QWidget):
        self._main_layout.addWidget(widget)

    def set_expanded(self, expanded: bool):
        self._expanded = expanded
        arrow = QtCore.Qt.DownArrow if self._expanded else QtCore.Qt.RightArrow
        self._expand_button.setArrowType(arrow)
        self._main_widget.setVisible(self._expanded)

    def __on_expand_clicked(self):
        self.set_expanded(self._expand_button.arrowType() == QtCore.Qt.RightArrow)
    
    def add_stretch(self):
        self._main_layout.addStretch()
