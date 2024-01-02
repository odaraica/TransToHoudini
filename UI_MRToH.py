#coding=UTF-8

import model_export
import exportShaderData
import exportLight

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import maya.cmds as mc



class MyWin(QWidget):

    def __init__(self):
        super(MyWin,self).__init__()
        self.selGrp = []
        self.DM = 1
        self.setWindowTitle('MayaToHoudini')
        self.resize(400,800)
        self.check_parm = {}
        self.savePath = ''
        self.saveNam = ''
        self.lightSavePath = ''
        self.lightSaveNam = ''
        self.lightList = []

        self.groupBox1 = QGroupBox(u'整理导出模型材质')
        self.groupBox1.setFixedSize(380,600)
        self.groupBox2 = QGroupBox(u'整理导出灯光')
        self.groupBox2.resize(380,150)
        self.button_selModel = QPushButton(u'选择角色大纲组')
        self.modelGrpNam = QLabel(self)
        self.modelGrpNam.setText(u'当前未选择任何组')
        self.modelGrpNam.setAlignment(Qt.AlignLeft)
        self.modelGrpNam.setFixedSize(120,20)
        # self.modelGrpNam.setScaledContents(False)
        self.chBox_bakeAnim = QCheckBox(u'烘焙动画')
        self.chBox_delOri = QCheckBox(u'整理完删除原组')
        self.chBox_exBS = QCheckBox(u'导出BS')
        self.chBox_exShader = QCheckBox(u'导出材质')
        self.button_selExPath = QPushButton(u'选择导出路径和名称')
        self.button_expShader = QPushButton(u'只导出材质')
        self.button_expModel = QPushButton(u'整理并导出')

        self.button_selLight = QPushButton(u'选择灯光')
        self.button_exLight = QPushButton(u'导出灯光信息')
        self.list_lights = QListWidget(self)
        self.list_lights.setSelectionMode(QAbstractItemView.MultiSelection)
        self.button_Ladd = QPushButton(u'+')
        self.button_Lrem = QPushButton(u'-')


        self.main_layout = QVBoxLayout()
        self.selExFile = QHBoxLayout()
        self.up_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.light_layout = QHBoxLayout()
        self.lightLeft_layout = QVBoxLayout()
        self.lightRight_layout = QVBoxLayout()
        self.lightBut_layout = QHBoxLayout()
        self.lightBut_layout.addWidget(self.button_Ladd)
        self.lightBut_layout.addWidget(self.button_Lrem)
        self.lightRight_layout.addWidget(self.list_lights)
        self.lightLeft_layout.addWidget(self.button_selLight)
        self.lightLeft_layout.addWidget(self.button_exLight)
        self.lightRight_layout.addLayout(self.lightBut_layout)
        self.light_layout.addLayout(self.lightLeft_layout)
        self.light_layout.addLayout(self.lightRight_layout)


        self.up_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.up_layout.addWidget(self.button_selModel)
        self.up_layout.addWidget(self.modelGrpNam)
        self.up_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.up_layout.addWidget(self.chBox_bakeAnim)
        self.up_layout.addWidget(self.chBox_delOri)
        self.up_layout.addWidget(self.chBox_exBS)
        self.up_layout.addWidget(self.chBox_exShader)
        self.up_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Maximum))
        self.up_layout.addWidget(self.button_selExPath)
        self.up_layout.addWidget(self.button_expShader)
        self.up_layout.addWidget(self.button_expModel)
        self.up_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Maximum))

        self.groupBox1.setLayout(self.up_layout)
        self.groupBox2.setLayout(self.light_layout)
        self.main_layout.addWidget(self.groupBox1)
        self.main_layout.addWidget(self.groupBox2)




        self.button_selModel.clicked.connect(self.selModelGrp)
        self.button_selExPath.clicked.connect(self.selPath)
        self.button_expShader.clicked.connect(self.export_shader)
        self.button_expModel.clicked.connect(self.export_MS)
        self.button_selLight.clicked.connect(self.lightListAddMul)
        self.button_Ladd.clicked.connect(self.lightListAddNew)
        self.button_Lrem.clicked.connect(self.lightListPop)
        self.button_exLight.clicked.connect(self.lightEx)

    def selModelGrp(self):
        self.selGrp = mc.ls(selection=True,ap=True)
        if self.selGrp:
            if len(self.selGrp) != 1:
                QMessageBox.information(self, u'错误', u'请选择一个角色大纲组 勿多选', QMessageBox.Yes, QMessageBox.Yes)
            else:
                self.modelGrpNam.setText(u'选择组：{0}'.format(self.selGrp[0]))
        else:
            QMessageBox.information(self, u'错误', u'请选择一个角色大纲组', QMessageBox.Yes, QMessageBox.Yes)

    def checkParm(self):
        self.check_parm['bakeAnim'] = self.chBox_bakeAnim.checkState()
        self.check_parm['delOrigin'] = self.chBox_delOri.checkState()
        self.check_parm['exportBS'] = self.chBox_exBS.checkState()
        self.check_parm['exportShader'] = self.chBox_exShader.checkState()


    def selPath(self):
        try:
            filespath = QFileDialog.getSaveFileName(self,u'选择保存路径 同时请填入保存文件的名称',"/",'txt(*.txt)')
            #G:/test/testsave.txt
        except:
            QMessageBox.information(self, u'错误', u'FileSaveDialog open  failed', QMessageBox.Yes, QMessageBox.Yes)
        if filespath:
            index = filespath[0].rfind('/')
            self.savePath = filespath[0][:index+1]
            self.saveNam = filespath[0][index+1:-4]
        else:
            QMessageBox.information(self, u'错误', u'未能读取到保存文件路径  请检查', QMessageBox.Yes, QMessageBox.Yes)



    def export_shader(self):
        if self.savePath and self.saveNam:
            a = exportShaderData.GeoShaderNet()
            a.setSel(self.selGrp)
            a.setSavePath(self.savePath + self.saveNam + '.txt')
            a.getGeoData()
            a.getShaderData()
            a.getFaceShader()
            sig = a.saveData()
            if sig:
                QMessageBox.information(self, u'成功', u'材质导出成功', QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.information(self, u'失败', u'材质导出失败', QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.information(self, u'错误', u'未能获取到正确的 保存路径和文件名  请重新选择输入', QMessageBox.Yes, QMessageBox.Yes)


    def export_MS(self):
        if self.savePath and self.saveNam:
            print(11111111111)
            self.checkParm()
            T = model_export.TransRigModel()
            T.setSel(self.selGrp)
            T.debugMode = self.DM
            T.needBake = self.check_parm['bakeAnim']
            T.BSexport = self.check_parm['exportBS']
            T.deleteOrg = self.check_parm['delOrigin']
            #a.debugMode = 0
            sig1 = T.objectFilter()
            sig2 = T.animJointPresentOp()



            #output shader ++++++++++++++++++++++++++++++++++++++++++
            G = exportShaderData.GeoShaderNet()
            G.curGrp(T.newGeoGrp)
            G.setSavePath(self.savePath + self.saveNam + '.txt')
            G.getGeoData()
            G.getShaderData()
            G.getFaceShader()
            sig = G.saveData()
            if sig:
                QMessageBox.information(self, u'成功', u'材质导出成功', QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.information(self, u'失败', u'材质导出失败', QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.information(self, u'错误', u'未能获取到正确的 保存路径和文件名  请重新选择输入', QMessageBox.Yes, QMessageBox.Yes)

    def lightListShow(self):
        #refresh list
        self.list_lights.clear()
        self.list_lights.addItems(self.lightList)

    def lightListAddMul(self):
        L = exportLight.lightInfoExport()
        # first add multi lights
        sel = mc.ls(selection=True,ap=True)
        self.lightList = L.lightFilter(sel)
        self.lightListShow()

    def lightListAddNew(self):
        L = exportLight.lightInfoExport()
        #add some lights
        sel = mc.ls(selection=True,ap=True)
        tempLightList = L.lightFilter(sel)
        for i in tempLightList:
            if i not in self.lightList:
                self.lightList.append(i)
        self.lightListShow()

    def lightListPop(self):
        L = exportLight.lightInfoExport()
        #delete some lights
        tempDelList = self.list_lights.selectedItems()
        if tempDelList:
            for i in tempDelList:
                self.lightList.remove(i.text())
        else:
            QMessageBox.information(self, u'错误', u'请在灯光列表里选择需要去除的灯', QMessageBox.Yes, QMessageBox.Yes)

        self.lightListShow()
    def lightEx(self):
        try:
            filespath = QFileDialog.getSaveFileName(self,u'选择保存路径 同时请填入保存文件的名称',"/",'txt(*.txt)')
            #G:/test/testsave.txt
        except:
            QMessageBox.information(self, u'错误', u'FileSaveDialog open  failed', QMessageBox.Yes, QMessageBox.Yes)
        if filespath:
            self.lightSavePath = filespath[0][:-4]
        else:
            QMessageBox.information(self, u'错误', u'未能读取到保存文件路径  请检查', QMessageBox.Yes, QMessageBox.Yes)

        L = exportLight.lightInfoExport()
        L.setPath(self.lightSavePath)
        L.lightFilter(self.lightList)
        L.bakeToWorld()
        L.outputLightData()
        sig = L.saveData()
        sig1 = L.saveFBX()
        if sig and sig1:
            QMessageBox.information(self, u'成功', u'灯光信息导出成功', QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.information(self, u'失败', u'灯光信息导出失败', QMessageBox.Yes, QMessageBox.Yes)


