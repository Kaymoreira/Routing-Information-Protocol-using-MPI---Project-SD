import utils
from mpi4py import MPI

comm = MPI.COMM_WORLD   # get MPI communicator object
size = comm.size        # total number of processes
rank = comm.rank        # rank of this process
status = MPI.Status()   # get MPI status object

isDirectionRight = True

topology = utils.getTopology()
topology = utils.fillInitialDistances(topology)

for node in topology:
    for neighbor in node.neighbors:
        if(neighbor.pointed):
            comm.send(utils.convertDistancesToString(node.distances), neighbor.node.id)

if(rank == 9):
    while(True):
        test = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)

        print('test', test)
