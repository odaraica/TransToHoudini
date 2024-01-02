# coding=UTF-8
import maya.cmds as mc
import copy
import rename_UDIM


class BaseNode(object):
    def __init__(self, nam):
        self.name = nam
        self.type = 'BaseNode'
        self.attrDict = {}
        self.importData = {}
        self.exportData = {}
        self.saveDict = {}

    def getData(self, ATDict=None):
        valList = 0.0
        if ATDict:
            self.attrDict = ATDict
        else:
            attrList = mc.listAttr(self.name, u=True, v=True, w=True)
            for attr in attrList:
                try:
                    valList = mc.getAttr(self.name + '.' + attr)
                    self.attrDict[attr] = valList
                except:
                    print("can not get float data from this attr")
            self.attrDict['type'] = self.type

    def getImData(self, importDict=None):

        if importDict:
            self.importData = importDict
        else:
            implugList = mc.listConnections(self.name, s=True, d=False, p=True, c=True)
            imNode = mc.listConnections(self.name, s=True, d=False)
            if imNode and implugList:
                for i in range(len(implugList) / 2):
                    ind = implugList[2 * i + 1].find('.')
                    if implugList[2 * i + 1][:ind] in imNode:
                        newimplugList = []
                        newimplugList.append(implugList[i * 2])
                        newimplugList.append(implugList[i * 2 + 1])
                        try:
                            self.importData[implugList[2 * i + 1][:ind]].append(implugList[i * 2])
                            self.importData[implugList[2 * i + 1][:ind]].append(implugList[i * 2 + 1])
                        except:
                            self.importData[implugList[2 * i + 1][:ind]] = newimplugList

    def getExData(self, exportDict=None):
        if exportDict:
            self.exportData = exportDict
        else:
            explugList = mc.listConnections(self.name, s=False, d=True, p=True, c=True)
            exNode = mc.listConnections(self.name, s=False, d=True)
            if exNode and explugList:
                for i in range(len(explugList) / 2):
                    ind = explugList[2 * i + 1].find('.')
                    if explugList[2 * i + 1][:ind] in exNode:
                        newexplugList = []
                        newexplugList.append(explugList[i * 2])
                        newexplugList.append(explugList[i * 2 + 1])
                        try:
                            self.exportData[explugList[2 * i + 1][:ind]].append(explugList[i * 2])
                            self.exportData[explugList[2 * i + 1][:ind]].append(explugList[i * 2 + 1])
                        except:
                            self.exportData[explugList[2 * i + 1][:ind]] = newexplugList


