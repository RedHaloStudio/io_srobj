# SPDX-License-Identifier: GPL-2.0-or-later

# <pep8-80 compliant>

bl_info = {
    "name": "Silkroad OBJ format",
    "author": "Perry, edit(RedHalo Studio-发霉的红地蛋)",
    "description": "Import silkroad models with vertgroups.",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
	"api": 35622,
    "location": "File > Import > srobj,File > Export > srobj",
    "url": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}

import bpy
from .import_srobj import *
from .export_srobj import *

classes = (
    IMPORT_OT_psk,
    EXPORT_OT_psk
)

def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_psk.bl_idname, text="Silkroad Object (.srobj)")

def menu_func_export(self, context):
    self.layout.operator(EXPORT_OT_psk.bl_idname, text="Silkroad Object (.srobj)")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
