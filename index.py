import utils
import classes
from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD   # obtém o objeto comunicador MPI
size = comm.size        # número total de processos
rank = comm.rank        # classificação deste processo
status = MPI.Status()   # obtém o objeto de status MPI

# Obtendo a topologia de rede
# Chamamos a função getTopology() do módulo utils para obter a topologia de rede. Essa função retorna uma lista de objetos Node, representando os nós da rede.
topology = utils.getTopology()


# Preenchendo as distâncias iniciais dos nós na topologia
# Chamamos a função fillInitialDistances(topology) do módulo utils para preencher as distâncias iniciais dos nós na topologia. 
# Essa função percorre cada nó na topologia e define suas distâncias iniciais com base nos vizinhos.
topology = utils.fillInitialDistances(topology)

# Definindo o nó principal como o primeiro nó da topologia
# Atribuímos o primeiro nó da topologia à variável mainNode. Esse nó é considerado o nó principal.
mainNode = topology[0]

# Obtendo o nó atual com base no rank
# usamos a função getCurrentNode(topology, rank) do módulo utils para obter o nó atual com base no rank. 
# A variável rank representa a classificação do processo atual no comunicador MPI. 
# Essa função percorre a topologia e retorna o nó cujo ID corresponde ao rank atual.
currentNode = utils.getCurrentNode(topology, rank)

# Verificando se o nó atual não existe na topologia
if currentNode is None:
    sys.exit()

def communicationsStopped():
    """
    Função chamada quando a comunicação é interrompida.
    Imprime as distâncias do nó atual.
    """
    distances = ''
    for distance in currentNode.distances:
        distances += distance.node.name + str(distance.distance) + ', '
    print('Node:' + currentNode.name + '\n' + 'Distances: ' + distances + '\n' + '______________________________________________')

# Criando um objeto de temporizador para chamar a função communicationsStopped()
# a cada 2 segundos
myTimer = classes.MyTimer(2, communicationsStopped)

# Se o rank atual for o mesmo do nó principal
if rank == mainNode.id:
    # Envia as distâncias para os vizinhos do nó principal
    utils.sendDistancesToNeighbors(mainNode.neighbors, mainNode.distances, comm)
    # Reinicia o temporizador
    myTimer.resetTimer()

while True:
    # Recebe uma mensagem de qualquer processo
    message = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        
    # Converte a mensagem recebida em uma lista de distâncias
    newDistances = utils.convertStringToDistances(message, topology)
    
    # Atualiza as distâncias do nó atual com base nas novas distâncias recebidas
    for newDistance in newDistances:
        if newDistance.node.id == currentNode.id:
            continue

        foundNode = False
        for distance in currentNode.distances:
            if newDistance.node.id == distance.node.id:
                foundNode = True
                if newDistance.distance + 1 < distance.distance:
                    distance.distance = newDistance.distance + 1

        if not foundNode:
            currentNode.distances.append(classes.Distance(newDistance.node, newDistance.distance + 1))

    # Envia as distâncias atualizadas para os vizinhos do nó atual
    utils.sendDistancesToNeighbors(currentNode.neighbors, currentNode.distances, comm)
    # Reinicia o temporizador
    myTimer.resetTimer()

