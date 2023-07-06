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
# Verificamos se o currentNode é None (ou seja, se o nó atual não existe na topologia). 
# Se isso for verdadeiro, encerramos o programa usando sys.exit()
if currentNode is None:
    sys.exit()
# Definimos a função communicationsStopped(), que é chamada quando a comunicação é interrompida. 
# Essa função fala sobre as distâncias do nó atual e imprime informações relevantes.
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

# Em um loop infinito, recebemos mensagens de qualquer fonte e com qualquer tag usando comm.recv(). 
# Em seguida, convertemos a mensagem recebida em uma lista de distâncias usando convertStringToDistances() do módulo utils
while True:
    # Recebe uma mensagem de qualquer processo
    message = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        
    # Converte a mensagem recebida em uma lista de distâncias
    newDistances = utils.convertStringToDistances(message, topology)
    
    # Atualiza as distâncias do nó atual com base nas novas distâncias recebidas
    # Se os IDs forem iguais, significa que a distância recebida está relacionada ao próprio nó atual. 
    # Nesse caso, não precisamos realizar nenhuma ação adicional, 
    # então usamos a instrução continue para pular para a próxima iteração do loop, 
    # ignorando o restante do código dentro do loop para essa iteração específica.
    for newDistance in newDistances:
        if newDistance.node.id == currentNode.id:
            continue

        foundNode = False
        for distance in currentNode.distances:
            if newDistance.node.id == distance.node.id:
                # Configuramos a variável foundNode como True para indicar que encontramos o nó correspondente na lista de distâncias existentes.
                foundNode = True
                # Verifica se a nova distância mais 1 (newDistance.distance + 1) é menor que a distância existente (distance.distance). 
                # Se for, atualizamos a distância existente com o novo valor.
                if newDistance.distance + 1 < distance.distance:
                    distance.distance = newDistance.distance + 1
        # Após o loop for interior, verificamos o valor da variável foundNode. 
        # Se foundNode for False, significa que não encontramos uma correspondência para a nova distância na lista de distâncias existentes. 
        # Nesse caso, adicionamos uma nova instância da classe Distance à lista de distâncias existentes do nó atual (currentNode.distances). 
        # Essa nova instância representa a nova distância recebida, incrementada em 1
        if not foundNode:
            currentNode.distances.append(classes.Distance(newDistance.node, newDistance.distance + 1))

    # Envia as distâncias atualizadas para os vizinhos do nó atual
    utils.sendDistancesToNeighbors(currentNode.neighbors, currentNode.distances, comm)
    # Reinicia o temporizador
    myTimer.resetTimer()

