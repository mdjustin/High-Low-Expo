from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

import maya.cmds as cmds

# Lists of objects.
List_High = []
List_Low = []
Tri_List = []

test = QtWidgets.QSpacerItem(0, 10)

def maya_main_window():
    """
    Return the Maya main window widget as a Python Object. 
    """
    main_window_prt = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_prt), QtWidgets.QWidget)
    
    
class HighLowDialog(QtWidgets.QDialog):
    
    dig_instance = None
    
    @classmethod
    def show_dialog(cls):
        if not cls.dig_instance:
            cls.dig_instance = HighLowDialog()
            
        if cls.dig_instance.isHidden():
            cls.dig_instance.show()
        else:
            cls.dig_instance.raise_()
            cls.dig_instance.activateWindow()
            
    
    def __init__(self, parent=maya_main_window()):
        super(HighLowDialog, self).__init__(parent)
        
        self.setWindowTitle("High Low Expo")
        self.setMinimumSize(350, 480)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
    # Buttons for the wdiget.
    def create_widgets(self):
        self.layer_btn = QtWidgets.QPushButton("Create High/Low Layers")
        self.rename_le = QtWidgets.QLineEdit("")
        self.high_Suffix = QtWidgets.QLineEdit("_high")
        self.low_Suffix = QtWidgets.QLineEdit("_low")
        self.high_btn = QtWidgets.QPushButton("Make High")
        self.low_btn = QtWidgets.QPushButton("Make Low")
        self.addh_btn = QtWidgets.QPushButton("Set High")
        self.addl_btn = QtWidgets.QPushButton("Set Low")
        self.toggleh_btn = QtWidgets.QCheckBox("Hide/Show High Poly Meshes")
        self.togglel_btn = QtWidgets.QCheckBox("Hide/Show Low Poly Meshes")
        self.exporth_btn = QtWidgets.QPushButton("Export High Meshes")
        self.exportl_btn = QtWidgets.QPushButton("Export Low Meshes")
        self.triangulate_btn = QtWidgets.QPushButton("Triangulate")
        self.toggleT_chbx = QtWidgets.QCheckBox("Hide/Show Triangulated Meshes")
        self.exportT_btn = QtWidgets.QPushButton("Export Triangulated Meshes")
        self.close_btn = QtWidgets.QPushButton("Close")
        self.filepath_le = QtWidgets.QLineEdit()
        self.select_file_path_btn = QtWidgets.QPushButton()
        self.set_file_name_le = QtWidgets.QLineEdit()
        self.help_btn = QtWidgets.QPushButton("Help")
        
        self.layer_btn.setToolTip("Create High and Low Display Layers.")      
        self.rename_le.setToolTip("Choose a name for your mesh.")
        self.high_Suffix.setToolTip("The name of the high suffix, that will be added to the end of the mesh name.")
        self.low_Suffix.setToolTip("The name of the low suffix, that will be added to the end of the mesh name.")
        self.high_btn.setToolTip("Add the high to the end of your mesh name, and assign it to the correct group.")
        self.low_btn.setToolTip("Add the low suffix to the end of your mesh name, and assign it to the correct group.")
        self.addh_btn.setToolTip("Don't rename the mesh, but assign it to the correct group.")
        self.addl_btn.setToolTip("Don't rename the mesh, but assign it to the correct group.")
        self.toggleh_btn.setToolTip("Toggle the visability of the High Poly Mesh group.")
        self.togglel_btn.setToolTip("Toggle the visability of the Low Poly Mesh group.")
        self.triangulate_btn.setToolTip("Triagulate the Low Meshes")
        self.toggleT_chbx.setToolTip("Toggle the visability of the Triangulated Mesh group.")
        self.exporth_btn.setToolTip("Export the High Poly Mesh group.")
        self.exportl_btn.setToolTip("Export the Low Poly Mesh group.")
        self.exportT_btn.setToolTip("Export the Triangulated Mesh group.")
        self.filepath_le.setToolTip("The location where you files will be expoerted.")  
        self.select_file_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.select_file_path_btn.setToolTip("Select export location.")    
        self.set_file_name_le.setToolTip("Set the file name that will be exported.")
        self.help_btn.setToolTip("Get help - Loads a webpage")
    
    #Layout of the widgets.
    def create_layout(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.high_btn)
        button_layout.addWidget(self.low_btn)

        suffix_layout = QtWidgets.QHBoxLayout()
        suffix_layout.addWidget(self.high_Suffix)
        suffix_layout.addWidget(self.low_Suffix)
        
        rename_layout = QtWidgets.QHBoxLayout()
        rename_layout.addWidget(self.rename_le)
        
        addbtn_layout = QtWidgets.QHBoxLayout()
        addbtn_layout.addWidget(self.addh_btn)
        addbtn_layout.addWidget(self.addl_btn)
        
        toggle_layout = QtWidgets.QVBoxLayout()
        toggle_layout.addWidget(self.toggleh_btn)
        toggle_layout.addWidget(self.togglel_btn)
        

        file_path_layout = QtWidgets.QHBoxLayout()
        file_path_layout.addWidget(self.filepath_le)
        file_path_layout.addWidget(self.select_file_path_btn)
        
        filename_layout = QtWidgets.QHBoxLayout()
        filename_layout.addWidget(self.set_file_name_le)
        
        tri_layout = QtWidgets.QVBoxLayout()
        tri_layout.addWidget(self.triangulate_btn)
        tri_layout.addWidget(self.toggleT_chbx)
        
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("Rename:", rename_layout)
        form_layout.addRow("Suffixes:", suffix_layout)
        form_layout.addRow(button_layout)
        form_layout.addRow(addbtn_layout)
        form_layout.addRow("", toggle_layout)
        form_layout.addRow("Triangulate Meshes:", tri_layout)
        form_layout.addRow("Export Location:", file_path_layout)
        form_layout.addRow("File Name:", filename_layout)
        
        
        close_layout = QtWidgets.QHBoxLayout()
        close_layout.addStretch()
        close_layout.addWidget(self.help_btn)
        close_layout.addWidget(self.close_btn)
        
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.addWidget(self.layer_btn)
        main_layout.addLayout(rename_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(suffix_layout)
        main_layout.addLayout(addbtn_layout)
        main_layout.addLayout(toggle_layout)
        main_layout.addLayout(file_path_layout)
        main_layout.addLayout(filename_layout)
        main_layout.addLayout(tri_layout)
        main_layout.addLayout(form_layout)
        main_layout.addSpacerItem(test)
        main_layout.addWidget(self.exporth_btn)
        main_layout.addWidget(self.exportl_btn)
        main_layout.addWidget(self.exportT_btn)
        main_layout.addLayout(close_layout)
        
    
    def create_connections(self):
        self.layer_btn.clicked.connect(self.Create_layers)
        self.high_btn.clicked.connect(self.high_rename)
        self.low_btn.clicked.connect(self.low_rename)
        self.addh_btn.clicked.connect(self.addtohigh)
        self.addl_btn.clicked.connect(self.addtolow)
        self.toggleh_btn.toggled.connect(self.H_toggle)
        self.togglel_btn.toggled.connect(self.L_toggle)
        self.select_file_path_btn.clicked.connect(self.show_file_select_dialog)
        self.exporth_btn.clicked.connect(self.ExportHigh)
        self.exportl_btn.clicked.connect(self.ExportLow)
        self.help_btn.clicked.connect(self.HelpLink)
        self.close_btn.clicked.connect(self.close)
        
        self.triangulate_btn.clicked.connect(self.TriangulateLows)
        self.toggleT_chbx.toggled.connect(self.T_toggle)
        self.exportT_btn.clicked.connect(self.ExportTris)
    
    def Create_layers(self):
        if cmds.objExists("Low_Poly"):
            pass
        elif cmds.objExists("High_Poly"):
            pass
        else:
            cmds.createDisplayLayer(noRecurse=True, name='Low_Poly', empty=True)
            cmds.createDisplayLayer(noRecurse=True, name='High_Poly', empty=True)


    def high_rename(self):
        selection = cmds.ls(sl=1, o=1)
        mesh_name = self.rename_le.text()
        high_Suf = self.high_Suffix.text()
        if self.rename_le.text() != "" and self.low_Suffix.text() != "":
            if len(selection) < 1:
                cmds.warning("No mesh selected")
            elif len(selection) > 1:
                cmds.warning("Too many meshes selected")
            else:
                cmds.rename(mesh_name + high_Suf)
                Name = cmds.ls(sl=1, o=1)
                cmds.editDisplayLayerMembers('High_Poly', Name , noRecurse=True)
                Name = cmds.ls(sl=1, o=1)
                Selected = Name[0]
                if Selected in List_High:
                    om.MGlobal.displayInfo("Already in List")
                else:
                    List_High.append(Selected)
                    om.MGlobal.displayInfo("Added to List.")
        else:
            cmds.warning("No Name or Suffix")
        
    def low_rename(self):
        selection = cmds.ls(sl=1, o=1)
        mesh_name = self.rename_le.text()
        low_suf = self.low_Suffix.text()
        if self.rename_le.text() != "" and self.low_Suffix.text() != "":
            if len(selection) < 1:
                cmds.warning("No mesh selected")
            elif len(selection) > 1:
                cmds.warning("Too many meshes selected")
            else:
                cmds.rename(mesh_name + low_suf)
                Name = cmds.ls(sl=1, o=1)
                cmds.editDisplayLayerMembers('Low_Poly', Name , noRecurse=True)
                Name = cmds.ls(sl=1, o=1)
                Selected = Name[0]
                if Selected in List_Low:
                    om.MGlobal.displayInfo("Already in List")
                else:
                    List_Low.append(Selected)
                    om.MGlobal.displayInfo("Added to List.")
        else:
            cmds.warning("No Name or Suffix")
            
    def addtohigh(self):
            Name = cmds.ls(sl=1, o=1)
            cmds.editDisplayLayerMembers('High_Poly', Name , noRecurse=True)
            Name = cmds.ls(sl=1, o=1)
            Selected = Name[0]
            if Selected in List_High:
                om.MGlobal.displayInfo("Already in List")
            else:
                List_High.append(Selected)
                om.MGlobal.displayInfo("Added to List.")
    
    def addtolow(self):
            Name = cmds.ls(sl=1, o=1)
            cmds.editDisplayLayerMembers('Low_Poly', Name , noRecurse=True)
            Name = cmds.ls(sl=1, o=1)
            Selected = Name[0]
            if Selected in List_Low:
                om.MGlobal.displayInfo("Already in List")
            else:
                List_Low.append(Selected)
                om.MGlobal.displayInfo("Added to List.")
        
            
    def H_toggle(self):
        if cmds.objExists("High_poly"):
            HV = cmds.getAttr('High_Poly.visibility')
            if HV == 1:
                cmds.setAttr('High_Poly.visibility', 0 )
            else:
                cmds.setAttr('High_Poly.visibility', 1 ) 
        else:
            pass
            
    def L_toggle(self):
        if cmds.objExists("Low_Poly"):
            HV = cmds.getAttr('Low_Poly.visibility')
            if HV == 1:
                cmds.setAttr('Low_Poly.visibility', 0 )
            else:
                cmds.setAttr('Low_Poly.visibility', 1 ) 
        else:
            pass
            
    def show_file_select_dialog(self):
        file_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder", "")
        if file_path:
            self.filepath_le.setText(file_path)
        return file_path
            
    def ExportHigh(self):
        filePath = self.filepath_le.text()
        fileName = self.set_file_name_le.text()
        if filePath and fileName != "":    
            for each in List_High:
                cmds.select(each, add=True)
            cmds.file(filePath + "/" + fileName, es=True , pr=False, force=True, typ="FBX export")
            cmds.select(cl=True)
            om.MGlobal.displayInfo("Exported High Meshes")
        else:
            cmds.warning("No export location selected. Or no file name chosen.")
                    
    def ExportLow(self):
        filePath = self.filepath_le.text()
        fileName = self.set_file_name_le.text()
        if filePath and fileName != "":  
            for each in List_Low:
                cmds.select(each, add=True)
            cmds.file(filePath + "/" + fileName, es=True , pr=False, force=True, typ="FBX export")
            cmds.select(cl=True)
            om.MGlobal.displayInfo("Exported Low Meshes")
        else:
            cmds.warning("No export location selected. Or no file name chosen.")
        
    def TriangulateLows(self):
        if cmds.objExists("Triangulated"):
            pass
        else:
            cmds.createDisplayLayer(noRecurse=True, name='Triangulated', empty=True)
        for each in Tri_List:
            cmds.select(each, add=True)
            cmds.delete()
        for each in List_Low:
            cmds.select(each, add=True)
            Name = cmds.ls(sl=1, o=1)
            Mesh = Name[0]
            cmds.duplicate()
            cmds.rename('Tri_' + Mesh)
            cmds.Triangulate()
            Tri_List.append(cmds.ls(sl=1, o=1))
            Name = cmds.ls(sl=1, o=1)
            Mesh = Name[0]
            cmds.editDisplayLayerMembers('Triangulated', Name , noRecurse=True)
            cmds.select(clear=True)
        
    def T_toggle(self):
        if cmds.objExists("Triangulated"):
            HV = cmds.getAttr('Triangulated.visibility')
            if HV == 1:
                cmds.setAttr('Triangulated.visibility', 0 )
            else:
                cmds.setAttr('Triangulated.visibility', 1 ) 
        else:
            pass
            
    def ExportTris(self):
        filePath = self.filepath_le.text()
        fileName = self.set_file_name_le.text()
        if filePath and fileName != "":  
            for each in Tri_List:
                cmds.select(each, add=True)
            cmds.file(filePath + "/" + fileName, es=True , pr=False, force=True, typ="FBX export")
            cmds.select(cl=True)
            om.MGlobal.displayInfo("Exported Triangulated Meshes")
        else:
            cmds.warning("No export location selected. Or no file name chosen.")


    def HelpLink(self):
        cmds.launch(web="https://github.com/mdjustin/High-Low-Expo")
        
if __name__ == "__main__":

    
    try:
        open_import_dialog.close()
        open_import_dialog.deleteLater()
    except:
        pass        
        
    open_import_dialog = HighLowDialog()
    open_import_dialog.show()
