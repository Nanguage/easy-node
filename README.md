# Easy node

Easynode is a Python package offering a suite of components for building Node editor-based GUI applications, characterized by its simplicity, configurability, and a decoupled design that separates interface display logic from node computation scheduling logic.


**Work in progress**


## TODO list

+ [x] Auto layout.
+ [x] Setting for each node(color, size, etc).
+ [x] Node status bar.
+ [x] Signals and slots.
+ [x] Port widget for editing port value.
+ [x] Node factory and registration.
+ [x] Multiple scenes.
+ [x] Node list for search and add widget.
+ [x] Undo/Redo.
+ [x] Serialization / Deserialization.
    * [x] Save the state of the port widgets.
+ [x] Copy and paste.
+ [x] Signals for hover, select, etc.
+ [x] Node right click menu.
+ [ ] Node and port documentation.
+ [ ] Menu.
+ [ ] Allow change config at runtime with UI.


## Signals

| Item | Signal | Value type | Description |
| --- | --- | --- | --- |
| Node | `.selected_changed` | `bool` | Emitted when the node is selected or unselected. |
| Node | `.position_changed` | `QtCore.QPointF` | Emitted when the node position is changed. |
| Node | `renamed` | `str` | Emitted when the node is renamed. |
| Port | `.edge_added` | `Edge` | Emitted when an edge is added to the port. |
| Port | `.edge_removed` | `Edge` | Emitted when an edge is removed from the port. |
| Edge | `.selected_changed` | `bool` | Emitted when the edge is selected or unselected. |
| Graph | `.elements_changed` | `None` | Emitted when the graph elements(nodes and edges) is changed. |
| Graph | `.node_added` | `Node` | Emitted when a node is added to the graph. |
| Graph | `.node_removed` | `Node` | Emitted when a node is removed from the graph. |
| Graph | `.edge_added` | `Edge` | Emitted when an edge is added to the graph. |
| Graph | `.edge_removed` | `Edge` | Emitted when an edge is removed from the graph. |
| GraphicsView | `.selected_node_items_moved` | `QtCore.QPointF` | Emitted when the selected nodes are moved. |
| GraphicsView | `.edge_drag_mode_changed` | `bool` | Emitted when the edge drag mode is changed. |
| NodeEditor | `.scene_added` | `GraphicsScene` | Emitted when a scene is added to the node editor. |
| NodeEditor | `.scene_removed` | `GraphicsScene` | Emitted when a scene is removed from the node editor. |
| NodeEditor | `.view_changed` | `GraphicsView` | Emitted when the view is changed. |
