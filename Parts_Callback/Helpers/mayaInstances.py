# coding=ascii

from typing import Union

from maya import OpenMaya

from Parts_Callback.Helpers import mayaUtils


class MayaInstances(object):

    __ALL_INSTANCES = []

    def __init__(self):
        self.__instances = {}
        self.__ALL_INSTANCES.append(self)
        self.__callback_id = OpenMaya.MDGMessage_addNodeRemovedCallback(self.remove)

    def __del__(self):
        OpenMaya.MMessage_removeCallback(self.__callback_id)

    @property
    def instances(self) -> dict:
        return self.__instances

    @staticmethod
    def __check_node(node: Union[str, OpenMaya.MObject, OpenMaya.MDagPath]):
        if isinstance(node, str):
            node = mayaUtils.get_object(node)
        elif isinstance(node, OpenMaya.MDagPath):
            node = node.node()
        return OpenMaya.MObjectHandle(node)

    @staticmethod
    def __is_valid(handle: OpenMaya.MObjectHandle):
        return not handle.object().isNull() and handle.isValid() and handle.isAlive()

    def get(self, node):
        handle = self.__check_node(node)
        if self.__is_valid(handle):
            hsh = handle.hashCode()
            hx = "%x" % hsh
            if hx in self.__instances:
                instance = self.__instances[hx]
                instance.object = node
                return instance

    def add(self, node: Union[str, OpenMaya.MObject, OpenMaya.MDagPath], value: object):
        handle = self.__check_node(node)
        if self.__is_valid(handle):
            hsh = handle.hashCode()
            hx = "%x" % hsh
            if hx not in self.__instances:
                self.__instances[hx] = value

    def remove(self, node: Union[str, OpenMaya.MObject, OpenMaya.MDagPath], *args, **kwargs):
        handle = self.__check_node(node)
        if self.__is_valid(handle):
            hsh = handle.hashCode()
            hx = "%x" % hsh
            if hx in self.__instances:
                del self.__instances[hx]

    @classmethod
    def clear(cls, *args, **kwargs):
        for instance in cls.__ALL_INSTANCES:
            instance.__instances = {}


OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kMayaExiting, MayaInstances.clear)
OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterNew, MayaInstances.clear)
node_instances = MayaInstances()
