# coding=ascii

import json
import os

from PySide2 import QtWidgets

from maya import cmds

from Parts.Helpers import mayaUtils
from Parts.Helpers.context import UnlockNode
from Parts.Helpers.UI.collapsingHeader import CollapsingHeader
from Parts.Helpers.UI.comboBox import ComboBox


class AssetWidget(CollapsingHeader):
    
    def __init__(self, ref_node: str, parent: QtWidgets.QWidget):
        super(AssetWidget, self).__init__(ref_node, parent=parent)
        
        self._parts = {}
        self._ref_node = ref_node
        self._data = self.__get_data()

        for part_type, part_data in self._data.items():
            self._parts[part_type] = None
            self.__add_part(part_type, part_data)
        
        self.add_stretch()
    
    def __add_part(self, part_type: str, part_data: dict):
        part_widget = ComboBox(part_type, self)
        items = [x for x in part_data.keys()]
        part_widget.add_items(items)
        self.__set_part_from_scene(part_widget, items)
        part_widget.changed.connect(self._import_part)
        self.add_widget(part_widget)

    def __get_data(self) -> dict:
        asset_path = self.asset_path(self._ref_node)
        with open(asset_path, "r") as handle:
            asset_name = self._ref_node.replace("RN", "")
            return json.load(handle).get(asset_name, dict)        
     
    def __set_part_from_scene(self, part_widget: QtWidgets.QWidget, items: list):
        outputs = cmds.listConnections(f"{self._ref_node}.message",
                                       source=False, destination=True, type="reference") or []
        for ref_node in outputs:
            part_type = cmds.getAttr(f"{ref_node}.partType")
            if part_type != part_widget.type:
                continue

            part_name = cmds.getAttr(f"{ref_node}.partName")
            if part_name not in items:
                mayaUtils.remove_reference(ref_node)
            else:
                part_widget.current_index = items.index(part_name)
                self._parts[part_widget.type] = ref_node
    
    def __set_ref_node(self, ref_node: str, part_type: str, part_name: str):
        with UnlockNode(ref_node):
            cmds.addAttr(ref_node, longName="className", dataType="string")
            cmds.addAttr(ref_node, longName="partType", dataType="string")
            cmds.addAttr(ref_node, longName="partName", dataType="string")
            cmds.addAttr(ref_node, longName="parentRef", attributeType="message")

            cmds.setAttr(f"{ref_node}.className", "PartReference", type="string")
            cmds.setAttr(f"{ref_node}.partType", part_type, type="string")
            cmds.setAttr(f"{ref_node}.partName", part_name, type="string")
            cmds.connectAttr(f"{self._ref_node}.message", f"{ref_node}.parentRef", force=True)
    
    def _get_maya_file(self, partial_path: str) -> str:
        asset_path = self.asset_path(self._ref_node)
        root_path = os.path.split(asset_path)[0]
        return os.path.normpath(os.path.join(root_path, partial_path))
    
    def _constrain_joints(self, ref_node: str):
        asset_nodes = cmds.ls(cmds.referenceQuery(self._ref_node, nodes=True), type="joint", long=True)
        map_asset_nodes = {x.split('|')[-1].split(':')[-1]: x for x in asset_nodes}
        part_nodes = cmds.ls(cmds.referenceQuery(ref_node, nodes=True), type="joint", long=True)
        map_part_nodes = {x.split('|')[-1].split(':')[-1]: x for x in part_nodes}
        
        for key, node in map_part_nodes.items():
            if key not in map_asset_nodes:
                continue
            cmds.parentConstraint(map_asset_nodes[key], node, maintainOffset=False)

    def _import_part(self):
        widget = self.sender()
        if self._parts.get(widget.type):
            print(self._parts[widget.type])
            mayaUtils.remove_reference(self._parts[widget.type])
        
        if widget.current_name != "None":
            partial_path = self._data[widget.type][widget.current_name]
            part_path = self._get_maya_file(partial_path)
            ref_node = mayaUtils.import_reference(part_path, widget.current_name)
            self.__set_ref_node(ref_node, widget.type, widget.current_name)
            self._constrain_joints(ref_node)
            self._parts[widget.type] = ref_node
        else:
            self._parts[widget.type] = None

    @classmethod
    def is_asset(cls, ref_node: str):
        asset_path = cls.asset_path(ref_node)
        return os.path.exists(asset_path)

    @classmethod
    def asset_path(cls, ref_node: str) -> str:
        ref_path = cmds.referenceQuery(ref_node, filename=True)
        return f"{os.path.splitext(ref_path)[0]}.json"
