#coding=UTF-8
import maya.cmds as mc
import maya.OpenMaya as om
import pymel.core as pm
import nodeClass
import copy
import json



class GeoShaderNet:
    def __init__(self):
        self.savePath = 'F:\\work_project\\python_project\\trans_houdini\\shaderface.txt'
        self.shaderNetData = {}
        self.polyData = {}
        self.saveDic = {}
        self.nodeTypeList = {'lambert': nodeClass.LambertMat, 'blinn': nodeClass.BlinnMat,
                             'layeredShader': nodeClass.LShaderMat, 'phong': nodeClass.PhoneMat, \
                             'RedshiftMaterial': nodeClass.RsMat, 'RedshiftColorLayer': nodeClass.RsColorLayer, \
                             'RedshiftColorCorrection': nodeClass.RsColorCor, 'file': nodeClass.FileNode,
                             'place2dTexture': nodeClass.uv2dNode, 'remapHsv': nodeClass.remapHsvNode, \
                             'RedshiftNormalMap': nodeClass.normalMapNode, 'reverse': nodeClass.reverseNode, \
                             'RedshiftBumpBlender': nodeClass.bumpBlender, 'RedshiftBumpMap': nodeClass.bumpMapNode}
        self.allgeo = {}
        self.sel = []

    def curGrp(self,curSel):
        self.sel.append(curSel)

    def setSavePath(self, pathStr, fileName):
        self.savePath = pathStr + fileName

    def getGeoData(self):
        '''
        在使用transRigModel整理模型之后  再手动选中整理出的模型大组 执行这个命令收集shader信息
        '''
        # self.allgeo {多边形trans节点名：对应shape名}
        for i in self.sel:
            tempGeoList = mc.listRelatives(i, ad=True, fullPath=True, typ='transform')
            if tempGeoList:
                for j in tempGeoList:
                    tempShapeList = mc.listRelatives(j, shapes=True, fullPath=True)
                    if tempShapeList:
                        if mc.nodeType(tempShapeList[0]) == 'mesh':
                            self.allgeo[j] = tempShapeList[0]

    def getShaderData(self):

        tempShaderNodeList = []
        tempGeoShaderDic = {}
        GeoShaderDic = {}

        for geo in self.allgeo.keys():
            tempShaderDic = {}
            shaderDic = {}
            conObjList = mc.listConnections(self.allgeo[geo], d=True, s=False, t='shadingEngine')
            shdList = self.listRebuild(conObjList)
            for i in shdList:

                mat = mc.listConnections(i + '.surfaceShader', s=True, d=True)
                shaderPlugList = mc.listConnections(i + '.surfaceShader', s=True, d=True, p=True,
                                                    c=True)  # [u'rsMaterial1SG.surfaceShader', u'rsMaterial1.outColor']
                if shaderPlugList:
                    self.getNodeData(mat, tempShaderNodeList)  # 调用self.getNodeData方法递归获取i这个sg节点对应的节点树
                    #print('geo:{0}  sgListLen:{1}  curSgnode:{2} mat:{3}'.format(geo,len(shdList),i,mat))
                    tempNodeDic = {}
                    NodeDic = {}
                    nodeDataDic = {}
                    # 根据shaderNodeList内的node名字 建立对应的实例 tempNodeDic字典（node名字：类实例）通过调用nodeclass内的方法 获取数据 并存入tempNodeDic字典的对应位置 (node名字：类实例的数据字典)
                    # 然后存入tempShaderDic字典（sg节点名字：tempNodeDic字典）
                    shaderNodeList = copy.deepcopy(tempShaderNodeList)
                    shaderNodeDict = copy.deepcopy(shaderNodeList)
                    del tempShaderNodeList[:]
                    for ind in range(len(shaderNodeList)):
                        nodeTyp = mc.nodeType(shaderNodeList[ind])
                        shaderNodeDict[ind] = self.nodeTypeList[nodeTyp](shaderNodeList[ind])
                        tempNodeDic[shaderNodeList[ind]] = shaderNodeDict[ind]
                        NodeDic[shaderNodeList[ind]] = {}

                    tempShaderDic[i] = tempNodeDic
                    shaderDic[i] = NodeDic

            tempGeoShaderDic[geo] = tempShaderDic
            GeoShaderDic[geo] = shaderDic

        for geo in tempGeoShaderDic.keys():
            for sgnode in tempGeoShaderDic[geo].keys():

                for nodeName in tempGeoShaderDic[geo][sgnode].keys():
                    tempGeoShaderDic[geo][sgnode][nodeName].getData()
                    try:
                        tempGeoShaderDic[geo][sgnode][nodeName].getImData()
                        print('{0} pre import-----{1}'.format(nodeName,len(tempGeoShaderDic[geo][sgnode][nodeName].importData.keys())))
                        tempGeoShaderDic[geo][sgnode][nodeName].getExData()
                        print('{0} pre export-----{1}'.format(nodeName,len(tempGeoShaderDic[geo][sgnode][nodeName].exportData.keys())))
                        tempGeoShaderDic[geo][sgnode][nodeName].dataFilter()
                        if tempGeoShaderDic[geo][sgnode][nodeName].importData:
                            print(tempGeoShaderDic[geo][sgnode][nodeName].importData)
                        print('{0} post import-----{1}'.format(nodeName,len(tempGeoShaderDic[geo][sgnode][nodeName].importData.keys())))
                        print('{0} post export-----{1}'.format(nodeName,len(tempGeoShaderDic[geo][sgnode][nodeName].exportData.keys())))

                    except:
                        print('{}-{}-{} datafilter failure'.format(geo, sgnode, nodeName))
                    GeoShaderDic[geo][sgnode][nodeName]['attrData'] = tempGeoShaderDic[geo][sgnode][nodeName].attrDict
                    GeoShaderDic[geo][sgnode][nodeName]['importData'] = tempGeoShaderDic[geo][sgnode][
                        nodeName].importData
                    GeoShaderDic[geo][sgnode][nodeName]['exportData'] = tempGeoShaderDic[geo][sgnode][
                        nodeName].exportData

        self.shaderNetData = GeoShaderDic


    def getNodeData(self, checkData, saveList):
        nextNodeList = []
        if type(checkData) == list:
            for node in checkData:
                if mc.nodeType(node) in self.nodeTypeList.keys() and node not in saveList:
                    saveList.append(node)
                tempConNode = mc.listConnections(node, d=False, s=True)
                if tempConNode:
                    tempNodeList = self.listRebuild(tempConNode)
                    for i in tempNodeList:
                        if mc.nodeType(i) in self.nodeTypeList.keys():
                            nextNodeList.append(i)

            if nextNodeList:
                return self.getNodeData(nextNodeList, saveList)


    def getFaceShader(self):
        for geo in self.allgeo.keys():
            shape = self.allgeo[geo]
            newgeo = self.cutStrNam(geo)
            print(newgeo)
            faceShader = {}

            pmnode = pm.PyNode(shape)
            apinode = pmnode.__apimobject__()

            curMesh = om.MFnMesh(apinode)
            curShaders = om.MObjectArray()
            curFaceIds = om.MIntArray()
            curMesh.getConnectedShaders(0, curShaders, curFaceIds)
            if curShaders:
                for k in range(curShaders.length()):
                    matList = []
                    tempShader = om.MFnDependencyNode(curShaders[k])
                    tempMatList = mc.listConnections(tempShader.name(),c=True,s=True,p=True)
                    if tempMatList:
                        for ind in range(len(tempMatList)/2):
                            if '.surfaceShader' in tempMatList[ind*2]:
                                matList.append(tempMatList[ind*2+1][:-9])
                    faceShader[tempShader.name()] = copy.deepcopy(matList)
                    del matList[:]
            self.polyData[newgeo] = faceShader


    def listRebuild(self, oriList):
        '''
        oriList内部去重
        '''
        tempList = []
        tempList.append(oriList[0])
        for i in oriList:
            if (i in tempList):
                pass
            else:
                tempList.append(i)
        return tempList


    def setSavePath(self, path):
        self.savePath = path


    def cutStrNam(self, oldStr):
        ind = oldStr.rfind(':')
        if not ind == -1:
            newStr = oldStr.replace(':', '_')
            return newStr
        return oldStr


    def saveData(self):
        self.saveDic['shaderData'] = self.shaderNetData
        self.saveDic['polyData'] = self.polyData
        try:
            with open(self.savePath, 'w') as fout:
                json.dump(self.saveDic, fout)
                print('save complete')
            return 1
        except:
            print('数据写入出错')
            return 0


# a = GeoShaderNet()
# a.setSavePath('F:\\work_project\\python_project\\trans_houdini\\shaderface.txt')
# a.getGeoData()
# a.getShaderData()
# a.getFaceShader()
# a.saveData()