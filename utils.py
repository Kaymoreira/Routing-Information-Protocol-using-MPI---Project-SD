import classes

def getTopology():
    """
    Retorna uma topologia de rede pré-definida.

    Returns:
        list[Node]: A topologia de rede.
    """
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

    # Definindo os vizinhos para cada nó
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
    """
    Preenche as distâncias iniciais dos nós com base nos vizinhos.

    Args:
        topology (list[Node]): A topologia de rede.

    Returns:
        list[Node]: A topologia de rede com as distâncias preenchidas.
    """
    for node in topology:
        for neighbor in node.neighbors:
            node.distances = node.distances + [
                classes.Distance(neighbor.node, 1)
            ]

    return topology

def convertDistancesToString(distances: list[classes.Distance]):
    """
    Converte uma lista de distâncias em uma string.

    Args:
        distances(descances: list[classes.Distance]): A lista de distâncias a ser convertida.

    Returns:
        str: A string contendo as distâncias convertidas.
    """
    res = ""
    for distance in distances:
        dist = "$" + str(distance.node.id) + ',' + str(distance.distance) + "$"
        res = res + dist
    return res

# A função convertStringToDistances recebe dois argumentos: 
# distances, uma string contendo as distâncias a serem convertidas, 
# e topology, uma lista de objetos Node que representa a topologia da rede. 
# Ela retorna uma lista de objetos Distance, representando as distâncias convertidas.
def convertStringToDistances(distances: str, topology: list[classes.Node]):
    """
    Converte uma string em uma lista de distâncias.

    Args:
        distances (str): A string contendo as distâncias.
        topology (list[Node]): A topologia de rede.

    Returns:
        list[Distance]: A lista de distâncias convertidas.
    """
    # objectStarted é uma flag que indica se o início de um objeto de distância foi encontrado. 
    # variablePointer é um contador usado para acompanhar qual variável está sendo preenchida (nó ou distância). 
    # currVariableValue é uma variável temporária para armazenar o valor atual sendo construído.
    objectStarted = False
    variablePointer = 0
    currVariableValue = ''

    # node e distance são variáveis usadas para armazenar os valores do nó e da distância atualmente sendo extraídos da string.
    node = ""
    distance = ""

    # res é uma lista vazia que armazenará as distâncias convertidas.
    res = []

    # Aqui está o processo de conversão propriamente dito. 
    # Percorremos cada caractere da string distances usando um loop for.
    for char in distances:
        # Se encontramos um caractere $, significa que estamos iniciando ou encerrando um objeto de distância.
        if(char == '$'):
            # Se objectStarted for True, isso indica que encontramos o final de um objeto de distância. 
            # Nesse caso, armazenamos os valores do nó e da distância extraídos nas variáveis correspondentes.
            if(objectStarted):
                # Em seguida, procuramos o objeto Node correspondente na topology usando o ID do nó extraído da string (node)
                if(variablePointer == 0):
                    node += currVariableValue
                # Quando encontramos o nó correspondente, criamos uma instância da classe Distance com o nó e a distância convertida (convertida para inteiro usando int(distance)
                elif(variablePointer == 1):
                    distance += currVariableValue

                myNode = None
                for nodeTop in topology:
                    if(str(nodeTop.id) == node):
                        myNode = nodeTop
                        break
                        
                res.append(classes.Distance(myNode, int(distance)))

                # einiciamos as variáveis relacionadas ao objeto de distância (objectStarted, node, distance, variablePointer, currVariableValue) para preparar a próxima iteração.
                objectStarted = False
                node = ""
                distance = ""
                variablePointer = 0
                currVariableValue = ''
            else: 
                objectStarted = True
            continue
        
        # Se encontramos uma vírgula (,) e objectStarted for True, isso indica que estamos lendo a distância atual. 
        # Dependendo do valor de variablePointer, adicionamos o valor atual à variável node ou distance.
        if(char == ','):
            if(variablePointer == 0):
                node += currVariableValue
            elif(variablePointer == 1):
                distance += currVariableValue

            variablePointer = variablePointer + 1
            currVariableValue = ''
            continue
        
        # No final, verificamos se objectStarted é True, o que significa que chegamos ao final da string, 
        # mas não encontramos o caractere $ de fechamento para o último objeto de distância.
        # Nesse caso, o último valor construído em currVariableValue seria perdido. 
        # Portanto, adicionamos o valor final à variável correspondente (node ou distance)
        if(objectStarted): 
            currVariableValue += char

    # Retornamos a lista res, que contém as distâncias convertidas
    return res

def sendDistancesToNeighbors(neighbors: list[classes.Neighbor], distances: list[classes.Distance], comm):
    """
    Envia as distâncias para os vizinhos.

    Args:
        neighbors (list[Neighbor]): A lista de vizinhos.
        distances (list[Distance]): A lista de distâncias.
        comm: O objeto de comunicação MPI.
    """
    # Aqui, percorremos cada vizinho na lista neighbors. 
    # Para cada vizinho, verificamos se o atributo pointed do vizinho é True, 
    # indicando que o vizinho deve receber as distâncias.
    # Dentro do bloco condicional, usamos o objeto de comunicação MPI comm para enviar as distâncias para o vizinho específico. 
    # Chamamos a função send() do objeto comm e passamos os seguintes argumentos: 
    # obj, que é o objeto a ser enviado (nesse caso, as distâncias convertidas em uma string usando convertDistancesToString(distances)), 
    # e dest, que é o ID do nó vizinho (neighbor.node.id).
    for neighbor in neighbors:
        if(neighbor.pointed):
            comm.send(obj=convertDistancesToString(distances), dest=neighbor.node.id)

# A função getCurrentNode recebe dois argumentos: 
# topology, uma lista de objetos Node que representa a topologia da rede, 
# e rank, um número inteiro que representa o rank do nó atual. 
# Ela retorna o nó atual com base no rank.
def getCurrentNode(topology: list[classes.Node], rank: int):
    """
    Obtém o nó atual com base no rank.

    Args:
        topology (list[Node]): A topologia de rede.
        rank (int): O rank do nó atual.

    Returns:
        Node: O nó atual.
    """
    # Inicializamos a variável res com o valor None. 
    # Essa variável será usada para armazenar o nó atual.
    # Aqui, percorremos cada nó na lista topology. 
    # Para cada nó, verificamos se o ID do nó (node.id) é igual ao rank fornecido. 
    # Se encontrarmos um nó com o ID correspondente ao rank, atribuímos esse nó à variável res.
    res = None
    for node in topology:
        if(node.id == rank):
            res = node

    return res
