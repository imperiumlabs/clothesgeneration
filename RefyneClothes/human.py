import bpy
import os

class REFYNE_OT_import_human(bpy.types.Operator):
    """Imports 3D human"""
    bl_idname = "refyne.import_human"
    bl_label = "Import Human"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'OBJECT'

    def execute(self, context):

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'human.dae')
        bpy.ops.wm.collada_import(filepath=filename)
        bpy.context.active_object.name = 'human'
        bpy.ops.object.modifier_add(type='COLLISION')
        bpy.ops.object.select_all(action='DESELECT')

        return {'FINISHED'}