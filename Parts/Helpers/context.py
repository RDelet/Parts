from typing import Union

from maya import cmds


class Context(object):

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self, *args, **kwargs):
        raise NotImplementedError('{0}.__enter__ need to be reimplemented !'.format(self.__class__.__name__))

    def __exit__(self, *args, **kwargs):
        raise NotImplementedError('{0}.__exit__ need to be reimplemented !'.format(self.__class__.__name__))


class UnlockNode(Context):

    def __init__(self, nodes: Union[str, list]):
        super(UnlockNode, self).__init__()
        if isinstance(nodes, str):
            nodes = [nodes]
        self._nodes = nodes

    def __enter__(self):
        cmds.lockNode(self._nodes, lock=False)

    def __exit__(self, *args):
        cmds.lockNode(self._nodes, lock=True)


class CleanFosterParent(Context):

    kFosterParent = "fosterParent"

    def __init__(self):
        super(CleanFosterParent, self).__init__()
        self._nodes = []

    def __enter__(self):
        self._nodes = cmds.ls(type=self.kFosterParent, long=True)

    def __exit__(self, *args):
        nodes = cmds.ls(type=self.kFosterParent, long=True)
        for node in nodes:
            if node not in self._nodes:
                cmds.delete(node)
