from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

N = 10    # check for 10, 1000, 10000

if rank == 0:
    data = np.arange(1, N+1)
    chunks = np.array_split(data, size) #, root=0)
else:
    chunks = None

local_chunks = comm.scatter(chunks, root=0)
local_sums = np.sum(local_chunks)
gather_sums = comm.gather(local_sums, root=0)

if rank == 0:
    distributed_sum = sum(gather_sums)
    # formula for sum of 1..N
    check_sum = N * (N + 1) // 2
    print(f"The sum of 1-{N} is {distributed_sum} == {check_sum}")