# coding=ascii

import json
import os
from typing import Union

from maya import cmds

from Parts_Callback.Helpers.logger import log


kManip = "Manip"


def get_asset_path(ref_node: str) -> str:
    ref_path = cmds.referenceQuery(ref_node, filename=True)
    return f"{os.path.splitext(ref_path)[0]}.json"


def get_asset_data(ref_node: str) -> dict:
    asset_path = get_asset_path(ref_node)
    with open(asset_path, "r") as handle:
        asset_name = ref_node.replace("RN", "")
        return json.load(handle).get(asset_name, dict)  


def get_maya_file(ref_node: str, partial_path: str) -> str:
    asset_path = get_asset_path(ref_node)
    root_path = os.path.split(asset_path)[0]
    return os.path.normpath(os.path.join(root_path, partial_path))


def find_manipulators(types: Union[str, list] = None) -> list:
    if isinstance(types, str):
        types = [types]

    manipulators = []
    attrs = cmds.ls("::*.className", long=True)
    for attr in attrs:
        if cmds.getAttr(attr) == kManip:
            node = attr.split(".")[0]
            if types and cmds.getAttr(f"{node}.type") not in types:
                continue
            manipulators.append(node)
    
    return manipulators
