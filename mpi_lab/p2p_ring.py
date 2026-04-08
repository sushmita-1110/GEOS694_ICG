from mpi4py import MPI
import random
import os

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
PID = os.getpid()

if rank == 0:
    n = random.randint(1, 10)
    message = (f"hello world! {n}")

    comm.send(message, dest=1, tag=11)
    final_message = comm.recv(source=size-1)
    print(final_message)

elif rank < size - 1:
    message = comm.recv(source=rank-1, tag=11)
    last_value = int(message.split()[-1])
    new_value = last_value * rank

    message += f" {new_value}"
    comm.send(message, dest=rank+1, tag=11)

else:
    message = comm.recv(source=rank-1, tag=11)
    last_value = int(message.split()[-1])
    new_value = last_value * rank
    
    # append result
    message += f" {new_value} goodbye world!"
    comm.send(message, dest=0)







