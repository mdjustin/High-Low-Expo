# HighLowExpo
A Simple Python tool designed for users to rename and group meshes for exporting to Substance Painter.

This tool has been originally desinged to help students, and others just getting into the flow of using Substance Painter and the workflow of naming meshes correctly to use the "By Mesh Name" baking option within Painter.

## Installation:

Video Installation Instructions : {Coming soon}

1. To install this script, place the ***high_low_expo.py*** file within your Maya's script directory. 
2. Inside maya, create a new shelf button set to python with the script :
```
  from high_low_expo import HighLowDialog

  HighLowDialog.show_dialog()
```
3. Enjoy the functionality and sorting powers of High Low Expo.





## Instructions for Use.
This section will outline what all the buttons will do within the tool. 
Video demonstration : {Coming Soon}

***Create High/Low Layers*** - This button will create a pair of Maya display layers, one named High_Poly and one named Low_poly.

***Rename text box*** - This is where you can enter a custom name for your mesh. 

***Make High & Make Low*** - These buttons will take the custom name in your Rename Text Box and add the corrisponding suffix to the mesh name, as well as moving the mesh onto the matching display layer, and an internal group group for other functions within the tool. If there is no name in the Rename Text Box, the mesh will just be named _high or _low based on which button you have made. 

***Set High & set Low*** - These buttons wil not rename your mesh, but will move them into the corrisponding display layer, and internal group. 

***Hide/Show Low/High Poly Meshes*** - Toggling these checkboxes will let you hide and unhide your meshs that have already been sorted within the display groups. 

***Export Location*** - This will let you select the folder in which you would like to export your meshes too. 

***File Name text box*** - This lets you set a name for your file, before exporting. 

***Export High/Low Meshes*** - These buttons will export the corrisponding mesh groups to the chosen folder with the chosen file name, without using the export UI. It exports your meshes as FBX format. 

***Help*** - Takes you to this page. 

***Close*** - Cloeses/hides the UI. 
