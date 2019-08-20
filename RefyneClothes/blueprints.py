import bpy

class BlueprintItem(bpy.types.PropertyGroup):
    """Blueprint"""
    name = bpy.props.StringProperty(name="Name", description="A name for this item", default="Untitled")
    random_prop = bpy.props.StringProperty(name="Any other property you want", description="", default="")

class REFYNE_UL_blueprints(bpy.types.UIList):
    """Displays all active blueprints"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname): 
        custom_icon = 'OBJECT_DATAMODE'  
        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(item.name, icon = custom_icon)
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label("", icon = custom_icon)

class REFYNE_OT_add_blueprint(bpy.types.Operator):
    """Adds a blueprint"""
    bl_idname = "refyne.add_blueprint"
    bl_label = "Add Blueprint"

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'OBJECT'

    def execute(self, context):
        
        context.scene.blueprint_list.add()

        return {'FINISHED'}

class REFYNE_OT_remove_blueprint(bpy.types.Operator):
    """Removes a blueprint"""
    bl_idname = "refyne.remove_blueprint"
    bl_label = "Remove Blueprint"

    @classmethod 
    def poll(cls, context): 
        return context.mode == 'OBJECT' and context.scene.blueprint_list

    def execute(self, context):
        
        blueprint_list = context.scene.blueprint_list 
        index = context.scene.blueprint_list_index 
        blueprint_list.remove(index) 
        context.scene.blueprint_list_index = min(max(0, index - 1), len(blueprint_list) - 1)

        return {'FINISHED'}