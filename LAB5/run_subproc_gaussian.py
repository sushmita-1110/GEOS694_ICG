import time
import subprocess

start = time.time()

step = 1
for i in range(1, 1000, step):
    subprocess.Popen(f"2d_gaussian.py {i} {i+step}", 
                     shell=True)

elapsed = time.time() - start
print(f"Total Elapsed {time.time() - start:.2f}s")

