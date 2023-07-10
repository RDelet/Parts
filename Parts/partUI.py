# coding=ascii

from maya import cmds

from Parts.Helpers.UI.mayaWidget import MayaWidget
from Parts.assetWidget import AssetWidget



class PartUI(MayaWidget):

    def __init__(self):
        super(PartUI, self).__init__()
        
        self.setWindowTitle("AskARigger | Part UI")
        self._ref_widgets = []
        self._update()
        self.add_stretch()
    
    def _clear(self):
        for ref_widget in self._ref_widgets:
            ref_widget.close()
        self._ref_widgets = []

    def _update(self):
        self._clear()
        ref_nodes = cmds.ls(type="reference")
        for ref_node in ref_nodes:
            if not AssetWidget.is_asset(ref_node):
                continue
            self.__add_asset(ref_node)
    
    def __add_asset(self, ref_node: str) :
        if self.__is_part(ref_node):
            return

        ref_widget = AssetWidget(ref_node, self)
        self._ref_widgets.append(ref_widget)
        self._master_layout.addWidget(ref_widget)
    
    @classmethod
    def __is_part(cls, ref_node: str) -> bool:
        class_name_attr = f"{ref_node}.className"
        if cmds.objExists(class_name_attr):
            class_name = cmds.getAttr(class_name_attr)
            if class_name == "PartReference":
                return True
        
        return False
    
    def __is_asset(self):
        pass
