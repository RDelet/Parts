# coding=ascii

from maya import cmds, OpenMaya

from Parts.Helpers.context import CleanFosterParent


def get_object(node: str) -> OpenMaya.MObject:
    try:
        msl = OpenMaya.MSelectionList()
        msl.add(node)
        obj = OpenMaya.MObject()
        msl.getDependNode(0, obj)
        return obj
    except:
        raise RuntimeError(f"Node {node} does not exists !")


def remove_reference(ref_node: str):
    with CleanFosterParent():
        ref_path = cmds.referenceQuery(ref_node, filename=True)
        cmds.file(ref_path, removeReference=True)


def import_reference(file_path: str, namespace: str) -> str:
    reference_path = cmds.file(file_path, reference=True, namespace=namespace)
    return cmds.file(reference_path, q=True, referenceNode=True)