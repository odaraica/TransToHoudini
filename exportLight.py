#coding=UTF-8
import maya.cmds as mc
import json
import maya.mel as mel

class lightInfoExport:
    def __init__(self):
        self.attrList =  {'exposure0': '.exposure0', 'DomeMap': '.tex0', 'MapType': '.envType', 'lightType': '.lightType',
                    'Gamma': '.gamma0', 'color': '.color', 'intensity': '.intensity', 'exposure': '.exposure',
                    'decayType': '.decayType', 'shadow': '.shadow', 'affectsDiffuse': '.affectsDiffuse',
                    'affectsSpecular': '.affectsSpecular', 'saturation': '.saturation0','Hue':'.hue0',
                    'scale': '.scale', 'rotate': '.rotate','translate': '.translate',
                    'areaVisibleInRender': '.areaVisibleInRender', 'areaBidirectional': '.areaBidirectional',
                    'volumeRayContributionScale': '.volumeRayContributionScale', 'areaShape': '.areaShape',
                    'samples': '.samples', 'srgbToLinear0': '.srgbToLinear0',
                    'diffuseRayContributionScale': '.diffuseRayContributionScale',
                    'glossyRayContributionScale': '.glossyRayContributionScale',
                    'singleScatteringRayContributionScale': '.singleScatteringRayContributionScale',
                    'multipleScatteringRayContributionScale': '.multipleScatteringRayContributionScale',
                    'indirectRayContributionScale': '.indirectRayContributionScale',
                    'background_enable': '.background_enable'}
        self.lightDict = {}
        self.lightTyp = ['RedshiftPhysicalLight','RedshiftDomeLight']
        self.lightList = []
        self.savePath = ''
        self.lightList = []
        self.constList = []
        self.bakeList = []
    def setPath(self,path):
        self.savePath = path
    def lightFilter(self,selList):
        if selList:
            for i in selList:
                shapeL = mc.listRelatives(i,shapes=True)
                if shapeL:
                    if mc.nodeType(shapeL[0]) in self.lightTyp:
                        self.lightList.append(i)
                    else:
                        print('{0} is not correct light'.format(i))
                else:
                    print('{0} does not have shape node '.format(i))
        else:
            print('select nothing     please select lights')
        return self.lightList

    def saveData(self):
        try:
            dataPath = self.savePath + '.txt'
            with open(dataPath,'w') as fout:
                json.dump(self.lightDict,fout)
            return 1
        except:
            print('数据写入出错')
            return 0
    def saveFBX(self):
        try:
            filePath = self.savePath + '.fbx'
            mc.select(self.bakeList)
            mel.eval('FBXExportBakeComplexAnimation -q;')
            mel.eval('FBXExport -f "{}" -s ;'.format(filePath))
            return 1
        except:
            print("FBX save fail,please check")
            return 0
    def outputLightData(self):

        for i in self.bakeList:
            tempMiddleDict = {}
            shapes = mc.listRelatives(i,shapes=True)
            lightType = mc.nodeType(shapes[0])
            tempMiddleDict['Type'] = lightType
            # u'exposure0',u'tex0',u'envType',u'gamma0', u'tex1', u'gamma1',
            for attr in self.attrList.keys():
                try:
                    if attr == 'scale' or attr == 'rotate' or attr == 'translate':
                        tempattrvalue = mc.getAttr(i + self.attrList[attr])
                    else:
                        tempattrvalue = mc.getAttr(shapes[0]+self.attrList[attr])
                    tempMiddleDict[attr] = tempattrvalue
                except:
                    tempMiddleDict[attr] = 'dick'

            self.lightDict[i] = tempMiddleDict


    def bakeToWorld(self):
        for light in self.lightList:
            pa = mc.listRelatives(light, parent=True)
            if not pa:
                continue
            else:
                duplicated_lamps = mc.duplicate(light, name=light + '_bakedToWorld', rc=True, rr=True)
                children = mc.listRelatives(duplicated_lamps, c=True, pa=True)[1:]
                for child in children:
                    mc.delete(child)
                tobake = mc.parent(duplicated_lamps, w=True)
                self.bakeList.append(duplicated_lamps[0])
                tempPC = mc.parentConstraint(light, tobake, mo=False)
                tempSC = mc.scaleConstraint(light, tobake, mo=False)
                self.constList.append(tempPC)
                self.constList.append(tempSC)
        startframe = mc.playbackOptions(q=True, minTime=True)
        endframe = mc.playbackOptions(q=True, maxTime=True)
        for i in self.bakeList:
            mc.bakeResults(i, t=(startframe, endframe))
        for c in self.constList:
            mc.delete(c)




if __name__ ==  '__main__':
    ExL = lightInfoExport()
    ExL.setPath("")
    sel = mc.ls(selection=True)
    ExL.lightFilter(sel)
    ExL.bakeToWorld()
    ExL.outputLightData()
    ExL.saveData()
    ExL.saveFBX()
