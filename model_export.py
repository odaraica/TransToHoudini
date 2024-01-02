# coding=UTF-8
import maya.cmds as mc



class TransRigModel:
    def __init__(self):
        self.sel = []
        self.breakAttrList = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ', 'scaleX', 'scaleY',
                         'scaleZ', 'visibility','tx','ty','tz','rx','ry','rz','sx','sy','sz','v','radi','translate','rotate','scale']
        self.constraintTypeList = ['parentConstraint','scaleConstraint','pointConstraint','poleVectorConstraint','orientConstraint']
        self.boneMap = {'Hips':'Root_M','Spine':'BackA_M','Spine1':'BackB_M','Spine2':'Chest_M','Neck':'Neck_M','Head':'Head_M',\
                        'LeftShoulder':'Scapula_L','LeftArm':'Shoulder_L','LeftForeArm':'Elbow_L','LeftHand':'Wrist_L',\
                        'RightShoulder':'Scapula_R','RightArm':'Shoulder_R','RightForeArm':'Elbow_R','RightHand':'Wrist_R',\
                        'LeftUpLeg':'Hip_L','LeftLeg':'Knee_L','LeftFoot':'Ankle_L','RightUpLeg':'Hip_R','RightLeg':'Knee_R',\
                        'RightFoot':'Ankle_R'}
        self.jointDict = {}
        self.groupDict = {}
        self.contraintDict = {}
        self.geoDict = {}
        self.newCharacter = ''
        self.stime = mc.playbackOptions(query=True, minTime=True)
        self.etime = mc.playbackOptions(query=True, maxTime=True)
        self.needBake = False
        self.BSexport = False
        self.debugMode = 1
        self.deleteOrg = False
        self.newJointGrp = ''
        self.newGeoGrp = ''
        self.newBSGrp = ''

    def setSel(self,selList):
        self.sel = selList

    def objectFilter(self):   #DeformationSystem    FaceDeformationSystem
        bodyJointList = []
        faceJointList = []
        bodyGrpList = []
        faceGrpList = []
        bodyConList = []
        faceConList = []
        self.groupDict['FaceDeformationSystem'] = ''
        self.groupDict['DeformationSystem'] = ''

        if len(self.sel) != 1:
            print('please choose only one Group of Charactor')
        else:
            tempTransnode = mc.listRelatives(self.sel[0], ad=True, fullPath=True, typ='transform')
            if tempTransnode:
                for node in tempTransnode:
                    tempShapeList = mc.listRelatives(node,fullPath = True,shapes=True)
                    if node.endswith('|DeformationSystem'):
                        self.groupDict['DeformationSystem'] = node
                        self.newJointGrp = node
                        tempBodyJointList =  mc.listRelatives(node, ad=True, fullPath=True, typ='joint')
                        if tempBodyJointList:
                            for j in tempBodyJointList:
                                if mc.nodeType(j) == 'joint':
                                    bodyJointList.append(j)
                    elif node.endswith('|FaceDeformationSystem'):
                        self.groupDict['FaceDeformationSystem'] = node
                        tempFaceJointList = mc.listRelatives(node, ad=True, fullPath=True)
                        if tempFaceJointList:
                            for j in tempFaceJointList:
                                if mc.nodeType(j) == 'joint':
                                    faceJointList.append(j)
                                elif mc.nodeType(j) == 'transform':
                                    try:
                                        tempShaList = mc.listRelatives(j,shapes = True)
                                        if not tempShaList:
                                             faceGrpList.append(j)
                                    except:
                                        pass
                                elif mc.nodeType(j) in self.constraintTypeList:
                                    faceConList.append(j)
                    # collection meshes     and  relative  BS++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    if tempShapeList:
                        if mc.nodeType(tempShapeList[0]) == 'mesh':
                            isVis = mc.getAttr(node +'.visibility')
                            if isVis:
                                if('FaceFit' not in node) and ('donghuajianchaceng' not in node) and ('maofa' not in node)\
                                        and ('MAOFA' not in node) and ('hair' not in node) and ('shave' not in node)\
                                    and('other' not in node)\
                                        and ('Xgen' not in node) and ('FaceDeformationSystem' not in node):
                                    self.geoDict[node] = []
                                    if self.BSexport:
                                        try:
                                            BSList = mc.blendShape(tempShapeList[0],q=True,t=True)
                                            self.geoDict[node] = BSList
                                        except:
                                            print('mesh:{0}  shape{1}  has no BS'.format(node,tempShapeList[0]))
                    else:
                        self.groupDict['FaceDeformationSystem'] = ''



                        # print(node)
                        # tempGeoList = mc.listRelatives(node, ad=True, fullPath=True, typ='transform')
                        # if tempGeoList:
                        #     for j in tempGeoList:
                        #         tempShapeList = mc.listRelatives(j,fullPath=True,shapes=True)
                        #         if tempShapeList:
                        #             if mc.nodeType(tempShapeList[0]) == 'mesh':
                        #                 isVis = mc.getAttr(j+'.visibility')
                        #                 if isVis:
                        #                     self.geoList.append(j)
            self.jointDict['FaceJoint'] = faceJointList
            self.jointDict['BodyJoint'] = bodyJointList
            self.groupDict['BodyGroup'] = bodyGrpList
            self.groupDict['FaceGroup'] = faceGrpList
            self.contraintDict['BodyContraint'] = bodyConList
            self.contraintDict['FaceContraint'] = faceConList


        if self.debugMode == 2:
            if self.groupDict['DeformationSystem']:
                print(self.groupDict['DeformationSystem'])
            else:
                print('')
            if self.groupDict['FaceDeformationSystem']:
                print(self.groupDict['FaceDeformationSystem'])
            print(len(self.jointDict['BodyJoint']))
            print(len(self.jointDict['FaceJoint']))
            print(len(self.groupDict['BodyGroup']))
            print(len(self.groupDict['FaceGroup']))
            print(len(self.contraintDict['BodyContraint']))
            print(len(self.contraintDict['FaceContraint']))
            print(len(self.geoDict.keys()))
        return 1

    def geoOp(self):
        pass

    def animJointPresentOp(self):
        '''bake Anime on joint,break connect with joint,delete contraint ,unparent DeformationSystem Group ,reparent face joint'''
        headBone = ''
        faceBone = ''
        if self.needBake:
            self.bakeAnim(self.jointDict['BodyJoint'])
            self.bakeAnim(self.jointDict['FaceJoint'])
        #delete contraint+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if self.contraintDict['BodyContraint']:
            for con in self.contraintDict['BodyContraint']:
                mc.delete(con)
        else:
            print('BodyContraint has no elements')
        if self.contraintDict['FaceContraint']:
            for con in self.contraintDict['FaceContraint']:
                mc.delete(con)
        else:
            print('FaceContraint has no elements')
        #break Connection between Joint and ControlCurve ++++++++++++++++++++++++++++++++
        for bone in self.jointDict['BodyJoint']:
            if bone.endswith('|Head_M') :
                headBone = bone
            try:
                self.disConnJoint(bone)
                mc.delete(bone,cn=True)
            except:
                print('BodyJoint:{0} clean fail'.format(bone))

        for bone in self.jointDict['FaceJoint']:
            if bone.endswith('|Face_M') or bone.endswith('|faceHeadJoint'):
                faceBone = bone
            try:
                self.disConnJoint(bone)
                mc.delete(bone,cn=True)
            except:
                print('FaceJoint:{0} clean fail'.format(bone))
        # if faceBone exsit     connnect the faceBone to headBone  ++++++++++++++++++++++++++++
        if faceBone:
            mc.parent(faceBone,headBone)
        # if faceBone not exsit  connect every TopBone to headBone ++++++++++++++++++++++++++++
        else:
            topBoneList = []
            tempBoneList = []
            for bone in self.jointDict['FaceJoint']:
                try:
                    self.findTopJoint(bone,tempBoneList)
                    if tempBoneList:
                        if tempBoneList[0] not in topBoneList:
                            topBoneList.append(tempBoneList[0])
                except:
                    print('currentBone:{0}  find it\'s  TopBone fail'.format(bone))
            if topBoneList:
                if self.debugMode == 6:
                    print('topBoneList is not empty,and topBone Count is {0}'.format(len(self.topBoneList)))

                for b in topBoneList:
                    mc.parent(b,headBone)


        mc.parent(self.groupDict['DeformationSystem'],world = True)
        # collection meshs    and BS    to new group
        self.newGeoGrp = mc.group(self.geoDict.keys(),name = 'geoGrp',world = True)
        self.newBSGrp = mc.group(em=True, name='BSGrp',world=True)
        for geo in self.geoDict.keys():
            if self.geoDict[geo]:
                mc.parent(self.geoDict[geo],self.newBSGrp)

        # # self.newGroup = mc.group(newGeoGroup,newJointGroup,name = self.sel[0]+'_new',w=True)
        if self.deleteOrg:
            mc.delete(self.sel[0])
            
        return 1



    def humanIKrebuild(self):
        boneSlot = []
        for bone in self.boneMap.keys():
            tempbone = self.boneMap[bone] + '_' + bone
            boneSlot.append(tempbone)
        self.newCharacter = mc.characterize(sk = boneSlot)

    def unlockObj(self,obj):
        lockAttr = mc.listAttr(obj, locked=True)
        if lockAttr:
            for j in lockAttr:
                longAttr = obj + '.' + j
                mc.setAttr(longAttr, lock=False)

    def delRelativeConst(self,obj):
        '''delete  relatives   contraint'''
        constList = mc.listRelatives(obj,fullPath=True,type = self.constraintTypeList)
        if constList:
            for i in constList:
                try:
                    mc.delete(i)
                except:
                    if self.debugMode:
                        print('delete child contraints  of  the joint:{0} fail'.format(obj))
                    pass
        if self.debugMode == 4:
            print('delete child contraint  of  joint:{0} Success'.format(obj))

    def unBindSkin(self,obj):
        shapeList = mc.listRelatives(obj, shapes=True, fullPath=True)
        if shapeList:
            for shape in shapeList:
                if shape.endswith('Orig'):
                    mc.delete(shape)
        conNodeList = mc.listConnections(shapeList[0], type='skinCluster')
        if conNodeList:
            for node in conNodeList:
                mc.delete(node)

    def bakeAnim(self,jointList):
        mc.bakeResults(jointList,simulation=True,time = (self.stime,self.etime))

    def disConnJoint(self,joint):
        tempConnList = mc.listConnections(joint, s=True, d=False, p=True, c=True)
        if tempConnList:
            for attrind in range(len(tempConnList) / 2):
                shortattr = self.nameCut(tempConnList[2 * attrind], 2)
                if shortattr in self.breakAttrList:
                    try:
                        mc.disconnectAttr(tempConnList[2 * attrind], tempConnList[2 * attrind + 1])
                    except:
                        mc.disconnectAttr(tempConnList[2 * attrind + 1], tempConnList[2 * attrind])
        if self.debugMode == 3:
            print('disconnect the joint:{0}'.format(joint))

    def findTopJoint(self,obj,topBone):

        paList = mc.listRelatives(obj,parent = True,type = 'joint')
        if paList:
            self.findTopJoint(paList[0],topBone)
        else:
            topBone.append(obj)

    def listBSnode(self,curNode):
        BSList = []
        try:
            tempShapeList = mc.listRelatives(curNode,shapes=True)
            if tempShapeList:
                if 'Orig' not in tempShapeList[0]:
                    BSList = mc.blendShape(tempShapeList[0],q=True,t=True)
        except:
            pass

        return BSList

    def nameCut(self,fullName, selInx):
        ind = fullName.rfind(':')
        indx = fullName.rfind('.')
        if ind == -1:
            ind = 0
        if indx == -1:
            indx = 0
        if selInx == 0:
            ind += 1
            return fullName[ind:]
        elif selInx == 1:
            return fullName[:ind]
        elif selInx == 2:
            return fullName[(indx + 1):]



