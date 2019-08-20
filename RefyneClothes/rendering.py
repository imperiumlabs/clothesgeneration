import bpy

class REFYNE_OT_render(bpy.types.Operator):
    """Renders clothing interaction"""
    bl_idname = "refyne.render"
    bl_label = "Render"

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'OBJECT'

    def execute(self, context):

        bpy.ops.screen.animation_play()

        return {'FINISHED'}
