# coding=ascii

import json
import os

from maya import cmds, OpenMaya

from Parts_Callback.Helpers.context import UnlockNode
from Parts_Callback.Helpers import mayaUtils
from Parts_Callback.Helpers import assetUtils
from Parts_Callback.Helpers.mayaInstances import node_instances


class Asset(object):
    
    kAssetSettings = "AssetSettings"

    def __init__(self, manipulator: str, ref_node: str):
        self._manipulator = manipulator
        self._shape_settings = self.__find_asset_shape()
        self._ref_node = ref_node
        self._data = assetUtils.get_asset_data(self._ref_node)
        self._parts = {}
        self._part = None
        self.__callback = None
        self._init_asset()
    
    def __del__(self):
        if self.__callback:
            OpenMaya.MMessage.removeCallback(self.__callback)
            self.__callback = None
    
    def _init_asset(self):
        if not self._shape_settings:
            self.__add_asset_shape()

        obj = mayaUtils.get_object(self._shape_settings)
        self.__callback = OpenMaya.MNodeMessage.addAttributeChangedCallback(obj, self.__on_attribute_change)
        node_instances.add(obj, self)
        
        for attr_name, part_data in self._data.items():
            node_attr = f"{self._shape_settings}.{attr_name}"
            self._parts[attr_name] = [x for x in part_data.keys()]
            enum_names = ":".join(self._parts[attr_name])
            if not cmds.objExists(node_attr):
                cmds.addAttr(self._shape_settings, longName=attr_name,
                             attributeType="enum", enumName=enum_names, keyable=True, readable=True)
            else:
                cmds.addAttr(node_attr, edit=True, enumName=enum_names)
    
    def __find_asset_shape(self) -> str:
        shapes = cmds.listRelatives(self._manipulator, shapes=True, fullPath=True)
        for shape in shapes:
            shape_attr = f"{shape}.className"
            if not cmds.objExists(shape_attr):
                continue
            if cmds.getAttr(shape_attr) == self.kAssetSettings:
                return shape

    def __add_asset_shape(self):
        curve_transform = cmds.curve(degree=1, knot=0, point=(0, 0, 0))
        curve_shape = cmds.listRelatives(curve_transform, shapes=True, fullPath=True)[0]
        curve_shape = cmds.rename(curve_shape, f"{self._manipulator}_AssetSettings")
        cmds.addAttr(curve_shape, longName="className", dataType="string")
        cmds.setAttr(f"{curve_shape}.className", self.kAssetSettings, type="string")
        self._shape_settings = cmds.ls(cmds.parent(curve_shape, self._manipulator, relative=True, shape=True), long=True)[0]
        cmds.delete(curve_transform)
    
    def __on_attribute_change(self, msg, plug, other_plug, client_data):
        node, attr = plug.name().split(".")
        if attr not in self._parts:
            return
        part_name = self._parts[attr][plug.asInt()]
        self._import_part(attr, part_name)
        cmds.select(self._manipulator)
    
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
    
    def _constrain_joints(self, ref_node: str):
        asset_nodes = cmds.ls(cmds.referenceQuery(self._ref_node, nodes=True), type="joint", long=True)
        map_asset_nodes = {x.split('|')[-1].split(':')[-1]: x for x in asset_nodes}
        part_nodes = cmds.ls(cmds.referenceQuery(ref_node, nodes=True), type="joint", long=True)
        map_part_nodes = {x.split('|')[-1].split(':')[-1]: x for x in part_nodes}
        
        for key, node in map_part_nodes.items():
            if key not in map_asset_nodes:
                continue
            cmds.parentConstraint(map_asset_nodes[key], node, maintainOffset=False)

    def _import_part(self, attr: str, part_name: str):
        if self._part:
            mayaUtils.remove_reference(self._part)
        
        if part_name != "None":
            partial_path = self._data[attr][part_name]
            part_path = assetUtils.get_maya_file(self._ref_node, partial_path)
            ref_node = mayaUtils.import_reference(part_path, part_name)
            self.__set_ref_node(ref_node, attr, part_name)
            self._constrain_joints(ref_node)
            self._part = ref_node
        else:
            self._part = None
