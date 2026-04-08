from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = size  

# Root initializes A and x
if rank == 0:
    A = np.random.randint(0, 10, size=(N, N))
    x = np.random.randint(0, 10, size=N)
else:
    A = None
    x = None

# Scatter rows of A
A_n = np.zeros(N, dtype=int)
comm.Scatter(A, A_n, root=0)

# Broadcast vector x to all processes
x = comm.bcast(x, root=0)

# Each process computes its piece
y_n = np.dot(A_n, x)

comm.Barrier()

# Gather results using non-blocking Igather
if rank == 0:
    y = np.zeros(N, dtype=int)
else:
    y = None

req = comm.Igather(y_n, y, root=0)
req.Wait()

# Root prints result
if rank == 0:
    print("Matrix A:")
    print(A)
    print("\nVector x:")
    print(x)
    print("\nResult y = A * x:\n")
    
    for i in range(N):
        row_str = " ".join(f"{val:3d}" for val in A[i])
        print(f"{row_str}  *  {x[i]:3d}  =  {y[i]:3d}")