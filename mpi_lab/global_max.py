from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = random.randint(0, 1000)

global_max = comm.reduce(n, op=MPI.MAX , root=0)

global_max = comm.bcast(global_max, root=0)

if n == global_max:
    print(f"Rank {rank} has value {n} which is the global max {global_max}")
else:
    print(f"Rank {rank} has value {n} which is less than global max {global_max}")