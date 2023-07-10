# coding=ascii

from maya import cmds

from Parts.Helpers.context import CleanFosterParent


def remove_reference(ref_node: str):
    with CleanFosterParent():
        ref_path = cmds.referenceQuery(ref_node, filename=True)
        cmds.file(ref_path, removeReference=True)


def import_reference(file_path: str, namespace: str) -> str:
    reference_path = cmds.file(file_path, reference=True, namespace=namespace)
    return cmds.file(reference_path, q=True, referenceNode=True)