# Clothing Generation Plugin (for clothing brands)

This plugin allows clothing brands to convert manufacturing blueprints of shorts and shirts into virtual 3D models of clothes. These clothing models can then be browsed via our web-based dressing room application. 

## How to Use

When it comes to modeling clothes, the process can be broken down into 4 steps:
1) Model blueprints using 2D planes
2) Arrange 2D planes around imported human
3) Stitch 2D planes together
4) Render final product and adjust seams based on tension

![Imgur](https://i.imgur.com/EoPT1g1.png)

### Modeling

After importing a blueprint, navigate to the main menu on the left as shown above. There are 5 tools under the modeling tab. `Start Modeling` will create a new project. The next three tools will help you outline each piece of the blueprint. It is recommended to start with straight lines and then add curves where necessary. When all outlines are finished, use the `Create Plane` to add mesh to your outlines. These 2D meshes will eventually be stitched to form 3D clothes.  

### Human

Next, import a basic human by clicking the `Import Human` button. Arrange the 2D pieces of clothes modeled in the previous step near where it would appear on a dressed human. 

### Sewing

![Imgur](https://i.imgur.com/GClGUva.png)

This is the heart of the program, turning 2D planes in 3D clothing models by "sewing" them together. Click the `Sew` button and then two edges you wish to be sewn together. You will be prompted to enter the number of seams and the type of stitching. We reccomend an even number of seams and normal stitching to begin with.

### Rendering

Finally, click the `Render` button to see how everything looks! Enabling `Tension` will allow you to see where the clothes are loose and tight and how to make adjustments. 

Note: Our rendering engine is actually Blender's real-time EEVEE engine, so it will work with speed and reliabilty. 
