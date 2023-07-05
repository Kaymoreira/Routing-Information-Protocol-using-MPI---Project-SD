import classes

def getTopology():
        nodeA = classes.Node(0, 'a')
        nodeB = classes.Node(1, 'b')
        nodeC = classes.Node(2, 'c')
        nodeD = classes.Node(3, 'd')
        nodeE = classes.Node(4, 'e')
        nodeF = classes.Node(5, 'f')
        nodeG = classes.Node(6, 'g')
        nodeH = classes.Node(7, 'h')
        nodeI = classes.Node(8, 'i')
        nodeJ = classes.Node(9, 'j')

        nodeA.set_neighbors([
            classes.Neighbor(nodeG, True),
            classes.Neighbor(nodeB, True)
        ])
        nodeB.set_neighbors([
            classes.Neighbor(nodeA),
            classes.Neighbor(nodeG, True)
        ])
        nodeG.set_neighbors([
            classes.Neighbor(nodeA),
            classes.Neighbor(nodeB),
            classes.Neighbor(nodeC, True),
            classes.Neighbor(nodeD, True),
            classes.Neighbor(nodeF, True),
            classes.Neighbor(nodeE, True),
            classes.Neighbor(nodeH, True)
        ])
        nodeF.set_neighbors([
            classes.Neighbor(nodeE, True),
            classes.Neighbor(nodeG)
        ])
        nodeC.set_neighbors([
            classes.Neighbor(nodeG),
            classes.Neighbor(nodeD, True)
        ])
        nodeE.set_neighbors([
            classes.Neighbor(nodeF),
            classes.Neighbor(nodeG),
            classes.Neighbor(nodeH),
            classes.Neighbor(nodeI, True)
        ])
        nodeH.set_neighbors([
            classes.Neighbor(nodeG),
            classes.Neighbor(nodeE, True),
            classes.Neighbor(nodeI, True),
            classes.Neighbor(nodeJ, True),
            classes.Neighbor(nodeD, True)
        ])
        nodeD.set_neighbors([
            classes.Neighbor(nodeC),
            classes.Neighbor(nodeG),
            classes.Neighbor(nodeH),
            classes.Neighbor(nodeJ, True)
        ])
        nodeJ.set_neighbors([
            classes.Neighbor(nodeD),
            classes.Neighbor(nodeH),
            classes.Neighbor(nodeI, True)
        ])
        nodeI.set_neighbors([
            classes.Neighbor(nodeE),
            classes.Neighbor(nodeH),
            classes.Neighbor(nodeJ)
        ])

        return [
            nodeA,
            nodeB,
            nodeC,
            nodeD,
            nodeE,
            nodeF,
            nodeG,
            nodeH,
            nodeJ,
            nodeI,
        ]

def fillInitialDistances(topology: list[classes.Node]):
    for node in topology:
        for neighbor in node.neighbors:
            node.distances = node.distances + [
                classes.Distance(neighbor.node, 1)
            ]

    return topology

def convertDistancesToString(distances: list[classes.Distance]):
    res = ""
    for distance in distances:
        dist = "$" + str(distance.node.id) + ',' + str(distance.distance) + "$"
        res = res + dist
    return res

def convertStringToDistances(distances: str, topology: list[classes.Node]):
    objectStarted = False
    variablePointer = 0
    currVariableValue = ''

    node = ""
    distance = ""

    res = []

    for char in distances:
        if(char == '$'):
            if(objectStarted):
                if(variablePointer == 0):
                    node += currVariableValue
                elif(variablePointer == 1):
                    distance += currVariableValue

                myNode = None
                for nodeTop in topology:
                    if(str(nodeTop.id) == node):
                        myNode = nodeTop
                        break
                        
                res.append(classes.Distance(myNode, int(distance)))

                objectStarted = False
                node = ""
                distance = ""
                variablePointer = 0
                currVariableValue = ''
            else: 
                objectStarted = True
            continue

        if(char == ','):
            if(variablePointer == 0):
                node += currVariableValue
            elif(variablePointer == 1):
                distance += currVariableValue

            variablePointer = variablePointer + 1
            currVariableValue = ''
            continue

        if(objectStarted): 
            currVariableValue += char


    return res


def sendDistancesToNeighbors(neighbors: list[classes.Neighbor], distances: list[classes.Distance], comm, directionReversed: bool):
    for neighbor in neighbors:
        condition = neighbor.pointed
        if(directionReversed):
            condition = not neighbor.pointed
            
        if(condition):
            comm.send(convertDistancesToString(distances), neighbor.node.id)