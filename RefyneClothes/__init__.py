# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

bl_info = {
    "name" : "Clothes Modeling",
    "author" : "Nikhil Sridhar",
    "description" : "Assists in modeling clothes",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

from . main import REFYNE_PT_main
from .blueprints import BlueprintItem, REFYNE_UL_blueprints, REFYNE_OT_add_blueprint, REFYNE_OT_remove_blueprint
from . modeling import REFYNE_OT_start_modeling, REFYNE_OT_create_segment, REFYNE_OT_linear_spline, REFYNE_OT_curved_spline, REFYNE_OT_create_plane
from . human import REFYNE_OT_import_human
from . sewing import REFYNE_OT_sew
from . rendering import REFYNE_OT_render

classes = [REFYNE_PT_main, 
        BlueprintItem, REFYNE_UL_blueprints, REFYNE_OT_add_blueprint, REFYNE_OT_remove_blueprint,
        REFYNE_OT_start_modeling, REFYNE_OT_create_segment, REFYNE_OT_linear_spline, REFYNE_OT_curved_spline, REFYNE_OT_create_plane,
        REFYNE_OT_import_human,
        REFYNE_OT_sew, 
        REFYNE_OT_render]

def updateTMSettings(self, context):
    # Updates settings
    bpy.context.object.data.tm_active = not bpy.context.object.data.tm_active
    bpy.context.object.data.tm_enable_vertex_colors = not bpy.context.object.data.tm_enable_vertex_colors

    # Sets nodes

    obj = bpy.context.active_object
    # Creates a new material
    tension_mat = bpy.data.materials.new(name="Tension")
    tension_mat.use_nodes = True
    # Removes default nodes
    nodes = tension_mat.node_tree.nodes
    for node in nodes:
        if node.type != 'OUTPUT_MATERIAL':
                nodes.remove(node)
    # Creates new nodes
    attribute_node = tension_mat.node_tree.nodes.new('ShaderNodeAttribute')
    diffuse_node = tension_mat.node_tree.nodes.new('ShaderNodeBsdfDiffuse')
    attribute_node.attribute_name = "tm_tension"
    # Links nodes
    output_node = tension_mat.node_tree.nodes.get('Material Output')
    tension_mat.node_tree.links.new(attribute_node.outputs[0], diffuse_node.inputs[0])
    tension_mat.node_tree.links.new(output_node.inputs[0], diffuse_node.outputs[0])
    obj.active_material = tension_mat

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    # bpy.types.Scene.blueprint_list = bpy.props.CollectionProperty(type = BlueprintItem) 
    # bpy.types.Scene.blueprint_list_index = bpy.props.IntProperty(name = "Index for blueprint_list", default = 0)
    bpy.types.Scene.tension_map = bpy.props.BoolProperty(
        name="Tension Map",
        description="Enables tension map for simulation",
        update=updateTMSettings)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    # del bpy.types.Scene.blueprint_list 
    # del bpy.types.Scene.blueprint_list_index
    del bpy.types.Scene.tension_map