from qtpy import QtWidgets

from .node_editor import NodeEditor


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    editor = NodeEditor()
    editor.show()
    app.exec_()
