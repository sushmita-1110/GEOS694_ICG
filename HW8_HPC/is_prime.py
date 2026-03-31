"""
Check if a number is prime or not, in parallel and serial, check time 
differences and that results match
"""
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor


def is_prime(n):
    for divisor in range(2, n):
        if n % divisor == 0:
            return False
    else:
        return True

def main(i, j):
    prime_numbers = []
    for n in range(i, j, 1):
        if is_prime(n):
            prime_numbers.append(n)
    return sum(prime_numbers)


if __name__ == "__main__":
    N = 100000
    nproc = int(sys.argv[1])
    step = N // nproc
    print(f"finding primes on {nproc} processors")

    # Serial
    start = time.time()
    total_serial = 0
    for i in range(1, N, step):
        total_serial += main(i, i + step)
    print(f"serial: {time.time() - start}")
    
    # Parallel
    start = time.time()
    with ProcessPoolExecutor(max_workers=nproc) as executor:
        futures = [executor.submit(main, i, i + step) 
                   for i in range(1, N, step)]
    total_parallel = 0
    for future in futures:
        total_parallel += future.result()
    print(f"parallel: {time.time() - start}")

    assert(total_serial == total_parallel)
    print("serial and parallel results match")
