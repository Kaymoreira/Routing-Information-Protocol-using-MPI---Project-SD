import utils
import classes
from mpi4py import MPI

comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object

isDirectionReversed = False

topology = utils.getTopology()
topology = utils.fillInitialDistances(topology)

mainNode = topology[0]

def fimDeEnvios():
    print('popo de elefante')
    isDirectionReversed = True
    mainNode = topology[8]

timer = classes.MyTimer(2, fimDeEnvios)

if(rank == mainNode.id):
    utils.sendDistancesToNeighbors(mainNode.neighbors, mainNode.distances, comm, isDirectionReversed)
    timer.resetTimer()

if(rank != mainNode.id):
    currentNode = None
    for node in topology:
        if(node.id == rank):
            currentNode = node
    
    if(currentNode != None):
        while(True):    
            for node in topology:
                if(node.id == rank):
                    currentNode = node
            
            if(currentNode == None):
                break
    
            newDistancesStr = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
            newDistances = utils.convertStringToDistances(newDistancesStr, topology)

            print(currentNode.name)
            for distance in currentNode.distances:
                print(distance.node.name, distance.distance)
            
            print('------------------------------')
            
            for newDistance in newDistances:
                if(newDistance.node.id == currentNode.id): 
                    continue

                foundNode = False
                for distance in currentNode.distances:
                    if(newDistance.node.id == distance.node.id):
                        foundNode = True
                        if(newDistance.distance + 1 < distance.distance):
                            distance.distance = newDistance.distance + 1

                if(foundNode == False):
                    currentNode.distances.append(classes.Distance(newDistance.node, newDistance.distance + 1))

            utils.sendDistancesToNeighbors(currentNode.neighbors, currentNode.distances, comm, isDirectionReversed)
            timer.resetTimer()
        
        


# for node in topology:
#     for neighbor in node.neighbors:
#         if(neighbor.pointed):
#             comm.send(utils.convertDistancesToString(node.distances), neighbor.node.id)


# if(rank == 9):
#     while(True):
#         test = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)

#         print('test', test)




""" print(currentNode.name)
    for distance in currentNode.distances:
        print(distance.node.name, distance.distance)
    
    print('------------------------------') """