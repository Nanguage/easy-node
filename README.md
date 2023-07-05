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
+ [ ] Node right click menu.
+ [ ] Node and port documentation.
+ [ ] Menu.
+ [ ] Allow change config at runtime with UI.


## Signals

| Item | Signal | Description |
| --- | --- | --- |
| Node | `.selected_changed` | Emitted when the node is selected or unselected. |
| Node | `.position_changed` | Emitted when the node position is changed. |
| Port | `.edge_added` | Emitted when an edge is added to the port. |
| Port | `.edge_removed` | Emitted when an edge is removed from the port. |
| Edge | `.selected_changed` | Emitted when the edge is selected or unselected. |
| GraphicsView | `.selected_node_items_moved` | Emitted when the selected nodes are moved. |
| GraphicsView | `.edge_drag_mode_changed` | Emitted when the edge drag mode is changed. |