class LambertMat(BaseNode):
    def __init__(self, nam):
        super(LambertMat, self).__init__(nam)
        self.type = 'lambert'

    def getData(self, ATDict=None):
        super(LambertMat, self).getData(ATDict)

    def getImData(self, importDict=None):
        super(LambertMat, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(LambertMat, self).getExData(exportDict)

    def dataFilter(self):
        pass


class BlinnMat(BaseNode):
    def __init__(self, nam):
        super(BlinnMat, self).__init__(nam)
        self.type = 'blinn'

    def getData(self, ATDict=None):
        super(BlinnMat, self).getData(ATDict)

    def getImData(self, importDict=None):
        super(BlinnMat, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(BlinnMat, self).getExData(exportDict)

    def dataFilter(self):
        pass


class LShaderMat(BaseNode):
    def __init__(self, nam):
        super(LShaderMat, self).__init__(nam)
        self.type = 'layeredShader'

    def getData(self, ATDict=None):
        super(LShaderMat, self).getData(ATDict)

    def getImData(self, importDict=None):
        super(LShaderMat, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(LShaderMat, self).getExData(exportDict)

    def dataFilter(self):
        pass


class PhoneMat(BaseNode):
    def __init__(self, nam):
        super(PhoneMat, self).__init__(nam)
        self.type = 'phong'


class RsMat(BaseNode):
    def __init__(self, nam):
        super(RsMat, self).__init__(nam)
        self.type = 'RedshiftMaterial'

    def getData(self, ATDict=None):
        super(RsMat, self).getData(ATDict)
        # self.dataFilter()

    def getImData(self, importDict=None):
        super(RsMat, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(RsMat, self).getExData(exportDict)

    def dataFilter(self):

        unuseList = ['depth_override', 'refl_depth', 'refl_enablecutoff', 'refl_cutoff', 'skip_inside_refl', \
                     'refr_depth', 'refr_enablecutoff', 'refr_cutoff', 'combined_depth', 'diffuse_direct', \
                     'diffuse_indirect', 'refl_direct', 'refl_indirect', 'refl_isGlossiness', 'coat_direct', \
                     'coat_indirect', 'coat_isGlossiness', 'refr_isGlossiness', 'decoupleIORFromRoughness', \
                     'shadow_opacity', 'affects_alpha', 'block_volumes', 'energyCompMode', 'overallAffectsEmission', \
                     'refl_k3', 'opacity_colorR', 'opacity_colorG', 'opacity_colorB', 'emission_colorR',
                     'emission_colorG', \
                     'emission_colorB', 'refl_reflectivityR', 'refl_reflectivityG', 'refl_reflectivityB',
                     'diffuse_colorR', \
                     'diffuse_colorG', 'diffuse_colorB', 'refl_edge_tintR', 'refl_edge_tintG', 'refl_edge_tintB',
                     'refl_colorR', \
                     'refl_colorG', 'refl_colorB', 'refr_colorR', 'refr_colorG', 'refr_colorB', 'refl_ior3',
                     'bump_input', 'bump_inputR', \
                     'bump_inputG', 'bump_inputB', 'overall_colorR', 'overall_colorG', 'overall_colorB', 'uvSet',
                     'frozen', \
                     'caching', 'version', 'nodeState']
        for i in unuseList:
            if i in self.attrDict.keys():
                del self.attrDict[i]

        if self.attrDict['transl_weight'] == 0:
            for i in self.attrDict.keys():
                if 'transl_' in i:
                    del self.attrDict[i]
        if self.attrDict['refl_weight'] == 0:
            for i in self.attrDict.keys():
                if 'refl_' in i:
                    del self.attrDict[i]
        if self.attrDict['refr_weight'] == 0:
            for i in self.attrDict.keys():
                if 'refr_' in i:
                    del self.attrDict[i]
        if self.attrDict['ms_amount'] == 0:
            for i in self.attrDict.keys():
                if 'ms_' in i:
                    del self.attrDict[i]
        if self.attrDict['coat_weight'] == 0:
            for i in self.attrDict.keys():
                if 'coat_' in i:
                    del self.attrDict[i]
        if self.attrDict['ss_amount'] == 0:
            for i in self.attrDict.keys():
                if 'ss_' in i or 'refr_transmittance' in i:
                    del self.attrDict[i]
    # def listRebuild(self, oriList):
    #     '''
    #     oriList内部去重
    #     '''
    #     tempList = []
    #     lenth = len(oriList)/2
    #     for ind in range(lenth):
    #         if (oriList[ind*2] in tempList):
    #             pass
    #         else:
    #             tempList.append(oriList[ind*2])
    #             tempList.append(oriList[ind*2+1])
    #     return tempList


class RsColorLayer(BaseNode):
    def __init__(self, nam):
        super(RsColorLayer, self).__init__(nam)
        self.type = 'RedshiftColorLayer'

    def getData(self, ATDict=None):
        super(RsColorLayer, self).getData(ATDict)
        # self.dataFilter()

    def getImData(self, importDict=None):
        super(RsColorLayer, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(RsColorLayer, self).getExData(exportDict)

    def dataFilter(self):
        enumList = ['1', '2', '3', '4', '5', '6', '7']
        for i in enumList:
            lenable = 'layer' + i + '_enable'
            if self.attrDict[lenable] == False:
                for j in self.attrDict.keys():
                    if ('layer' + i) in j:
                        del self.attrDict[j]
        for i in self.attrDict.keys():
            if 'premult' in i:
                del self.attrDict[i]


class RsColorCor(BaseNode):
    # {u'hue': 0, u'saturation': 1.0, u'level': 1.0, u'contrast': 0.5, u'gamma': 1.0}
    def __init__(self, nam):
        super(RsColorCor, self).__init__(nam)
        self.type = 'RedshiftColorCorrection'

    def getData(self, ATDict=None):
        super(RsColorCor, self).getData(ATDict)
        # self.dataFilter()

    def getImData(self, importDict=None):
        super(RsColorCor, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(RsColorCor, self).getExData(exportDict)

    def dataFilter(self):
        usePlug = [self.name + '.input', self.name + '.outColor']
        tempimportDict = {}
        tempexportDict = {}
        for attr in self.attrDict.keys():
            if 'input' in attr:
                del self.attrDict[attr]
        if self.importData:
            for node in self.importData.keys():
                templist = []
                for ind in range(len(self.importData[node])):
                    if self.importData[node][ind] in usePlug:
                        templist.append(self.importData[node][ind])
                        templist.append(self.importData[node][ind + 1])
                        try:
                            tempimportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempimportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.importData = tempimportDict
        if self.exportData:
            for node in self.exportData.keys():
                templist = []
                for ind in range(len(self.exportData[node])):
                    if self.exportData[node][ind] in usePlug:
                        templist.append(self.exportData[node][ind])
                        templist.append(self.exportData[node][ind + 1])
                        try:
                            tempexportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempexportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.exportData = tempexportDict


class FileNode(BaseNode):
    def __init__(self, nam):
        super(FileNode, self).__init__(nam)
        self.type = 'file'

    def getData(self, ATDict=None):
        super(FileNode, self).getData(ATDict)
        # self.dataFilter()

    def getImData(self, importDict=None):
        super(FileNode, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(FileNode, self).getExData(exportDict)

    def dataFilter(self):
        useList = ['fileTextureName', 'uvTilingMode', 'exposure', 'defaultColorR', 'defaultColorG', 'defaultColorB',
                   'colorGainR', 'colorGainG', 'colorGainB',
                   'colorOffsetR', 'colorOffsetG', 'colorOffsetB', 'alphaGain', 'alphaOffset', 'alphaIsLuminance',
                   'invert', 'colorSpace', 'type']
        usePlug = [self.name + '.outAlpha', self.name + '.outColor', self.name + '.coverage', self.name + '.outColorR', \
                   self.name + '.outColorG', self.name + '.outColorB']
        tempimportDict = {}
        tempexportDict = {}
        for attr in self.attrDict.keys():
            if attr not in useList:
                del self.attrDict[attr]
            else:
                if attr == 'fileTextureName':

                    oldPath = self.attrDict[attr]
                    a = rename_UDIM.FileRename()
                    a.inputFilePath(oldPath)
                    a.genNewNam()
                    if a.copy_success:
                        self.attrDict[attr] = a.O_N_NamDict[oldPath]
                        print('newFilePath:{}'.format(a.O_N_NamDict[oldPath]))
                    else:
                        self.attrDict[attr] = oldPath
                        print('filePath keep:{}'.format(oldPath))

        if self.importData:
            for node in self.importData.keys():
                templist = []
                for ind in range(len(self.importData[node])):
                    if self.importData[node][ind] in usePlug:
                        templist.append(self.importData[node][ind])
                        templist.append(self.importData[node][ind + 1])
                        try:
                            tempimportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempimportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.importData = tempimportDict
        if self.exportData:
            for node in self.exportData.keys():
                templist = []
                for ind in range(len(self.exportData[node])):
                    if self.exportData[node][ind] in usePlug:
                        templist.append(self.exportData[node][ind])
                        templist.append(self.exportData[node][ind + 1])
                        try:
                            tempexportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempexportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.exportData = tempexportDict


class uv2dNode(BaseNode):
    def __init__(self, nam):
        super(uv2dNode, self).__init__(nam)
        self.type = 'place2dTexture'

    def getData(self, ATDict=None):
        super(uv2dNode, self).getData(ATDict)
        # self.dataFilter()

    def getImData(self, importDict=None):
        super(uv2dNode, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(uv2dNode, self).getExData(exportDict)

    def dataFilter(self):
        attrList = ['repeatU', 'repeatV', 'offsetU', 'offsetV', 'rotateUV', 'mirrorU', 'mirrorV', 'type']
        usePlug = [self.name + '.coverage']
        tempimportDict = {}
        tempexportDict = {}
        for attr in self.attrDict.keys():
            if attr not in attrList:
                del self.attrDict[attr]
        if self.importData:
            for node in self.importData.keys():
                templist = []
                for ind in range(len(self.importData[node])):
                    if self.importData[node][ind] in usePlug:
                        templist.append(self.importData[node][ind])
                        templist.append(self.importData[node][ind + 1])
                        try:
                            tempimportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempimportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.importData = tempimportDict
        if self.exportData:
            for node in self.exportData.keys():
                templist = []
                for ind in range(len(self.exportData[node])):
                    if self.exportData[node][ind] in usePlug:
                        templist.append(self.exportData[node][ind])
                        templist.append(self.exportData[node][ind + 1])
                        try:
                            tempexportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempexportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.exportData = tempexportDict


class normalMapNode(BaseNode):
    def __init__(self, nam):
        super(normalMapNode, self).__init__(nam)
        self.type = 'RedshiftNormalMap'

    def getData(self, ATDict=None):
        super(normalMapNode, self).getData(ATDict)

    def getImData(self, importDict=None):
        super(normalMapNode, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(normalMapNode, self).getExData(exportDict)

    def dataFilter(self):
        attrList = ['rsNormalMap10.scale', 'repeats0', 'repeats1', 'min_uv0', 'min_uv1', 'max_uv0', 'max_uv1', 'type',
                    'tex0']
        usePlug = [self.name + '.outDisplacementVector']
        tempimportDict = {}
        tempexportDict = {}
        for attr in self.attrDict.keys():
            if attr not in attrList:
                del self.attrDict[attr]
        if self.importData:
            for node in self.importData.keys():
                templist = []
                for ind in range(len(self.importData[node])):
                    if self.importData[node][ind] in usePlug:
                        templist.append(self.importData[node][ind])
                        templist.append(self.importData[node][ind + 1])
                        try:
                            tempimportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempimportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.importData = tempimportDict
        if self.exportData:
            for node in self.exportData.keys():
                templist = []
                for ind in range(len(self.exportData[node])):
                    if self.exportData[node][ind] in usePlug:
                        templist.append(self.exportData[node][ind])
                        templist.append(self.exportData[node][ind + 1])
                        try:
                            tempexportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempexportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.exportData = tempexportDict


class remapHsvNode(BaseNode):
    def __init__(self, nam):
        super(remapHsvNode, self).__init__(nam)
        self.type = 'remapHsv'

    def getData(self, ATDict=None):
        super(remapHsvNode, self).getData(ATDict)

    def getImData(self, importDict=None):
        super(remapHsvNode, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(remapHsvNode, self).getExData(exportDict)

    def dataFilter(self):
        usePlug = [self.name + '.outColor', self.name + '.colorR', self.name + '.colorG', self.name + '.colorB',
                   self.name + '.outColorR', \
                   self.name + '.outColorG', self.name + '.outColorB']
        tempimportDict = {}
        tempexportDict = {}
        if self.importData:
            for node in self.importData.keys():
                templist = []
                for ind in range(len(self.importData[node])):
                    if self.importData[node][ind] in usePlug:
                        templist.append(self.importData[node][ind])
                        templist.append(self.importData[node][ind + 1])
                        try:
                            tempimportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempimportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]

            self.importData = tempimportDict
        if self.exportData:
            for node in self.exportData.keys():
                templist = []
                for ind in range(len(self.exportData[node])):
                    if self.exportData[node][ind] in usePlug:
                        templist.append(self.exportData[node][ind])
                        templist.append(self.exportData[node][ind + 1])
                        try:
                            tempexportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempexportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.exportData = tempexportDict


class reverseNode(BaseNode):
    def __init__(self, nam):
        super(reverseNode, self).__init__(nam)
        self.type = 'reverse'

    def getData(self, ATDict=None):
        super(reverseNode, self).getData(ATDict)

    def getImData(self, importDict=None):
        super(reverseNode, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(reverseNode, self).getExData(exportDict)

    def dataFilter(self):
        pass


class bumpBlender(BaseNode):
    def __init__(self, nam):
        super(bumpBlender, self).__init__(nam)
        self.type = 'RedshiftBumpBlender'

    def getData(self, ATDict=None):
        super(bumpBlender, self).getData(ATDict)

    def getImData(self, importDict=None):
        super(bumpBlender, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(bumpBlender, self).getExData(exportDict)

    def dataFilter(self):
        attrList = ['bumpWeight0', 'bumpWeight1', 'bumpWeight2', 'type']
        usePlug = [self.name + '.outColor']
        tempimportDict = {}
        tempexportDict = {}
        for attr in self.attrDict.keys():
            if attr not in attrList:
                del self.attrDict[attr]
        if self.importData:
            for node in self.importData.keys():
                templist = []
                for ind in range(len(self.importData[node])):
                    if self.importData[node][ind] in usePlug:
                        templist.append(self.importData[node][ind])
                        templist.append(self.importData[node][ind + 1])
                        try:
                            tempimportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempimportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.importData = tempimportDict
        if self.exportData:
            for node in self.exportData.keys():
                templist = []
                for ind in range(len(self.exportData[node])):
                    if self.exportData[node][ind] in usePlug:
                        templist.append(self.exportData[node][ind])
                        templist.append(self.exportData[node][ind + 1])
                        try:
                            tempexportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempexportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.exportData = tempexportDict


class bumpMapNode(BaseNode):
    def __init__(self, nam):
        super(bumpMapNode, self).__init__(nam)
        self.type = 'RedshiftBumpMap'

    def getData(self, ATDict=None):
        super(bumpMapNode, self).getData(ATDict)

    def getImData(self, importDict=None):
        super(bumpMapNode, self).getImData(importDict)

    def getExData(self, exportDict=None):
        super(bumpMapNode, self).getExData(exportDict)

    def dataFilter(self):
        attrList = ['scale', 'oldrange_min', 'oldrange_max', 'newrange_min', 'newrange_max', 'type']
        usePlug = [self.name + '.input', self.name + '.out']
        tempimportDict = {}
        tempexportDict = {}
        for attr in self.attrDict.keys():
            if attr not in attrList:
                del self.attrDict[attr]
        if self.importData:
            for node in self.importData.keys():
                templist = []
                for ind in range(len(self.importData[node])):
                    if self.importData[node][ind] in usePlug:
                        templist.append(self.importData[node][ind])
                        templist.append(self.importData[node][ind + 1])
                        try:
                            tempimportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempimportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.importData = tempimportDict
        if self.exportData:
            for node in self.exportData.keys():
                templist = []
                for ind in range(len(self.exportData[node])):
                    if self.exportData[node][ind] in usePlug:
                        templist.append(self.exportData[node][ind])
                        templist.append(self.exportData[node][ind + 1])
                        try:
                            tempexportDict[node].extend(copy.deepcopy(templist))
                        except:
                            tempexportDict[node] = copy.deepcopy(templist)
                    else:
                        del templist[:]
            self.exportData = tempexportDict