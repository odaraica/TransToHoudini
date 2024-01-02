
import json
import hou


def getData(path):
    dict = {}
    try:
        with open(path, 'r') as fin:
            dict = json.load(fin)
    except:
        print('read json error')
    return dict


def quchong(oldList):
    '''
    oldList qu chong
    '''
    tempList = []
    for i in oldList:
        if i:
            if i in tempList:
                pass
            else:
                tempList.append(i)
    return tempList


def nameFilter(oriList, getStrList):
    newList = []
    for i in oriList:
        for j in getStrList:
            if i.endswith(j):
                newList.append(i)
            else:
                pass
    return newList


def stringRebuild(oriStr, indx):
    if indx == 0:
        ind = oriStr.rfind('.')
        if ind == -1:
            ind = 0
        ind += 1
        return oriStr[ind:]
    elif indx == 1:
        ind = oriStr.rfind('|')
        if ind == -1:
            ind = 0
        ind += 1
        return oriStr[ind:]
    elif indx == 3:
        ind = oriStr.rfind('/')
        if ind == -1:
            ind = 0
        ind += 1
        return oriStr[ind:]
    elif indx == 2:
        oriStr = oriStr.replace('|', '_')
        oriStr = oriStr.replace('/', '_')
        oriStr = oriStr.replace(':', '_')
        return oriStr


def listStringRebuild(oriStrList, indx):
    if indx == 0:
        newStrList = []
        for i in oriStrList:
            newStr = stringRebuild(i, 0)
            newStrList.append(newStr)
        return newStrList
    elif indx == 1:
        newStrList = []
        for i in oriStrList:
            newStr = stringRebuild(i, 1)
            newStrList.append(newStr)
        return newStrList


def main():
    node = hou.pwd()
    geo = node.geometry()

    oldPrimGrpList = geo.primGroups()
    jsonPath = node.parm("jsonPath").evalAsString()
    jsonData = getData(jsonPath)
    polyData = jsonData['polyData']
    if node.inputs()[0].type().name() == 'agentunpack':
        try:
            tempNameList = geo.primStringAttribValues('agentshapename')
            if tempNameList:
                tempagentNameList = nameFilter(quchong(tempNameList), listStringRebuild(polyData.keys(), 1))
                agentNameList = listStringRebuild(tempagentNameList, 0)
                primGrpDict = {}
                for i in agentNameList:
                    try:
                        primGrpDict[i] = geo.createPrimGroup(i)
                    except:
                        pass

                for primId in range(len(tempNameList)):
                    if stringRebuild(tempNameList[primId], 0) in agentNameList:
                        primGrpDict[stringRebuild(tempNameList[primId], 0)].add(geo.iterPrims()[primId])

                for i in oldPrimGrpList:
                    i.destroy()
        except:
            print('node {0} do not have prim agentshapename'.format(node.name()))

    elif node.inputs()[0].type().name() == 'file':
        try:
            tempPolyNam = geo.primStringAttribValues('name')
            if tempPolyNam:
                tempPolyNamList = nameFilter(quchong(tempPolyNam), listStringRebuild(polyData.keys(), 1))
                primGrpDict = {}
                for i in tempPolyNamList:
                    i = stringRebuild(i, 2)
                    try:
                        primGrpDict[i] = geo.createPrimGroup(i)

                    except:
                        print('primGroup {0} create fail'.format(i))
                for primId in range(len(tempPolyNam)):
                    if tempPolyNam[primId] in tempPolyNamList:
                        primGrpDict[stringRebuild(tempPolyNam[primId], 2)].add(geo.iterPrims()[primId])
        except:
            print('node {0} do not have prim name'.format(node.name()))
    elif node.inputs()[0].type().name() == 'blast':
        try:
            primMatDict = {}
            shopMatList = geo.primStringAttribValues('shop_materialpath')
            # if '/' in shopMatList[0] or 'JS' in shopMatList[0]:
            matSgDict = {}
            matNamList = []
            for nam in polyData.keys():
                if nam.endswith(oldPrimGrpList[0].name()):
                    matNamList.append(nam)
                    for sg in polyData[nam].keys():
                        newSGNam = stringRebuild(sg, 2)
                        if len(polyData[nam][sg]) == 1:
                            matSgDict[newSGNam] = polyData[nam][sg][0]  # matSgDict  key:newSGNam   value:matNam

                        else:
                            print('geo:{0} sg:{1} MaterialArray has not only single element'.format(nam, sg))

            if len(matNamList) != 1:
                print('There are {0} SGNodeNam endswith same name of primGroups,please check the {1} Node'.format(
                    len(matNamList), node.name()))
            else:
                matDict = polyData[matNamList[0]]
                primGrpDict = {}
                for SGNam in matDict.keys():
                    newSGNam = stringRebuild(SGNam, 2)
                    try:
                        primGrpDict[newSGNam] = geo.createPrimGroup(
                            newSGNam)  # primGrpDict  key:newSGNam value:houdiniGrp
                    except:
                        print('primGroup {0} create fail'.format(newSGNam))

                for primId in range(len(shopMatList)):  # primMatDict   key:matNam   value:primIdGroup
                    if shopMatList[primId] not in primMatDict.keys():
                        primMatDict[shopMatList[primId]] = []
                        primMatDict[shopMatList[primId]].append(primId)
                    elif shopMatList[primId] in primMatDict.keys():
                        primMatDict[shopMatList[primId]].append(primId)

                for newSGNam in primGrpDict.keys():
                    matNam = stringRebuild(matSgDict[newSGNam], 2)
                    for key in primMatDict.keys():

                        if matNam in key:
                            for primId in primMatDict[key]:
                                primGrpDict[newSGNam].add(geo.iterPrims()[primId])

            for i in oldPrimGrpList:
                i.destroy()

        except:
            print('SGNam primGroup create fail on Node : {0}'.format(node))


main()
